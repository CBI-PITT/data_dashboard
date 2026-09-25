"""DuckDB + Parquet storage backend (the default, service-free engine).

Datasets are stored as one Parquet file per dataset plus a sidecar
.dashboard_meta.json (schema cache + dashboard parameters) in the configured
datasets_dir. Queries run as SQL aggregates over the Parquet file.
"""

import os

import duckdb

from ..utils import sanitize_dataset_name
from .base import (
    CategoricalFilter,
    DashboardBackend,
    DISTINCT_CAP,
    UnknownDatasetError,
    format_byte_size,
    load_meta,
    meta_path,
    write_meta,
)

KEYWORD = 'keyword'


def _quote_ident(name):
    """Quote a SQL identifier. Only ingest-time-validated column names reach
    this function, but quoting keeps unusual CSV headers (spaces, brackets)
    working."""
    return '"' + str(name).replace('"', '""') + '"'


def _quote_literal(value):
    return "'" + str(value).replace("'", "''") + "'"


def _duckdb_type_to_field_type(col_type):
    """Map a DuckDB column type to the ES-flavoured type names the UI
    understands ('keyword' is the only categorical type; everything else
    lands in the continuous filter bucket)."""
    upper = str(col_type).upper()
    if upper == 'VARCHAR':
        return KEYWORD
    if 'INT' in upper or upper in ('HUGEINT', 'UBIGINT'):
        return 'long'
    if upper in ('FLOAT', 'DOUBLE') or upper.startswith('DECIMAL'):
        return 'float'
    if upper == 'BOOLEAN':
        return 'boolean'
    if 'DATE' in upper or 'TIME' in upper:
        return 'date'
    return 'float'


_NUMERIC_AGGS = ('min', 'max', 'avg', 'sum', 'boxplot')


