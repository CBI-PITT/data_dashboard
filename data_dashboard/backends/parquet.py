"""DuckDB + Parquet storage backend (the default, service-free engine).

Datasets are owned by a user: one folder per user under the configured
datasets_dir, holding `<name>.parquet` + `<name>.dashboard_meta.json`
(schema cache + dashboard parameters + samples registry). Ownerless/legacy
files at the root remain readable (admins only, enforced in the routes).
Queries run as SQL aggregates over the Parquet file.
"""

import datetime
import decimal
import os
import re

import duckdb

from ..utils import sanitize_dataset_name
from .base import (
    CategoricalFilter,
    DashboardBackend,
    DISTINCT_CAP,
    UnknownDatasetError,
    build_identifier,
    ensure_within,
    format_byte_size,
    load_meta,
    meta_path,
    same_bound,
    write_meta,
)

KEYWORD = 'keyword'
SAMPLE_COLUMN = 'sample'
COLUMN_STATS_VALUE_CAP = 100


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


def _json_safe(value):
    """DuckDB returns datetime/Decimal objects that the default Flask JSON
    encoder cannot serialize; string them (numbers stay native)."""
    if isinstance(value, (datetime.date, datetime.time, decimal.Decimal)):
        return str(value)
    return value


class ParquetBackend(DashboardBackend):
    name = 'parquet'

    # Explicit CSV parsing options. The sniffer only samples the first 20480
    # rows to detect the quote character, so CSVs whose quoted fields appear
    # late (e.g. quoted atlas names with commas) are misparsed with the naive
    # call. These options match the pandas to_csv convention PEACE outputs
    # use; delim stays auto-detected so the CLI metadata-join TSVs keep
    # working, and sample_size=-1 lets type detection scan the whole file.
    CSV_OPTIONS = "header=true, quote='\"', escape='\"', sample_size=-1"

    def __init__(self, datasets_dir):
        self.datasets_dir = os.path.realpath(datasets_dir)
        os.makedirs(self.datasets_dir, exist_ok=True)

    # -- dataset locations -------------------------------------------------

    def _user_dir(self, owner):
        return os.path.join(self.datasets_dir, owner) if owner else self.datasets_dir

    def _parquet_file(self, name, owner=None):
        return os.path.join(self._user_dir(owner), name + '.parquet')

    def _meta_file(self, name, owner=None):
        return meta_path(self._user_dir(owner), name)

    def _unique_name(self, name, owner):
        """First free name: name, name_2, name_3... Adds never overwrite."""
        if not os.path.isfile(self._parquet_file(name, owner)):
            return name
        match = re.match(r'^(.*)_(\d+)$', name)
        if match:
            base = match.group(1)
            counter = int(match.group(2))
        else:
            base, counter = name, 1
        while True:
            counter += 1
            candidate = '%s_%d' % (base, counter)
            if not os.path.isfile(self._parquet_file(candidate, owner)):
                return candidate

    # -- catalog -----------------------------------------------------------

    def list_datasets(self, owner=None):
        """owner given -> that user's datasets (`owner/name` identifiers);
        owner None (admin) -> every user folder plus root-level ownerless
        files (plain-name identifiers)."""
        identifiers = []
        if owner:
            return [build_identifier(name, owner) for name in self._folder_datasets(self._user_dir(owner))]
        for entry in sorted(os.listdir(self.datasets_dir)):
            path = os.path.join(self.datasets_dir, entry)
            if os.path.isdir(path):
                for name in self._folder_datasets(path):
                    identifiers.append(build_identifier(name, entry))
            elif entry.endswith('.parquet'):
                identifiers.append(entry[:-len('.parquet')])
        return sorted(identifiers)

    @staticmethod
    def _folder_datasets(folder):
        names = []
        try:
            entries = os.listdir(folder)
        except OSError:
            return []
        for fname in entries:
            if fname.endswith('.parquet'):
                names.append(fname[:-len('.parquet')])
        return sorted(names)

    def dataset_exists(self, name, owner=None):
        return os.path.isfile(self._parquet_file(name, owner))

    def delete_dataset(self, name, owner=None):
        # Containment check BEFORE any removal: both paths must resolve
        # inside the dashboard folder (catches '..' names and symlink
        # escapes), so nothing outside it can ever be deleted.
        parquet_path = ensure_within(self.datasets_dir, self._parquet_file(name, owner))
        meta_file = ensure_within(self.datasets_dir, self._meta_file(name, owner))
        for path in (parquet_path, meta_file):
            if os.path.isfile(path):
                os.remove(path)

    def rename_dataset(self, name, new_name, owner=None):
        new_name = sanitize_dataset_name(new_name)
        src_parquet = self._parquet_file(name, owner)
        if not os.path.isfile(src_parquet):
            raise UnknownDatasetError(name)
        dst_parquet = self._parquet_file(new_name, owner)
        if os.path.isfile(dst_parquet):
            raise ValueError("A dataset named %r already exists" % (new_name,))
        os.rename(src_parquet, dst_parquet)
        src_meta = self._meta_file(name, owner)
        dst_meta = self._meta_file(new_name, owner)
        meta = load_meta(self._user_dir(owner), name)
        if os.path.isfile(src_meta):
            os.rename(src_meta, dst_meta)
        if meta is not None:
            meta['name'] = new_name
            write_meta(self._user_dir(owner), new_name, meta)
        return new_name

    # -- ingestion ---------------------------------------------------------

    def create_dataset(self, name, csv_path, owner=None):
        """Ingest as a NEW dataset under the owner's folder; never overwrites
        (collisions get a _2, _3... suffix). Returns the final name."""
        name = self._unique_name(sanitize_dataset_name(name), owner)
        out_path = self._parquet_file(name, owner)
        os.makedirs(self._user_dir(owner), exist_ok=True)
        con = duckdb.connect(database=':memory:')
        try:
            try:
                con.execute(
                    'CREATE TABLE dataset AS SELECT * FROM read_csv_auto(?, %s)'
                    % (self.CSV_OPTIONS,),
                    [csv_path],
                )
                con.execute('COPY dataset TO ? (FORMAT PARQUET)', [out_path])
                meta = self._build_meta(con, name, owner, out_path, csv_path)
            except duckdb.Error as exc:
                # Surface as a 400 through the route error handler instead of
                # a 500, so the modal shows the real conversion/parsing error.
                raise ValueError(str(exc)) from exc
        finally:
            con.close()
        write_meta(self._user_dir(owner), name, meta)
        return name

    def _build_meta(self, con, name, owner, out_path, csv_path='', samples=None):
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
                    # Dates serialize as strings in the sidecar (raw
                    # datetime.date would crash json.dump).
                    continuous[col] = [_json_safe(row[0]), _json_safe(row[1])]
        row_count = con.execute('SELECT COUNT(*) FROM dataset').fetchone()[0]
        return {
            'name': name,
            'owner': owner,
            'backend': self.name,
            'row_count': row_count,
            'store_size': os.path.getsize(out_path),
            'updated': os.path.getmtime(out_path),
            'fields': fields,
            'categorical': categorical,
            'continuous': continuous,
            'source_path': csv_path,
            'source_size': os.path.getsize(csv_path) if csv_path and os.path.isfile(csv_path) else None,
            'samples': samples or [],
            'dashboard': {},
        }

    def _rebuild_meta(self, name, owner=None):
        """Recompute the meta sidecar from the Parquet file when it is missing
        (e.g. hand-placed files)."""
        con = duckdb.connect(database=':memory:')
        try:
            con.execute(
                'CREATE TABLE dataset AS SELECT * FROM read_parquet(?)',
                [self._parquet_file(name, owner)],
            )
            meta = self._build_meta(con, name, owner, self._parquet_file(name, owner))
        finally:
            con.close()
        write_meta(self._user_dir(owner), name, meta)
        return meta

    # -- merging -----------------------------------------------------------

    def merge_datasets(self, sources, new_name, owner=None):
        """Stack several datasets into one new dataset under the owner's
        folder. sources is a list of (name, owner, fields_dict); each source
        gets a `sample` column (its dataset name) plus the caller's fields as
        constant VARCHAR columns. Sources are not modified."""
        new_name = self._unique_name(sanitize_dataset_name(new_name), owner)
        prepared = []
        for src_name, src_owner, fields in sources:
            src_path = self._parquet_file(src_name, src_owner)
            if not os.path.isfile(src_path):
                raise UnknownDatasetError(src_name)
            prepared.append((src_name, src_path, dict(fields or {})))
        if not prepared:
            raise ValueError('No datasets to merge')

        out_path = self._parquet_file(new_name, owner)
        os.makedirs(self._user_dir(owner), exist_ok=True)
        samples = []
        con = duckdb.connect(database=':memory:')
        try:
            try:
                for idx, (src_name, src_path, fields) in enumerate(prepared):
                    # DDL (CREATE VIEW) cannot use prepared parameters, so the
                    # constants are inlined as escaped literals: field keys are
                    # quoted identifiers, values escaped string literals.
                    extra = ['%s AS %s' % (
                        _quote_literal(src_name), _quote_ident(SAMPLE_COLUMN))]
                    for key in sorted(fields):
                        extra.append('%s AS %s' % (
                            _quote_literal(fields[key]), _quote_ident(key)))
                    view_sql = 'SELECT *, %s FROM read_parquet(%s)' % (
                        ', '.join(extra), _quote_literal(src_path))
                    con.execute('CREATE VIEW s%d AS %s' % (idx, view_sql))
                    rows = con.execute('SELECT COUNT(*) FROM s%d' % idx).fetchone()[0]
                    samples.append({
                        'name': src_name,
                        'owner': src_owner,
                        'fields': fields,
                        'source_path': src_path,
                        'rows': rows,
                    })
                union = ' UNION ALL BY NAME '.join(
                    'SELECT * FROM s%d' % idx for idx in range(len(prepared)))
                con.execute('CREATE TABLE dataset AS %s' % union)
                con.execute('COPY dataset TO ? (FORMAT PARQUET)', [out_path])
                meta = self._build_meta(
                    con, new_name, owner, out_path, samples=samples)
            except duckdb.Error as exc:
                raise ValueError(str(exc)) from exc
        finally:
            con.close()
        write_meta(self._user_dir(owner), new_name, meta)
        return new_name

    # -- schema ------------------------------------------------------------

    def get_field_types(self, name, owner=None):
        meta = load_meta(self._user_dir(owner), name)
        if meta is None:
            if not self.dataset_exists(name, owner):
                raise UnknownDatasetError(name)
            meta = self._rebuild_meta(name, owner)
        return dict(meta.get('fields') or {})

    def get_filter_values(self, name, owner=None):
        meta = load_meta(self._user_dir(owner), name)
        if meta is None:
            if not self.dataset_exists(name, owner):
                raise UnknownDatasetError(name)
            meta = self._rebuild_meta(name, owner)
        return dict(meta.get('categorical') or {}), dict(meta.get('continuous') or {})

    def get_meta(self, name, owner=None):
        return load_meta(self._user_dir(owner), name)

    def get_status(self, name, owner=None):
        path = self._parquet_file(name, owner)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        stat = os.stat(path)
        meta = load_meta(self._user_dir(owner), name)
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
        path = self._parquet_file(name, spec.owner)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        field_types = self.get_field_types(name, spec.owner)

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

        # ES composite terms sources exclude documents with a missing group
        # value; DuckDB's GROUP BY would keep a NULL group, so exclude them.
        null_exclusions = ['%s IS NOT NULL' % _quote_ident(gb) for gb in group_cols]
        if null_exclusions:
            where_sql = (' WHERE ' + ' AND '.join(where + null_exclusions)) if (where or null_exclusions) else ''

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

    # -- spreadsheet rows ---------------------------------------------------

    def get_rows(self, name, offset=0, limit=100, owner=None, filters=None):
        """One page of raw rows for the spreadsheet view. Continuous filters
        that still carry the meta's full min/max range (untouched sliders)
        are treated as no filter so the unfiltered view keeps NULL rows."""
        name = sanitize_dataset_name(name)
        path = self._parquet_file(name, owner)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        offset = max(int(offset), 0)
        limit = max(int(limit), 1)
        field_types = self.get_field_types(name, owner)
        meta = load_meta(self._user_dir(owner), name) or {}
        full_ranges = dict(meta.get('continuous') or {})

        where = []
        params = []
        for f in filters or []:
            if f.field not in field_types:
                raise UnknownDatasetError('Unknown field: %r' % (f.field,))
            col = _quote_ident(f.field)
            if isinstance(f, CategoricalFilter):
                values = [str(v) for v in f.values if str(v) != '']
                if not values:
                    # Empty selection means "no filter" (query() parity).
                    continue
                placeholders = ', '.join(['?'] * len(values))
                where.append('%s IN (%s)' % (col, placeholders))
                params.extend(values)
            else:
                if f.min is None and f.max is None:
                    continue
                full = full_ranges.get(f.field)
                if (isinstance(full, (list, tuple)) and len(full) == 2 and
                        same_bound(f.min, full[0]) and same_bound(f.max, full[1])):
                    continue
                where.append('%s BETWEEN ? AND ?' % col)
                params.extend([f.min, f.max])
        where_sql = (' WHERE ' + ' AND '.join(where)) if where else ''
        from_sql = 'FROM read_parquet(%s)%s' % (_quote_literal(path), where_sql)

        con = duckdb.connect(database=':memory:')
        try:
            if where:
                total = con.execute(
                    'SELECT COUNT(*) %s' % from_sql, params).fetchone()[0]
            else:
                total = meta.get('row_count')
                if total is None:
                    total = con.execute(
                        'SELECT COUNT(*) %s' % from_sql, params).fetchone()[0]
            columns = [row[0] for row in con.execute(
                'DESCRIBE SELECT * %s' % from_sql, params).fetchall()]
            rows = con.execute(
                'SELECT * %s LIMIT %d OFFSET %d' % (from_sql, limit, offset),
                params).fetchall()
        finally:
            con.close()
        return {
            'columns': columns,
            'rows': [[_json_safe(value) for value in row] for row in rows],
            'total': int(total),
        }

    # -- column stats (numiqo-style picker) ---------------------------------

    def get_column_stats(self, name, column, owner=None):
        """Descriptive stats for one column. Categorical: frequency table
        (top COLUMN_STATS_VALUE_CAP values by occurrences, fraction relative
        to the non-null values). Numeric: min/max/mean/median/quantiles/std.
        Date: min/max/count only (quantiles/std are undefined for dates)."""
        name = sanitize_dataset_name(name)
        path = self._parquet_file(name, owner)
        if not os.path.isfile(path):
            raise UnknownDatasetError(name)
        field_types = self.get_field_types(name, owner)
        if column not in field_types:
            raise UnknownDatasetError('Unknown field: %r' % (column,))
        ftype = field_types[column]
        col = _quote_ident(column)
        from_sql = 'FROM read_parquet(?)'

        def _number(value):
            if value is None:
                return None
            if isinstance(value, decimal.Decimal):
                return float(value)
            return value

        con = duckdb.connect(database=':memory:')
        try:
            if ftype == KEYWORD or ftype == 'boolean':
                total, non_null, distinct = con.execute(
                    'SELECT COUNT(*), COUNT(%s), COUNT(DISTINCT %s) %s'
                    % (col, col, from_sql), [path]).fetchone()
                rows = con.execute(
                    'SELECT %s, COUNT(*) %s WHERE %s IS NOT NULL '
                    'GROUP BY 1 ORDER BY 2 DESC, 1 ASC LIMIT %d'
                    % (col, from_sql, col, COLUMN_STATS_VALUE_CAP),
                    [path]).fetchall()
                values = [
                    {
                        'value': _json_safe(value),
                        'count': int(count),
                        'fraction': (float(count) / float(non_null)) if non_null else 0.0,
                    }
                    for value, count in rows
                ]
                return {
                    'column': column,
                    'type': ftype,
                    'kind': 'categorical',
                    'values': values,
                    'distinct': int(distinct),
                    'missing': int(total) - int(non_null),
                    'total': int(total),
                    'truncated': int(distinct) > len(values),
                }
            if ftype == 'date':
                low, high, valid, total = con.execute(
                    'SELECT MIN(%s), MAX(%s), COUNT(%s), COUNT(*) %s'
                    % (col, col, col, from_sql), [path]).fetchone()
                return {
                    'column': column,
                    'type': ftype,
                    'kind': 'date',
                    'stats': {
                        'min': _json_safe(low),
                        'max': _json_safe(high),
                        'valid': int(valid),
                        'missing': int(total) - int(valid),
                        'total': int(total),
                    },
                }
            low, high, mean, median, q25, q75, std, valid, total = con.execute(
                'SELECT MIN(%s), MAX(%s), AVG(%s), MEDIAN(%s), '
                'QUANTILE_CONT(%s, 0.25), QUANTILE_CONT(%s, 0.75), '
                'STDDEV_SAMP(%s), COUNT(%s), COUNT(*) %s'
                % (col, col, col, col, col, col, col, col, from_sql),
                [path]).fetchone()
            return {
                'column': column,
                'type': ftype,
                'kind': 'numeric',
                'stats': {
                    'min': _number(low),
                    'max': _number(high),
                    'mean': _number(mean),
                    'median': _number(median),
                    'q25': _number(q25),
                    'q75': _number(q75),
                    'std': _number(std),
                    'valid': int(valid),
                    'missing': int(total) - int(valid),
                    'total': int(total),
                },
            }
        finally:
            con.close()
