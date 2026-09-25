"""ElasticSearch storage backend.

Ports the original dashboard's ES code (flask-server/query_dsl/query_dsl.py,
bp_routes/dashboard.py and es_importing/*.py) behind the DashboardBackend
interface so the same UI works against an ES instance when datasets grow
beyond what DuckDB/Parquet handles comfortably.

The elasticsearch python package is imported lazily (module level import in
_init_client only), so parquet-only deployments never need it installed.
"""

import os

import pandas as pd

from ..utils import sanitize_dataset_name
from .base import (
    CategoricalFilter,
    DashboardBackend,
    DISTINCT_CAP,
    UnknownDatasetError,
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

    # -- catalog -----------------------------------------------------------

    def list_datasets(self):
        entries = self.es.cat.indices(format='json')
        return sorted(entry['index'] for entry in entries)

    def dataset_exists(self, name):
        return bool(self.es.indices.exists(index=name))

    def delete_dataset(self, name):
        self.es.indices.delete(index=name, ignore=[400, 404])
        path = meta_path(self.datasets_dir, name)
        if os.path.isfile(path):
            os.remove(path)

    # -- ingestion ---------------------------------------------------------

    def create_dataset(self, name, csv_path):
        from elasticsearch import helpers
        name = sanitize_dataset_name(name)
        df = pd.read_csv(csv_path, sep=None, engine='python')
        df = df.astype(object).where(pd.notnull(df), None)

        if not self.es.indices.exists(index=name):
            mappings = {
                'properties': {
                    col: {'type': _pandas_type_to_es(dtype)}
                    for col, dtype in df.dtypes.items()
                }
            }
            self.es.indices.create(index=name, body={
                'settings': {'index': {'number_of_shards': self.index_shards}},
                'mappings': mappings,
            })

        actions = (
            {'_index': name, '_id': idx, '_source': record}
            for idx, record in enumerate(df.to_dict('records'))
        )
        helpers.bulk(self.es, actions)

        self._build_meta(name, df, csv_path)
        return name

    def _build_meta(self, name, df, csv_path):
        fields = {}
        categorical = {}
        continuous = {}
        for col, dtype in df.dtypes.items():
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
            'backend': self.name,
            'row_count': int(len(df)),
            'store_size': None,
            'updated': None,
            'fields': fields,
            'categorical': categorical,
            'continuous': continuous,
            'source_path': csv_path,
            'source_size': os.path.getsize(csv_path) if csv_path and os.path.isfile(csv_path) else None,
            'dashboard': {},
        }
        write_meta(self.datasets_dir, name, meta)
        return meta

    # -- schema ------------------------------------------------------------

    def get_field_types(self, name):
        if not self.es.indices.exists(index=name):
            raise UnknownDatasetError(name)
        mappings = self.es.indices.get_mapping(index=name)[name]['mappings']['properties']
        result = {}
        for key, value in mappings.items():
            es_type = value.get('type')
            if es_type is None:
                continue
            result[key] = es_type
        return result

    def get_filter_values(self, name):
        field_types = self.get_field_types(name)
        categorical = {}
        continuous = {}
        for field, ftype in field_types.items():
            if ftype == 'keyword':
                body = {
                    'size': 0,
                    'aggs': {field: {'terms': {'field': field, 'size': DISTINCT_CAP}}},
                }
                resp = self.es.search(index=name, body=body)
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
                resp = self.es.search(index=name, body=body)
                aggs = resp['aggregations']
                continuous[field] = [aggs['min_' + field]['value'], aggs['max_' + field]['value']]
        return categorical, continuous

    def get_meta(self, name):
        return load_meta(self.datasets_dir, name)

    def get_status(self, name):
        for index_data in self.es.cat.indices(format='json'):
            if index_data['index'] == name:
                return {
                    'health': index_data.get('health'),
                    'status': index_data.get('status'),
                    'storage_size': index_data.get('store.size'),
                    'docs_count': index_data.get('docs.count'),
                }
        raise UnknownDatasetError(name)

    # -- querying ----------------------------------------------------------

    def query(self, spec):
        if not self.es.indices.exists(index=spec.dataset):
            raise UnknownDatasetError(spec.dataset)
        field_types = self.validate_fields(
            spec.dataset, list(spec.group_by) + [spec.field, spec.n_field])
        for agg in spec.aggregates:
            if agg.name in NUMERIC_AGGS and field_types.get(agg.field) == 'keyword':
                raise ValueError(
                    'Aggregate %r is not valid on the keyword field %r'
                    % (agg.name, agg.field)
                )
        body = self._composite_query_body(spec)
        resp = self.es.search(index=spec.dataset, body=body)
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
