"""ElasticSearch storage backend.

Ports the original dashboard's ES code (flask-server/query_dsl/query_dsl.py,
bp_routes/dashboard.py and es_importing/*.py) behind the DashboardBackend
interface so the same UI works against an ES instance when datasets grow
beyond what DuckDB/Parquet handles comfortably.

Ownership: datasets created through the blueprint get an ES index named
`<owner>--<name>` (index names cannot contain '/') and a sidecar meta in the
owner's folder under datasets_dir. Ownerless/legacy indices (no sidecar
anywhere, e.g. the original klimstra*/cebra* indices) are addressed with a
plain-name identifier and are admin-only (enforced in the routes).

Merging is parquet-only for now (ES merging would need scripted _reindex).
The elasticsearch python package is imported lazily, so parquet-only
deployments never need it installed.
"""

import json
import os
import re

import pandas as pd

from ..utils import sanitize_dataset_name
from .base import (
    CategoricalFilter,
    DashboardBackend,
    DISTINCT_CAP,
    UnknownDatasetError,
    build_identifier,
    load_meta,
    meta_path,
    write_meta,
)

NUMERIC_AGGS = ('min', 'max', 'avg', 'sum', 'boxplot')


def _pandas_type_to_es(dtype):
    name = str(dtype)
    if name == 'object':
        return 'keyword'
    if name.startswith('int'):
        return 'long'
    if name.startswith('float'):
        return 'float'
    if name == 'bool':
        return 'boolean'
    if name.startswith('datetime'):
        return 'date'
    return 'keyword'


