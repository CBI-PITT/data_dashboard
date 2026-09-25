# data_dashboard

PEACE data dashboard: visualizes and explores PEACE pipeline results as plots
(line, bar, pie, box, area, word cloud, ...). Integrated into the PEACE Flask
app as a blueprint with pluggable storage backends — **no ElasticSearch,
MySQL or Kibana required by default**.

## Architecture

- `data_dashboard/` — python package (pip-installable blueprint, same pattern
  as `flask_file_browser`)
  - `backends/` — storage backends behind one `DashboardBackend` interface:
    - `parquet.py` (default): DuckDB + one Parquet file per dataset on disk,
      no services to deploy
    - `elasticsearch.py`: ports the original ES query/ingest code (for very
      large datasets); the `elasticsearch` package is imported lazily
  - `query_form.py` / `postprocess.py` — shared form-JSON → QuerySpec parsing
    and density / N-normalization / error-bar post-processing (identical
    responses from every backend)
  - `routes.py` — `init_blueprint(app, prefix='/dashboard')` factory: JSON API
    + the built React single-page app
  - `web/` — built React app, served by the blueprint
- `dashboard/` — React (CRA) source. Pages trimmed to Dashboard + IndexInfo;
  same-origin API calls (no CORS); `homepage: /dashboard`.
- `import_csv.py` — CLI importer (`--backend`, klimstra-style metadata join,
  dashboard parameters)
- `flask-server/`, `es_importing/` — legacy reference code (no longer used)

## Install

From the PEACE flask env:

    pip install duckdb
    pip install -e ./data_dashboard

## Frontend build (one time, requires Node 16+)

    ./build_frontend.sh

Builds `dashboard/` and copies the output into `data_dashboard/web/`. The
server does not need node. Until the build runs, `/dashboard` serves a
fallback page (the JSON API is unaffected).

## Configure

Edit `data_dashboard/settings.ini` (inside the package):

- `[dashboard] enabled` — blueprint on/off (PEACE navbar link hidden when off)
- `[dashboard] backend` — `parquet` (default) or `elasticsearch`
- `[dashboard] datasets_dir` — where datasets are stored
  (`<name>.parquet` + `<name>.dashboard_meta.json` per dataset)
- `[backend_elasticsearch] es_server` — ES instance to use when
  `backend = elasticsearch` (old `klimstra*`/`cebra*` indices stay readable)

Switching backends = change one line + restart. Datasets do not migrate
automatically; re-ingest with `./import_csv.py --backend <other>`.

## Use

1. Browse CSVs in the PEACE File Browser and click **Add to dashboard** on any
   `.csv` (button visible only when the dashboard is enabled). The CSV is
   ingested into the configured backend.
2. Open `/dashboard`, pick a dataset, build a query, pick a plot.
3. Or ingest from the CLI:

       python3 import_csv.py /path/to/cells.csv
       python3 import_csv.py --metadata metadata.csv job_*.csv \
           --atlas-acronym-col atlas_structure_acronym --n-col metadata \
           --density-agg value_count --atlas-resolution 25

## API

- `GET /dashboard/api/indices`
- `GET /dashboard/api/index_choosen/<name>` (+ `/meta/`, `/current_status/`)
- `POST /dashboard/api/query`, `POST /dashboard/api/query_paras`
- `GET /dashboard/indexInfo`
- `POST /dashboard/api/add_csv` (login required; the CSV must live inside the
  file browser's browsable roots)
- `GET /dashboard/` (React SPA)

The query JSON contract is unchanged from the original dashboard, so the
React code works against either backend.

## Legacy

The original ElasticSearch + MySQL + Kibana stack lives in `flask-server/`
and `es_importing/` for reference. `ElasticsearchBackend` ports the relevant
query logic; point `[backend_elasticsearch] es_server` at an existing ES
instance to keep old indices visible.
