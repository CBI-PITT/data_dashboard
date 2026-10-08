"""ElasticsearchBackend tests against the in-python fake ES client: request
parity with the original query_dsl composite query, ingest, schema, status."""

import pytest

from data_dashboard.backends.base import (
    Aggregate,
    CategoricalFilter,
    ContinuousFilter,
    QuerySpec,
    UnknownDatasetError,
)


# -- composite query body parity ---------------------------------------------


def test_composite_query_body_matches_original_contract(es_backend):
    spec = QuerySpec(
        dataset="klimstra5.0", field="x_raw",
        filters=[
            CategoricalFilter("treatment", ["ctrl", "stim"]),
            ContinuousFilter("x_raw", 0.0, 10.0),
        ],
        group_by=["treatment", "route"],
        aggregates=[Aggregate("avg", "x_raw"), Aggregate("value_count", "x_raw")],
        n_field="metadata",
    )
    body = es_backend._composite_query_body(spec)
    must = body["query"]["bool"]["filter"]["bool"]["must"]
    # categorical -> bool should of term clauses
    assert must[0] == {"bool": {"should": [
        {"term": {"treatment": "ctrl"}}, {"term": {"treatment": "stim"}}]}}
    # continuous -> range filter
    assert must[1] == {"range": {"x_raw": {"gte": 0.0, "lte": 10.0}}}
    # composite sources for every group field
    sources = body["aggs"]["categories"]["composite"]["sources"]
    assert sources == [{"treatment": {"terms": {"field": "treatment"}}},
                       {"route": {"terms": {"field": "route"}}}]
    assert body["aggs"]["categories"]["composite"]["size"] == 100000
    # sub-aggs keyed <agg>_<field> plus the N cardinality agg
    sub = body["aggs"]["categories"]["aggs"]
    assert sub == {
        "avg_x_raw": {"avg": {"field": "x_raw"}},
        "value_count_x_raw": {"value_count": {"field": "x_raw"}},
        "N": {"cardinality": {"field": "metadata"}},
    }
    assert body["size"] == 0


def test_composite_query_body_empty_categorical_means_no_filter_clause(es_backend):
    spec = QuerySpec(
        dataset="idx", field="x_raw",
        filters=[CategoricalFilter("treatment", [])],
        group_by=["treatment"], aggregates=[Aggregate("avg", "x_raw")])
    body = es_backend._composite_query_body(spec)
    assert body["query"]["bool"]["filter"]["bool"]["must"] == []


# -- ingest -------------------------------------------------------------------