class ElasticsearchBackend(DashboardBackend):
    name = 'elasticsearch'

    def __init__(self, datasets_dir, es_server='http://localhost:9200',
                 index_shards=1, request_timeout=180):
        self.datasets_dir = os.path.realpath(datasets_dir)
        os.makedirs(self.datasets_dir, exist_ok=True)
        self.index_shards = int(index_shards)
        self._es_server = es_server
        self._request_timeout = request_timeout
        self.es = self._init_client(es_server, request_timeout)

    @staticmethod
    def _init_client(es_server, request_timeout):
        from elasticsearch import Elasticsearch
        return Elasticsearch(es_server, request_timeout=request_timeout)

    # -- dataset locations -------------------------------------------------

    def _user_dir(self, owner):
        return os.path.join(self.datasets_dir, owner) if owner else self.datasets_dir

    def _index_name(self, name, owner=None):
        """ES index names cannot contain '/', so owned datasets get an
        owner-prefixed index; ownerless/legacy keep the plain name."""
        return '%s--%s' % (owner, name) if owner else name

    def _sidecar_exists(self, name, owner):
        return os.path.isfile(meta_path(self._user_dir(owner), name))

    # -- catalog -----------------------------------------------------------

    def list_datasets(self, owner=None):
        identifiers = []
        if owner:
            folder = self._user_dir(owner)
            try:
                entries = os.listdir(folder)
            except OSError:
                return []
            for fname in entries:
                if fname.endswith('.dashboard_meta.json'):
                    identifiers.append(
                        build_identifier(fname[:-len('.dashboard_meta.json')], owner))
            return sorted(identifiers)
        # admin: every user folder's sidecars plus ownerless legacy indices
        for entry in sorted(os.listdir(self.datasets_dir)):
            path = os.path.join(self.datasets_dir, entry)
            if os.path.isdir(path):
                for fname in os.listdir(path):
                    if fname.endswith('.dashboard_meta.json'):
                        identifiers.append(build_identifier(
                            fname[:-len('.dashboard_meta.json')], entry))
        sided = {identifier for identifier in identifiers}
        for entry in self.es.cat.indices(format='json'):
            index_name = entry['index']
            if index_name not in sided and not index_name.startswith('.'):
                identifiers.append(index_name)
        return sorted(identifiers)

    def dataset_exists(self, name, owner=None):
        return bool(self.es.indices.exists(index=self._index_name(name, owner)))

    def delete_dataset(self, name, owner=None):
        self.es.indices.delete(index=self._index_name(name, owner), ignore=[400, 404])
        path = meta_path(self._user_dir(owner), name)
        if os.path.isfile(path):
            os.remove(path)

    def rename_dataset(self, name, new_name, owner=None):
        """ES cannot rename indices in place: _reindex to the new name,
        refresh, delete the old, then rename the sidecar."""
        new_name = sanitize_dataset_name(new_name)
        old_index = self._index_name(name, owner)
        if not self.es.indices.exists(index=old_index):
            raise UnknownDatasetError(name)
        new_index = self._index_name(new_name, owner)
        if self.es.indices.exists(index=new_index):
            raise ValueError("A dataset named %r already exists" % (new_name,))
        self.es.reindex(
            body={'source': {'index': old_index}, 'dest': {'index': new_index}},
            refresh=True,
        )
        self.es.indices.delete(index=old_index)
        meta = load_meta(self._user_dir(owner), name)
        src_meta = meta_path(self._user_dir(owner), name)
        if os.path.isfile(src_meta):
            os.rename(src_meta, meta_path(self._user_dir(owner), new_name))
        if meta is not None:
            meta['name'] = new_name
            write_meta(self._user_dir(owner), new_name, meta)
        return new_name

    def merge_datasets(self, sources, new_name, owner=None):
        raise NotImplementedError(
            'Merging is parquet-only for now; re-ingest the merged data with '
            'the parquet backend or import_csv.py')

    # -- ingestion ---------------------------------------------------------

    def create_dataset(self, name, csv_path, owner=None):
        from elasticsearch import helpers
        name = sanitize_dataset_name(name)
        # Always-create semantics: an existing index name gets a _2, _3... suffix.
        match = re.match(r'^(.*)_(\d+)$', name)
        if match:
            base, counter = match.group(1), int(match.group(2))
        else:
            base, counter = name, 1
        while self.es.indices.exists(index=self._index_name(name, owner)):
            counter += 1
            name = '%s_%d' % (base, counter)
        index_name = self._index_name(name, owner)

        df = pd.read_csv(csv_path, sep=None, engine='python')
        # Capture the sniffed dtypes before the object conversion below, or
        # every column would map to keyword.
        dtypes = {col: dtype for col, dtype in df.dtypes.items()}
        df = df.astype(object).where(pd.notnull(df), None)

        mappings = {
            'properties': {
                col: {'type': _pandas_type_to_es(dtype)}
                for col, dtype in dtypes.items()
            }
        }
        self.es.indices.create(index=index_name, body={
            'settings': {'index': {'number_of_shards': self.index_shards}},
            'mappings': mappings,
        })

        actions = (
            {'_index': index_name, '_id': idx, '_source': record}
            for idx, record in enumerate(df.to_dict('records'))
        )
        helpers.bulk(self.es, actions)

        self._build_meta(name, owner, df, csv_path, dtypes)
        return name

    def _build_meta(self, name, owner, df, csv_path, dtypes):
        fields = {}
        categorical = {}
        continuous = {}
        for col, dtype in dtypes.items():
            fields[col] = _pandas_type_to_es(dtype)
            if fields[col] == 'keyword':
                values = [str(v) for v in df[col].dropna().unique()][:DISTINCT_CAP]
                categorical[col] = sorted(values)
            else:
                numeric = pd.to_numeric(df[col], errors='coerce').dropna()
                if not numeric.empty:
                    continuous[col] = [float(numeric.min()), float(numeric.max())]
        meta = {
            'name': name,
            'owner': owner,
            'backend': self.name,
            'row_count': int(len(df)),
            'store_size': None,
            'updated': None,
            'fields': fields,
            'categorical': categorical,
            'continuous': continuous,
            'source_path': csv_path,
            'source_size': os.path.getsize(csv_path) if csv_path and os.path.isfile(csv_path) else None,
            'samples': [],
            'dashboard': {},
        }
        write_meta(self._user_dir(owner), name, meta)
        return meta

    # -- schema ------------------------------------------------------------

    def get_field_types(self, name, owner=None):
        if not self.es.indices.exists(index=self._index_name(name, owner)):
            raise UnknownDatasetError(name)
        mappings = self.es.indices.get_mapping(
            index=self._index_name(name, owner))[self._index_name(name, owner)]['mappings']['properties']
        result = {}
        for key, value in mappings.items():
            es_type = value.get('type')
            if es_type is None:
                continue
            result[key] = es_type
        return result

    def get_filter_values(self, name, owner=None):
        field_types = self.get_field_types(name, owner)
        categorical = {}
        continuous = {}
        for field, ftype in field_types.items():
            if ftype == 'keyword':
                body = {
                    'size': 0,
                    'aggs': {field: {'terms': {'field': field, 'size': DISTINCT_CAP}}},
                }
                resp = self.es.search(index=self._index_name(name, owner), body=body)
                categorical[field] = [
                    bucket['key'] for bucket in resp['aggregations'][field]['buckets']
                ]
            else:
                body = {
                    'size': 0,
                    'aggs': {
                        'max_' + field: {'max': {'field': field}},
                        'min_' + field: {'min': {'field': field}},
                    },
                }
                resp = self.es.search(index=self._index_name(name, owner), body=body)
                aggs = resp['aggregations']
                continuous[field] = [aggs['min_' + field]['value'], aggs['max_' + field]['value']]
        return categorical, continuous

    def get_meta(self, name, owner=None):
        return load_meta(self._user_dir(owner), name)

    def get_status(self, name, owner=None):
        index_name = self._index_name(name, owner)
        for index_data in self.es.cat.indices(format='json'):
            if index_data['index'] == index_name:
                return {
                    'health': index_data.get('health'),
                    'status': index_data.get('status'),
                    'storage_size': index_data.get('store.size'),
                    'docs_count': index_data.get('docs.count'),
                }
        raise UnknownDatasetError(name)

    # -- querying ----------------------------------------------------------

    def query(self, spec):
        index_name = self._index_name(spec.dataset, spec.owner)
        if not self.es.indices.exists(index=index_name):
            raise UnknownDatasetError(spec.dataset)
        field_types = self.validate_fields(
            spec.dataset, list(spec.group_by) + [spec.field, spec.n_field], spec.owner)
        for agg in spec.aggregates:
            if agg.name in NUMERIC_AGGS and field_types.get(agg.field) == 'keyword':
                raise ValueError(
                    'Aggregate %r is not valid on the keyword field %r'
                    % (agg.name, agg.field)
                )
        body = self._composite_query_body(spec)
        resp = self.es.search(index=index_name, body=body)
        return resp['aggregations']['categories']['buckets']

    def _composite_query_body(self, spec):
        """Port of query_dsl.Query.formCompositeQuery, fed from a QuerySpec."""
        form_query_body = {
            'size': 0,
            'query': {'bool': {'filter': {'bool': {'must': []}}}},
        }
        must = form_query_body['query']['bool']['filter']['bool']['must']
        for f in spec.filters:
            if isinstance(f, CategoricalFilter):
                values = [v for v in f.values if str(v) != '']
                if not values:
                    continue
                should = [{'term': {f.field: value}} for value in values]
                must.append({'bool': {'should': should}})
            else:
                if f.min is None and f.max is None:
                    continue
                must.append({'range': {f.field: {'gte': f.min, 'lte': f.max}}})

        form_query_body['aggs'] = {'categories': {'aggs': {}}}
        form_query_body['aggs']['categories']['composite'] = {
            'sources': [
                {group_by: {'terms': {'field': group_by}}} for group_by in spec.group_by
            ],
            'size': spec.size_cap or DISTINCT_CAP,
        }

        aggs = {}
        for agg in spec.aggregates:
            aggs[agg.name + '_' + agg.field] = {agg.name: {'field': agg.field}}
        if spec.n_field:
            aggs['N'] = {'cardinality': {'field': spec.n_field}}
        form_query_body['aggs']['categories']['aggs'] = aggs
        return form_query_body
