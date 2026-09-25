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


class DashboardBackendError(Exception):
    """Base error for backend failures that map to a 400 response."""


class UnknownDatasetError(DashboardBackendError):
    pass


class UnknownFieldError(DashboardBackendError):
    pass


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


class DashboardBackend(abc.ABC):
    """Interface every dashboard storage backend implements."""

    name = None

    @abc.abstractmethod
    def list_datasets(self):
        """Sorted list of dataset (index) names."""

    @abc.abstractmethod
    def dataset_exists(self, name):
        """True when the dataset name is known to this backend."""

    @abc.abstractmethod
    def create_dataset(self, name, csv_path):
        """Ingest a CSV file as a new (or replacement) dataset. Returns the
        sanitized dataset name."""

    @abc.abstractmethod
    def delete_dataset(self, name):
        """Remove a dataset and its meta."""

    @abc.abstractmethod
    def get_field_types(self, name):
        """{field: type} with 'keyword' for categorical (string) fields."""

    @abc.abstractmethod
    def get_filter_values(self, name):
        """(categorical, continuous) dicts for the query form.

        categorical: {field: [distinct values]}
        continuous:  {field: [min, max]}
        """

    @abc.abstractmethod
    def get_status(self, name):
        """{health, status, storage_size, docs_count} for the dataset card."""

    @abc.abstractmethod
    def get_meta(self, name):
        """Sidecar meta dict (schema cache + dashboard parameters); None when
        the dataset has no meta."""

    @abc.abstractmethod
    def query(self, spec):
        """Run a QuerySpec, returning normalized bucket dicts."""

    def validate_fields(self, name, fields):
        """Raise UnknownFieldError for any field the dataset does not have."""
        known = self.get_field_types(name)
        for field in fields:
            if field is not None and field not in known:
                raise UnknownFieldError('Unknown field: %r' % (field,))
        return known
