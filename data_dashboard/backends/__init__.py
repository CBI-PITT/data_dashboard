"""Backend selection for the PEACE data dashboard.

Backends are imported lazily inside get_backend() so a parquet-only
deployment does not need the elasticsearch package installed (and vice
versa). Adding a future engine (e.g. ClickHouse) means: subclass
DashboardBackend, give it a unique `name`, and add it to the factory below.
"""

from .base import (
    AGGREGATES,
    Aggregate,
    CategoricalFilter,
    ContinuousFilter,
    DashboardBackend,
    DashboardBackendError,
    DISTINCT_CAP,
    QuerySpec,
    UnknownDatasetError,
    UnknownFieldError,
    format_byte_size,
    load_meta,
    meta_path,
    write_meta,
)

__all__ = [
    'AGGREGATES', 'Aggregate', 'CategoricalFilter', 'ContinuousFilter',
    'DashboardBackend', 'DashboardBackendError', 'DISTINCT_CAP', 'QuerySpec',
    'UnknownDatasetError', 'UnknownFieldError', 'format_byte_size',
    'load_meta', 'meta_path', 'write_meta', 'get_backend',
]


def get_backend(settings):
    """Build the storage backend named in [dashboard] backend."""
    backend_name = str(settings.get('dashboard', 'backend', fallback='parquet')).strip().lower()
    datasets_dir = str(settings.get('dashboard', 'datasets_dir', fallback='')).strip()
    if not datasets_dir:
        raise ValueError('[dashboard] datasets_dir is not configured in settings.ini')

    if backend_name == 'parquet':
        from .parquet import ParquetBackend
        return ParquetBackend(datasets_dir)

    if backend_name == 'elasticsearch':
        from .elasticsearch import ElasticsearchBackend
        return ElasticsearchBackend(
            datasets_dir,
            es_server=settings.get(
                'backend_elasticsearch', 'es_server', fallback='http://localhost:9200'),
            index_shards=settings.getint(
                'backend_elasticsearch', 'index_shards', fallback=1),
        )

    raise ValueError(
        "Unknown dashboard backend: %r (expected 'parquet' or 'elasticsearch')"
        % (backend_name,)
    )
