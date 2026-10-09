"""In-python stand-in for the elasticsearch python package.

Implements just enough of the ES client for the ElasticsearchBackend to run:
mapping create/exists/get_mapping, term/range filtered docs, the composite
aggregation (group-by sources + metric sub-aggs over stored docs), cat
indices, and helpers.bulk. This lets the suite assert request-body parity
with the original query_dsl code AND that both backends return equivalent
buckets from the same data.
"""

import sys
import types


def _quantile(sorted_vals, q):
    if not sorted_vals:
        return None
    n = len(sorted_vals)
    pos = q * (n - 1)
    low = int(pos)
    high = min(low + 1, n - 1)
    frac = pos - low
    return sorted_vals[low] * (1 - frac) + sorted_vals[high] * frac


class _FakeCat:
    def __init__(self, client):
        self._client = client

    def indices(self, format=None):
        return [
            {
                "index": name,
                "health": "green",
                "status": "open",
                "store.size": "1.2mb",
                "docs.count": str(len(data["docs"])),
            }
            for name, data in sorted(self._client.indices_data.items())
        ]


class _FakeIndices:
    def __init__(self, client):
        self._client = client

    def exists(self, index=None):
        return index in self._client.indices_data

    def get_mapping(self, index=None):
        data = self._client.indices_data[index]
        return {index: {"mappings": {"properties": data["mappings"]}}}

    def create(self, index=None, body=None):
        self._client.indices_data[index] = {
            "mappings": body["mappings"]["properties"],
            "docs": [],
        }
        self._client.created_bodies.append((index, body))

    def delete(self, index=None, ignore=None):
        self._client.indices_data.pop(index, None)