class ParquetBackend(DashboardBackend):
    name = 'parquet'

    def __init__(self, datasets_dir):
        self.datasets_dir = os.path.realpath(datasets_dir)
        os.makedirs(self.datasets_dir, exist_ok=True)

    # -- dataset locations -------------------------------------------------

    def _parquet_file(self, name):
        return os.path.join(self.datasets_dir, name + '.parquet')

    def _meta_file(self, name):
        return meta_path(self.datasets_dir, name)

    # -- catalog -----------------------------------------------------------

    def list_datasets(self):
        names = []
        try:
            entries = os.listdir(self.datasets_dir)
        except OSError:
            return []
        for fname in entries:
            if fname.endswith('.parquet'):
                names.append(fname[:-len('.parquet')])
        return sorted(names)

    def dataset_exists(self, name):
        return os.path.isfile(self._parquet_file(name))

    def delete_dataset(self, name):
        for path in (self._parquet_file(name), self._meta_file(name)):
            if os.path.isfile(path):
                os.remove(path)

    # -- ingestion ---------------------------------------------------------

    # Explicit CSV parsing options. The sniffer only samples the first 20480
    # rows to detect the quote character, so CSVs whose quoted fields appear
    # late (e.g. quoted atlas names with commas) are misparsed with the naive
    # call. These options match the pandas to_csv convention PEACE outputs
    # use; delim stays auto-detected so the CLI metadata-join TSVs keep
    # working, and sample_size=-1 lets type detection scan the whole file.
    CSV_OPTIONS = "header=true, quote='\"', escape='\"', sample_size=-1"

    def create_dataset(self, name, csv_path):
        name = sanitize_dataset_name(name)
        out_path = self._parquet_file(name)
        con = duckdb.connect(database=':memory:')
        try:
            try:
                con.execute(
                    'CREATE TABLE dataset AS SELECT * FROM read_csv_auto(?, %s)'
                    % (self.CSV_OPTIONS,),
                    [csv_path],
                )
                con.execute('COPY dataset TO ? (FORMAT PARQUET)', [out_path])
                meta = self._build_meta(con, name, csv_path, out_path)
            except duckdb.Error as exc:
                # Surface as a 400 through the route error handler instead of
                # a 500, so the modal shows the real conversion/parsing error.
                raise ValueError(str(exc)) from exc
        finally:
            con.close()
        write_meta(self.datasets_dir, name, meta)
        return name

    def _build_meta(self, con, name, csv_path, out_path):
        fields = {}
        categorical = {}
        continuous = {}
        columns = [(row[0], row[1]) for row in con.execute('DESCRIBE dataset').fetchall()]
        for col, col_type in columns:
            fields[col] = _duckdb_type_to_field_type(col_type)
            if fields[col] == KEYWORD:
                rows = con.execute(
                    'SELECT DISTINCT %s FROM dataset WHERE %s IS NOT NULL '
                    'ORDER BY 1 LIMIT %d'
                    % (_quote_ident(col), _quote_ident(col), DISTINCT_CAP + 1)
                ).fetchall()
                categorical[col] = [row[0] for row in rows[:DISTINCT_CAP]]
            else:
                row = con.execute(
                    'SELECT MIN(%s), MAX(%s) FROM dataset'
                    % (_quote_ident(col), _quote_ident(col))
                ).fetchone()
                if row is not None and row[0] is not None:
                    continuous[col] = [row[0], row[1]]
        row_count = con.execute('SELECT COUNT(*) FROM dataset').fetchone()[0]
        return {
            'name': name,
            'backend': self.name,
            'row_count': row_count,
            'store_size': os.path.getsize(out_path),
            'updated': os.path.getmtime(out_path),
            'fields': fields,
            'categorical': categorical,
            'continuous': continuous,
            'source_path': csv_path,
            'source_size': os.path.getsize(csv_path),
            'dashboard': {},
        }

    def _rebuild_meta(self, name):
        """Recompute the meta sidecar from the Parquet file when it is missing
        (e.g. hand-placed files)."""
        con = duckdb.connect(database=':memory:')
        try:
            con.execute(
                'CREATE TABLE dataset AS SELECT * FROM read_parquet(?)',
                [self._parquet_file(name)],
            )
            meta = self._build_meta(con, name, '', self._parquet_file(name))
        finally:
            con.close()
        write_meta(self.datasets_dir, name, meta)
        return meta

    # -- schema ------------------------------------------------------------

    def get_field_types(self, name):
        meta = load_meta(self.datasets_dir, name)
        if meta is None:
            if not self.dataset_exists(name):
                raise UnknownDatasetError(name)
            meta = self._rebuild_meta(name)
        return dict(meta.get('fields') or {})

    def get_filter_values(self, name):
        meta = load_meta(self.datasets_dir, name)
        if meta is None:
            if not self.dataset_exists(name):
                raise UnknownDatasetError(name)
            meta = self._rebuild_meta(name)
        return dict(meta.get('categorical') or {}), dict(meta.get('continuous') or {})

    def get_meta(self, name):
        return load_meta(self.datasets_dir, name)

    def get_status(self, name):
        path = self._parquet_file(name)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        stat = os.stat(path)
        meta = load_meta(self.datasets_dir, name)
        row_count = meta.get('row_count') if meta else None
        if row_count is None:
            con = duckdb.connect(database=':memory:')
            try:
                row_count = con.execute(
                    'SELECT COUNT(*) FROM read_parquet(?)', [path]
                ).fetchone()[0]
            finally:
                con.close()
        return {
            'health': 'green',
            'status': 'open',
            'storage_size': format_byte_size(stat.st_size),
            'docs_count': str(row_count),
        }

    # -- querying ----------------------------------------------------------

    def query(self, spec):
        name = sanitize_dataset_name(spec.dataset)
        path = self._parquet_file(name)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        field_types = self.get_field_types(name)

        where = []
        params = []
        for f in spec.filters:
            if f.field not in field_types:
                raise UnknownDatasetError('Unknown field: %r' % (f.field,))
            col = _quote_ident(f.field)
            if isinstance(f, CategoricalFilter):
                values = [str(v) for v in f.values if str(v) != '']
                if not values:
                    # Empty selection means "no filter" (ES empty-should parity).
                    continue
                placeholders = ', '.join(['?'] * len(values))
                where.append('%s IN (%s)' % (col, placeholders))
                params.extend(values)
            else:
                if f.min is None and f.max is None:
                    continue
                where.append('%s BETWEEN ? AND ?' % col)
                params.extend([f.min, f.max])
        where_sql = (' WHERE ' + ' AND '.join(where)) if where else ''

        group_cols = list(spec.group_by)
        for gb in group_cols:
            if gb not in field_types:
                raise UnknownDatasetError('Unknown field: %r' % (gb,))
        if spec.n_field is not None and spec.n_field not in field_types:
            raise UnknownDatasetError('Unknown field: %r' % (spec.n_field,))

        select_parts = [_quote_ident(gb) for gb in group_cols]
        agg_meta = []  # (bucket key, kind, consumed column count)
        for agg in spec.aggregates:
            if agg.field not in field_types:
                raise UnknownDatasetError('Unknown field: %r' % (agg.field,))
            if agg.name in _NUMERIC_AGGS and field_types[agg.field] == KEYWORD:
                raise ValueError(
                    'Aggregate %r is not valid on the keyword field %r' % (agg.name, agg.field)
                )
            col = _quote_ident(agg.field)
            key = agg.name + '_' + agg.field
            if agg.name == 'boxplot':
                select_parts.extend([
                    'MIN(%s)' % col,
                    'QUANTILE_CONT(%s, 0.25)' % col,
                    'QUANTILE_CONT(%s, 0.5)' % col,
                    'QUANTILE_CONT(%s, 0.75)' % col,
                    'MAX(%s)' % col,
                ])
                agg_meta.append((key, 'boxplot', 5))
            else:
                expr = {
                    'min': 'MIN(%s)' % col,
                    'max': 'MAX(%s)' % col,
                    'avg': 'AVG(%s)' % col,
                    'sum': 'SUM(%s)' % col,
                    'value_count': 'COUNT(%s)' % col,
                    'cardinality': 'COUNT(DISTINCT %s)' % col,
                }[agg.name]
                select_parts.append(expr)
                agg_meta.append((key, 'value', 1))
        if spec.n_field is not None:
            select_parts.append('COUNT(DISTINCT %s)' % _quote_ident(spec.n_field))
            agg_meta.append(('N', 'value', 1))
        select_parts.append('COUNT(*)')
        agg_meta.append(('doc_count', 'raw', 1))

        sql = 'SELECT %s FROM read_parquet(%s)%s' % (
            ', '.join(select_parts), _quote_literal(path), where_sql)
        if group_cols:
            sql += ' GROUP BY %s' % ', '.join(_quote_ident(gb) for gb in group_cols)
            sql += ' ORDER BY %s' % ', '.join(_quote_ident(gb) for gb in group_cols)
        sql += ' LIMIT %d' % max(int(spec.size_cap or DISTINCT_CAP), 1)

        con = duckdb.connect(database=':memory:')
        try:
            rows = con.execute(sql, params).fetchall()
        finally:
            con.close()

        buckets = []
        for row in rows:
            idx = 0
            key = {}
            for gb in group_cols:
                key[gb] = row[idx]
                idx += 1
            bucket = {'key': key}
            for bucket_key, kind, width in agg_meta:
                if kind == 'boxplot':
                    bucket[bucket_key] = {
                        'min': row[idx],
                        'q1': row[idx + 1],
                        'q2': row[idx + 2],
                        'q3': row[idx + 3],
                        'max': row[idx + 4],
                    }
                elif kind == 'raw':
                    bucket[bucket_key] = row[idx]
                else:
                    bucket[bucket_key] = {'value': row[idx]}
                idx += width
            buckets.append(bucket)
        return buckets
