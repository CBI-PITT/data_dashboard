"""Storage backend abstraction for the PEACE data dashboard.

Every backend implements the same interface and returns query results in one
normalized shape: the ElasticSearch composite-aggregation bucket format the
dashboard UI was built against.

    {
      "key": {<group_by field>: value, ...},
      "doc_count": <int>,
      "<agg>_<field>": {"value": <number>},
      "boxplot_<field>": {"min": .., "max": .., "q1": .., "q2": .., "q3": ..},
      "N": {"value": <int>}            # only when the spec has an n_field
    }

The shared post-processing (density, N-normalization, error bars) runs on top
of that shape, so responses are identical regardless of the configured engine.
"""

import abc
import json
import os
from dataclasses import dataclass

from ..utils import sanitize_dataset_name

# Aggregation names the dashboard UI can request (Form.js pushes "boxplot" for
# non-keyword fields; the formFrame offers the rest).
AGGREGATES = ('min', 'max', 'avg', 'sum', 'value_count', 'cardinality', 'boxplot')

# Cap on distinct categorical values, mirroring the ES terms-agg size the
# original dashboard used (query_dsl.py sizeValue = 100000).
DISTINCT_CAP = 100000


@dataclass
class CategoricalFilter:
    field: str
    values: list


@dataclass
class ContinuousFilter:
    field: str
    min: float
    max: float


@dataclass
class Aggregate:
    name: str
    field: str


@dataclass
class QuerySpec:
    dataset: str
    field: str
    filters: list
    group_by: list
    aggregates: list
    n_field: str = None
    size_cap: int = DISTINCT_CAP
    owner: str = None


def build_identifier(name, owner):
    """Dataset identifier for the API: `owner/name`; ownerless/legacy
    datasets (owner None) use the plain name."""
    if owner:
        return '%s/%s' % (owner, name)
    return name


def parse_identifier(identifier):
    """Split an `owner/name` identifier. Returns (name, owner_or_None).
    An identifier without a slash addresses an ownerless/legacy dataset
    (admin-only access, enforced in the routes)."""
    identifier = str(identifier or '').strip()
    if '/' in identifier:
        owner, name = identifier.split('/', 1)
        if not owner or not name:
            raise UnknownFieldError('Invalid dataset identifier: %r' % (identifier,))
        return name, owner
    if not identifier:
        raise UnknownFieldError('Invalid dataset identifier: %r' % (identifier,))
    return identifier, None


class DashboardBackendError(Exception):
    """Base error for backend failures that map to a 400 response."""


class UnknownDatasetError(DashboardBackendError):
    pass


class UnknownFieldError(DashboardBackendError):
    pass


def ensure_within(base_dir, *path_parts):
    """Resolve a dataset file path under base_dir and refuse anything that
    would land outside it, before the caller touches the filesystem.

    Mirrors the repo's containment pattern (utils.csv_within_allowed_roots):
    explicit '..' segments (and null/newline control characters) are rejected
    before resolution, realpath resolves symlinks so a link pointing outside
    base_dir is caught, and the resolved path must be strictly inside.
    Raises PermissionError (routes map it to a 403)."""
    parts = [str(part) for part in path_parts]
    joined = os.path.join(base_dir, *parts)
    if '\x00' in joined or '\n' in joined or '\r' in joined:
        raise PermissionError(
            'Dataset path contains control characters: %r' % (joined,))
    for part in joined.replace('\\', '/').split(os.sep):
        if part == '..':
            raise PermissionError(
                'Dataset path must stay inside the dashboard folder: %r' % (joined,))
    real = os.path.realpath(joined)
    base = os.path.realpath(base_dir)
    if real != base and not real.startswith(base.rstrip(os.sep) + os.sep):
        raise PermissionError(
            'Dataset path must stay inside the dashboard folder: %r' % (joined,))
    return real


def meta_path(datasets_dir, name):
    return os.path.join(datasets_dir, name + '.dashboard_meta.json')