class FakeESClient:
    def __init__(self, *args, **kwargs):
        self.indices_data = {}
        self.cat = _FakeCat(self)
        self.indices = _FakeIndices(self)
        self.search_calls = []
        self.created_bodies = []

    def search(self, index=None, body=None):
        self.search_calls.append((index, body))
        aggs = body.get("aggs") or {}
        if "categories" in aggs:
            return {
                "aggregations": {
                    "categories": {"buckets": self._composite(index, body)}
                }
            }
        if aggs:
            out = {}
            for key, spec in aggs.items():
                agg_type, agg_spec = list(spec.items())[0]
                if agg_type == "terms":
                    counts = {}
                    for doc in self.indices_data[index]["docs"]:
                        value = doc.get(agg_spec["field"])
                        if value is not None:
                            counts[value] = counts.get(value, 0) + 1
                    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
                    size = int(agg_spec.get("size") or 10)
                    buckets = [
                        {"key": key, "doc_count": count}
                        for key, count in ordered[:size]
                    ]
                    other = sum(count for _, count in ordered[size:])
                    out[key] = {
                        "buckets": buckets,
                        "sum_other_doc_count": other,
                    }
                    continue
                if agg_type == "cardinality":
                    field = agg_spec["field"]
                    distinct = {
                        doc.get(field)
                        for doc in self.indices_data[index]["docs"]
                        if doc.get(field) is not None
                    }
                    out[key] = {"value": len(distinct)}
                    continue
                if agg_type == "extended_stats":
                    field = agg_spec["field"]
                    values = [
                        doc.get(field)
                        for doc in self.indices_data[index]["docs"]
                        if isinstance(doc.get(field), (int, float))
                    ]
                    n = len(values)
                    if not n:
                        out[key] = {
                            "count": 0, "min": None, "max": None,
                            "avg": None, "sum": 0, "std_deviation": None,
                        }
                        continue
                    mean = sum(values) / n
                    variance = (
                        sum((v - mean) ** 2 for v in values) / (n - 1)
                    ) if n > 1 else 0.0
                    out[key] = {
                        "count": n,
                        "min": min(values),
                        "max": max(values),
                        "avg": mean,
                        "sum": sum(values),
                        "std_deviation": variance ** 0.5,
                    }
                    continue
                if agg_type == "percentiles":
                    field = agg_spec["field"]
                    percents = agg_spec.get("percents") or [25, 50, 75]
                    values = sorted(
                        doc.get(field)
                        for doc in self.indices_data[index]["docs"]
                        if isinstance(doc.get(field), (int, float))
                    )
                    percents_out = {
                        ("%s.0" % p): _quantile(values, p / 100.0)
                        for p in percents
                    }
                    out[key] = {"values": percents_out}
                    continue
                values = [
                    doc.get(agg_spec["field"])
                    for doc in self.indices_data[index]["docs"]
                    if isinstance(doc.get(agg_spec["field"]), (int, float))
                ]
                if agg_type == "min":
                    out[key] = {"value": min(values) if values else None}
                elif agg_type == "max":
                    out[key] = {"value": max(values) if values else None}
                else:
                    out[key] = {"value": None}
            return {"aggregations": out}
        # Plain hits search (spreadsheet rows: from/size in stored order).
        docs = self._filtered_docs(index, body.get("query"))
        start = int(body.get("from") or 0)
        size = int(body.get("size") or 10)
        source = body.get("_source")
        hits = []
        for doc in docs[start:start + size]:
            if source is None:
                src = dict(doc)
            else:
                src = {field: doc.get(field) for field in source}
            hits.append({"_source": src})
        return {"hits": {"total": {"value": len(docs)}, "hits": hits}}

    def count(self, index=None, body=None):
        docs = self._filtered_docs(index, (body or {}).get("query"))
        return {"count": len(docs)}

    def reindex(self, body=None, refresh=False):
        """_reindex: copy all documents from source to dest."""
        source = body["source"]["index"]
        dest = body["dest"]["index"]
        self.indices_data[dest] = {
            "mappings": self.indices_data[source]["mappings"],
            "docs": list(self.indices_data[source]["docs"]),
        }

    # -- composite execution ------------------------------------------------

    def _filtered_docs(self, index, query):
        docs = self.indices_data[index]["docs"]
        if not query or "match_all" in query:
            return list(docs)
        must = query["bool"]["filter"]["bool"]["must"]
        out = []
        for doc in docs:
            keep = True
            for clause in must:
                if "bool" in clause:
                    matched = False
                    for term in clause["bool"]["should"]:
                        (field, value), = term["term"].items()
                        if doc.get(field) == value:
                            matched = True
                    if not matched:
                        keep = False
                elif "range" in clause:
                    (field, rng), = clause["range"].items()
                    value = doc.get(field)
                    if not isinstance(value, (int, float)):
                        keep = False
                    else:
                        if rng.get("gte") is not None and value < rng["gte"]:
                            keep = False
                        if rng.get("lte") is not None and value > rng["lte"]:
                            keep = False
                if not keep:
                    break
            if keep:
                out.append(doc)
        return out

    def _composite(self, index, body):
        docs = self._filtered_docs(index, body.get("query"))
        composite = body["aggs"]["categories"]["composite"]
        sources = [list(src.keys())[0] for src in composite["sources"]]
        sub_aggs = body["aggs"]["categories"]["aggs"]

        groups = {}
        for doc in docs:
            key = tuple(doc.get(source) for source in sources)
            if any(value is None for value in key):
                continue
            groups.setdefault(key, []).append(doc)

        buckets = []
        for key in sorted(groups.keys(), key=lambda k: tuple(str(v) for v in k)):
            group_docs = groups[key]
            bucket = {"key": dict(zip(sources, key)), "doc_count": len(group_docs)}
            for agg_name, agg_spec in sub_aggs.items():
                if agg_name == "N":
                    field = agg_spec["cardinality"]["field"]
                    distinct = {
                        doc.get(field)
                        for doc in group_docs
                        if doc.get(field) is not None
                    }
                    bucket[agg_name] = {"value": len(distinct)}
                    continue
                agg_type, agg_field_spec = list(agg_spec.items())[0]
                field = agg_field_spec["field"]
                values = sorted(
                    doc.get(field)
                    for doc in group_docs
                    if isinstance(doc.get(field), (int, float))
                )
                if agg_type == "value_count":
                    bucket[agg_name] = {"value": len(values)}
                elif agg_type == "cardinality":
                    bucket[agg_name] = {"value": len(set(values))}
                elif agg_type == "avg":
                    bucket[agg_name] = {
                        "value": (sum(values) / len(values)) if values else None
                    }
                elif agg_type == "sum":
                    bucket[agg_name] = {"value": sum(values) if values else 0}
                elif agg_type == "min":
                    bucket[agg_name] = {"value": values[0] if values else None}
                elif agg_type == "max":
                    bucket[agg_name] = {"value": values[-1] if values else None}
                elif agg_type == "boxplot":
                    bucket[agg_name] = {
                        "min": values[0] if values else None,
                        "max": values[-1] if values else None,
                        "q1": _quantile(values, 0.25),
                        "q2": _quantile(values, 0.5),
                        "q3": _quantile(values, 0.75),
                    }
            buckets.append(bucket)
        return buckets


class _FakeHelpers:
    @staticmethod
    def bulk(es, actions):
        count = 0
        for action in actions:
            index = action["_index"]
            es.indices_data.setdefault(index, {"mappings": {}, "docs": []})
            es.indices_data[index]["docs"].append(action["_source"])
            count += 1
        return count, []


def install(monkeypatch):
    """Stub the elasticsearch module in sys.modules (the backend imports it
    lazily inside ElasticsearchBackend._init_client)."""
    stub = types.ModuleType("elasticsearch")
    stub.Elasticsearch = FakeESClient
    stub.helpers = _FakeHelpers
    monkeypatch.setitem(sys.modules, "elasticsearch", stub)
    return stub
