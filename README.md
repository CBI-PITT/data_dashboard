# data_dashboard

PEACE data dashboard: visualizes and explores PEACE pipeline results as plots
(line, bar, pie, box, area, word cloud, ...). Integrated into the PEACE Flask
app as a blueprint with pluggable storage backends — **no ElasticSearch,
MySQL or Kibana required by default**.

## Ownership and privacy

Datasets are owned by a user: one folder per user under `datasets_dir`
(`<datasets_dir>/<username>/<name>.parquet`). **Every dashboard route is
login-protected** — users only see and access their own datasets; `CBI_Admin`
(configurable via `[dashboard] admins`) sees everything, including
ownerless/legacy datasets. Identifiers combine as `owner/name`.

Dataset management in the dashboard UI:

- **Add** — the file-browser "Add to dashboard" button always creates a NEW
  dataset (name collisions get a `_2`, `_3`... suffix, never overwrite).
- **Rename** — pencil button next to the Index picker.
- **Merge** — pick 2+ of your datasets, assign per-dataset fields (e.g.
  `treatment=ctrl`), get one new dataset with a `sample` column so group-by
  compares the sources on one plot. Sources stay untouched.

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
  same-origin API calls (no CORS); `homepage: /dashboard`. The navbar (both
  pages) shows the logged-in user via `/api/whoami` plus Home, IndexInfo and
  Logout links, and hosts the rename/merge controls.
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
- `POST /dashboard/api/add_csv` (the CSV must live inside the file browser's
  browsable roots; always creates a new dataset with a suffix on collision)
- `GET /dashboard/api/whoami`
- `POST /dashboard/api/datasets/<identifier>/rename`
- `POST /dashboard/api/merge`
- `GET /dashboard/` (React SPA)

The query JSON contract is unchanged from the original dashboard, so the
React code works against either backend.

## Legacy

The original ElasticSearch + MySQL + Kibana stack lives in `flask-server/`
and `es_importing/` for reference. `ElasticsearchBackend` ports the relevant
query logic; point `[backend_elasticsearch] es_server` at an existing ES
instance to keep old indices visible.