def load_meta(datasets_dir, name):
    """Load the sidecar meta JSON for a dataset; None when absent."""
    path = meta_path(datasets_dir, name)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, 'r') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def write_meta(datasets_dir, name, meta):
    path = meta_path(datasets_dir, name)
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w') as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)
    os.replace(tmp_path, path)


def format_byte_size(num_bytes):
    """Human-readable size in the style of the ES cat API."""
    size = float(num_bytes or 0)
    for unit in ('b', 'kb', 'mb', 'gb', 'tb'):
        if size < 1024.0 or unit == 'tb':
            if unit in ('b', 'kb'):
                return '%d%s' % (int(size), unit)
            return '%.1f%s' % (size, unit)
        size /= 1024.0


def same_bound(a, b):
    """True when two numeric bounds match (the meta range round-trips through
    JSON floats, so compare with a small relative tolerance). Used by both
    backends to treat untouched full-range sliders as no filter."""
    if a is None or b is None:
        return a is None and b is None
    a = float(a)
    b = float(b)
    return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))


class DashboardBackend(abc.ABC):
    """Interface every dashboard storage backend implements.

    Datasets are owned by a user (owner=None addresses ownerless/legacy
    datasets, which only admins may access — enforced in the routes). Every
    method takes an explicit owner; identifiers combine as `owner/name`.
    """

    name = None

    @abc.abstractmethod
    def list_datasets(self, owner=None):
        """Dataset identifiers visible to the given user. owner=None (admin)
        lists every user's datasets plus ownerless/legacy ones."""

    @abc.abstractmethod
    def dataset_exists(self, name, owner=None):
        """True when the dataset name is known to this backend."""

    @abc.abstractmethod
    def create_dataset(self, name, csv_path, owner=None):
        """Ingest a CSV file as a NEW dataset (never overwrites; name
        collisions get a _2, _3... suffix). Returns the final dataset name."""

    @abc.abstractmethod
    def delete_dataset(self, name, owner=None):
        """Remove a dataset and its meta."""

    @abc.abstractmethod
    def rename_dataset(self, name, new_name, owner=None):
        """Rename a dataset. Raises ValueError for collisions."""

    @abc.abstractmethod
    def merge_datasets(self, sources, new_name, owner=None):
        """Stack several datasets into one new dataset. sources is a list of
        (name, owner, fields_dict) where fields_dict adds constant columns so
        the sources are comparable via group-by. Each source is additionally
        tagged with a `sample` column. Sources are not modified."""

    @abc.abstractmethod
    def get_field_types(self, name, owner=None):
        """{field: type} with 'keyword' for categorical (string) fields."""

    @abc.abstractmethod
    def get_filter_values(self, name, owner=None):
        """(categorical, continuous) dicts for the query form.

        categorical: {field: [distinct values]}
        continuous:  {field: [min, max]}
        """

    @abc.abstractmethod
    def get_status(self, name, owner=None):
        """{health, status, storage_size, docs_count} for the dataset card."""

    @abc.abstractmethod
    def get_meta(self, name, owner=None):
        """Sidecar meta dict (schema cache + dashboard parameters); None when
        the dataset has no meta."""

    @abc.abstractmethod
    def query(self, spec):
        """Run a QuerySpec, returning normalized bucket dicts. spec.owner
        scopes the dataset."""

    @abc.abstractmethod
    def get_rows(self, name, offset=0, limit=100, owner=None, filters=None):
        """Raw rows for the spreadsheet view, progressively: {columns: [names
        in row order], rows: [[...]], total: <int>} for one page
        (offset/limit). filters is a list of CategoricalFilter/
        ContinuousFilter (empty = no filter). spec.owner scopes the dataset."""

    def validate_fields(self, name, fields, owner=None):
        """Raise UnknownFieldError for any field the dataset does not have."""
        known = self.get_field_types(name, owner)
        for field in fields:
            if field is not None and field not in known:
                raise UnknownFieldError('Unknown field: %r' % (field,))
        return known
