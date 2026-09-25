#!/usr/bin/env python3
"""CLI importer for the PEACE data dashboard.

Ingests CSV files into the configured dashboard backend:

    python3 import_csv.py /path/to/cells.csv
    python3 import_csv.py --backend parquet job_*.csv
    python3 import_csv.py --metadata metadata.csv cells.csv \
        --atlas-acronym-col atlas_structure_acronym --n-col metadata \
        --density-agg value_count --atlas-resolution 25

The file browser's "Add to dashboard" button covers single CSVs; this CLI adds
the klimstra-style metadata join and per-dataset dashboard parameters
(atlas density / N normalization) on top. With --backend, datasets can be
copied into the other storage engine (e.g. elasticsearch when datasets grow).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd

from data_dashboard.backends import get_backend
from data_dashboard.backends.base import write_meta
from data_dashboard.utils import get_config, sanitize_dataset_name


def join_with_metadata(cells, metadata, metadata_key='id', cells_key='metadata',
                       metadata_shift=0):
    """Port of es_importing.join_with_metadata: join a per-brain metadata CSV
    (file_path, treatment, time_point, ...) with a cells CSV on the metadata
    id column. Writes a TSV next to the cells file and returns its path."""
    df_cells = pd.read_csv(cells)
    df_cells = df_cells.rename(columns={'uuid': 'uuid_cell'})
    df_metadata = pd.read_csv(metadata)
    df_metadata = df_metadata.rename(columns={'uuid': 'uuid_brain'})
    df_merged = pd.merge(
        left=df_metadata,
        right=df_cells,
        how='inner',
        left_on=metadata_key,
        right_on=cells_key,
    ).drop([metadata_key], axis=1)
    if metadata_shift:
        df_merged[cells_key] = df_merged[cells_key] + metadata_shift
    joint_file = cells[:-len('.csv')] + '_with_metadata.csv' if cells.lower().endswith('.csv') else cells + '_with_metadata.csv'
    df_merged.to_csv(joint_file, sep='\t', index=False)
    return joint_file


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('csv_files', nargs='+', help='cells CSV files to ingest')
    parser.add_argument('--backend', choices=['parquet', 'elasticsearch'],
                        help='storage backend (default: [dashboard] backend in settings.ini)')
    parser.add_argument('--name', help='dataset name for a single CSV (default: file basename)')
    parser.add_argument('--metadata',
                        help='optional per-brain metadata CSV joined with each cells CSV')
    parser.add_argument('--metadata-key', default='id',
                        help='join column in the metadata CSV (default: id)')
    parser.add_argument('--cells-key', default='metadata',
                        help='join column in the cells CSV (default: metadata)')
    parser.add_argument('--metadata-shift', type=int, default=0,
                        help='offset added to the join ids to keep them unique across brains')
    parser.add_argument('--atlas-acronym-col',
                        help='column holding atlas structure acronyms, enables density')
    parser.add_argument('--n-col', help='column whose cardinality is the N normalization')
    parser.add_argument('--density-agg',
                        choices=['count', 'value_count', 'sum', 'avg', 'cardinality'],
                        help='aggregation used for the density calculation')
    parser.add_argument('--atlas-resolution', type=int, choices=[10, 25],
                        help='atlas resolution (um) used for density volumes')
    parser.add_argument('--dry-run', action='store_true',
                        help='print what would be ingested without ingesting')
    args = parser.parse_args(argv)

    settings = get_config()
    if args.backend:
        settings.set('dashboard', 'backend', args.backend)
    backend = get_backend(settings)

    if args.name and len(args.csv_files) > 1:
        parser.error('--name only works with a single CSV file')

    dashboard_params = {
        'aggregation_condition': args.density_agg,
        'atlas_structure_acronym_column_name': args.atlas_acronym_col,
        'metadata_calculation_name': args.n_col,
        'atlas_resolution_micrometer': args.atlas_resolution,
    }
    dashboard_params = {k: v for k, v in dashboard_params.items() if v is not None}

    for csv_path in args.csv_files:
        if not os.path.isfile(csv_path):
            print('ERROR: no such file: %s' % csv_path)
            continue
        name = sanitize_dataset_name(args.name or os.path.basename(csv_path))
        source = csv_path
        if args.metadata:
            source = join_with_metadata(
                csv_path, args.metadata,
                metadata_key=args.metadata_key,
                cells_key=args.cells_key,
                metadata_shift=args.metadata_shift,
            )
        if args.dry_run:
            print('would ingest %s -> %s [%s] as %s' % (source, backend.name, backend.datasets_dir, name))
            continue
        print('Ingesting %s -> %s [%s] as %s' % (source, backend.name, backend.datasets_dir, name))
        backend.create_dataset(name, source)
        if dashboard_params:
            meta = backend.get_meta(name) or {}
            meta.setdefault('dashboard', {}).update(dashboard_params)
            write_meta(backend.datasets_dir, name, meta)
        print('Done: %s' % name)

    print('Datasets now available: %s' % ', '.join(backend.list_datasets()))


if __name__ == '__main__':
    main()