def test_create_dataset_builds_mapping_and_bulk_indexes(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text(
        "treatment,x_raw\n"
        "ctrl,1.0\n"
        "ctrl,2.0\n"
        "stim,3.0\n")
    name = es_backend.create_dataset("klimstra_cells", str(csv_path))
    assert name == "klimstra_cells"
    index, body = es_backend.es.created_bodies[0]
    assert index == "klimstra_cells"
    mappings = body["mappings"]["properties"]
    assert mappings == {"treatment": {"type": "keyword"}, "x_raw": {"type": "float"}}
    assert len(es_backend.es.indices_data["klimstra_cells"]["docs"]) == 3


def test_create_dataset_writes_sidecar_meta(es_backend, tmp_path, datasets_dir):
    import os
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text("treatment,x_raw\nctrl,1.0\nstim,3.0\n")
    es_backend.create_dataset("sidecar_cells", str(csv_path))
    sidecar = os.path.join(datasets_dir, "sidecar_cells.dashboard_meta.json")
    assert os.path.isfile(sidecar)
    import json
    meta = json.load(open(sidecar))
    assert meta["fields"]["treatment"] == "keyword"
    assert meta["categorical"]["treatment"] == ["ctrl", "stim"]
    assert meta["continuous"]["x_raw"] == [1.0, 3.0]


# -- delete containment -------------------------------------------------------


def test_delete_containment_check_runs_before_any_removal(es_backend):
    """The ensure_within containment check aborts with PermissionError before
    the ES index delete runs, so a '..' identifier can neither remove files
    outside the dashboard folder nor touch other indices."""
    es_backend.es.indices_data["../../escape"] = {"mappings": {}, "docs": []}
    with pytest.raises(PermissionError):
        es_backend.delete_dataset("../../escape")
    assert "../../escape" in es_backend.es.indices_data


def test_delete_removes_index_and_sidecar(es_backend, tmp_path, datasets_dir):
    import os
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text("treatment,x_raw\nctrl,1.0\n")
    es_backend.create_dataset("gone_soon", str(csv_path))
    sidecar = os.path.join(datasets_dir, "gone_soon.dashboard_meta.json")
    assert os.path.isfile(sidecar)
    es_backend.delete_dataset("gone_soon")
    assert "gone_soon" not in es_backend.es.indices_data
    assert not os.path.isfile(sidecar)


# -- schema and status --------------------------------------------------------


def test_get_field_types_from_mapping(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text("treatment,x_raw\nctrl,1.0\n")
    es_backend.create_dataset("mapped", str(csv_path))
    fields = es_backend.get_field_types("mapped")
    assert fields == {"treatment": "keyword", "x_raw": "float"}


def test_get_filter_values_runs_terms_and_minmax_aggs(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text(
        "treatment,x_raw\n"
        "ctrl,1.0\n"
        "ctrl,2.0\n"
        "stim,3.0\n")
    es_backend.create_dataset("filtered", str(csv_path))
    categorical, continuous = es_backend.get_filter_values("filtered")
    assert categorical["treatment"] == ["ctrl", "stim"]
    assert continuous["x_raw"] == [1.0, 3.0]


def test_get_status_from_cat_indices(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text("treatment,x_raw\nctrl,1.0\n")
    es_backend.create_dataset("status_idx", str(csv_path))
    status = es_backend.get_status("status_idx")
    assert status == {
        "health": "green", "status": "open",
        "storage_size": "1.2mb", "docs_count": "1",
    }


def test_list_datasets_sorted(es_backend, tmp_path):
    for name in ("beta", "alpha"):
        csv_path = tmp_path / (name + ".csv")
        csv_path.write_text("x_raw\n1.0\n")
        es_backend.create_dataset(name, str(csv_path))
    assert es_backend.list_datasets() == ["alpha", "beta"]


# -- querying -----------------------------------------------------------------


def test_query_returns_normalized_buckets_and_validates_fields(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text(
        "treatment,metadata,x_raw\n"
        "ctrl,1,1.0\n"
        "ctrl,2,2.0\n"
        "stim,1,3.0\n")
    es_backend.create_dataset("queried", str(csv_path))
    spec = QuerySpec(
        dataset="queried", field="x_raw",
        filters=[CategoricalFilter("treatment", ["ctrl"])],
        group_by=["treatment"],
        aggregates=[Aggregate("avg", "x_raw"), Aggregate("value_count", "x_raw")],
        n_field="metadata")
    buckets = es_backend.query(spec)
    assert len(buckets) == 1
    bucket = buckets[0]
    assert bucket["key"] == {"treatment": "ctrl"}
    assert bucket["doc_count"] == 2
    assert bucket["avg_x_raw"]["value"] == 1.5
    assert bucket["value_count_x_raw"]["value"] == 2
    assert bucket["N"]["value"] == 2  # two distinct metadata ids among ctrl docs

    with pytest.raises(UnknownDatasetError):
        es_backend.query(QuerySpec(
            dataset="missing", field="x_raw", filters=[], group_by=["treatment"],
            aggregates=[Aggregate("avg", "x_raw")]))
    with pytest.raises(Exception):
        es_backend.query(QuerySpec(
            dataset="queried", field="x_raw", filters=[], group_by=["nope"],
            aggregates=[Aggregate("avg", "x_raw")]))


def test_numeric_agg_on_keyword_field_rejected(es_backend, tmp_path):
    csv_path = tmp_path / "cells.csv"
    csv_path.write_text("treatment,x_raw\nctrl,1.0\n")
    es_backend.create_dataset("kw", str(csv_path))
    with pytest.raises(ValueError):
        es_backend.query(QuerySpec(
            dataset="kw", field="treatment", filters=[], group_by=["treatment"],
            aggregates=[Aggregate("avg", "treatment")]))


def test_both_backends_return_equivalent_buckets(parquet_backend, es_backend, cells_csv):
    """The abstraction contract: the same CSV + the same QuerySpec produce
    equivalent buckets from the parquet and elasticsearch backends."""
    from data_dashboard.backends.base import QuerySpec, Aggregate
    name = parquet_backend.create_dataset("parity", cells_csv)
    es_backend.create_dataset("parity", cells_csv)
    spec = QuerySpec(
        dataset="parity", field="x_raw",
        filters=[CategoricalFilter("treatment", ["ctrl"])],
        group_by=["atlas_structure_acronym"],
        aggregates=[
            Aggregate("avg", "x_raw"), Aggregate("value_count", "x_raw"),
            Aggregate("boxplot", "x_raw"),
        ],
        n_field="metadata")
    pq_buckets = parquet_backend.query(spec)
    es_buckets = es_backend.query(spec)
    assert len(pq_buckets) == len(es_buckets)
    for pq, es in zip(pq_buckets, es_buckets):
        assert pq["key"] == es["key"]
        assert pq["doc_count"] == es["doc_count"]
        assert pq["avg_x_raw"]["value"] == pytest.approx(es["avg_x_raw"]["value"])
        assert pq["value_count_x_raw"]["value"] == es["value_count_x_raw"]["value"]
        for part in ("min", "max", "q1", "q2", "q3"):
            assert pq["boxplot_x_raw"][part] == pytest.approx(es["boxplot_x_raw"][part])
        assert pq["N"]["value"] == es["N"]["value"]
