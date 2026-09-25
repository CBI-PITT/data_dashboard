"""Flask blueprint for the PEACE data dashboard.

Bundling follows the flask_file_browser pattern: one init_blueprint(app,
prefix=...) factory creates the Blueprint with package-absolute template and
web (built React app) directories, wires the storage backend chosen in
settings.ini, registers the JSON API routes and the single-page-app catch-all,
then registers itself and returns the app.

When [dashboard] enabled is false, no routes are registered (the navbar link
is hidden via the app config flag DATA_DASHBOARD_ENABLED).
"""

import os
from dataclasses import replace

from flask import Blueprint, jsonify, request, send_from_directory
from flask_login import login_required

from .backends import get_backend
from .backends.base import DashboardBackendError
from .postprocess import (
    apply_density,
    boxplot_filter_out,
    total_n_and_std,
    total_n_count,
)
from .query_form import parse_query_json
from .utils import csv_within_allowed_roots, get_config, sanitize_dataset_name

routes_script_folder = os.path.dirname(__file__)
settings = get_config(os.path.join(routes_script_folder, 'settings.ini'))
WEB_DIR = os.path.join(routes_script_folder, 'web')


def init_blueprint(app, settings=settings, prefix='/dashboard'):
    dashboard_enabled = settings.getboolean('dashboard', 'enabled', fallback=True)
    app.config['DATA_DASHBOARD_ENABLED'] = dashboard_enabled
    if not dashboard_enabled:
        return app

    try:
        backend = get_backend(settings)
    except Exception as exc:
        # A broken dashboard configuration must not keep the PEACE app from
        # booting; the navbar link is hidden and the API is unavailable.
        print('data_dashboard disabled: %s' % (exc,))
        app.config['DATA_DASHBOARD_ENABLED'] = False
        return app

    blueprint = Blueprint('data_dashboard', __name__)

    def _error_response(exc, status=400):
        return jsonify({'error': str(exc)}), status

    # -- dataset catalog ---------------------------------------------------

    @blueprint.route('/api/indices')
    def get_indices():
        return jsonify(backend.list_datasets())

    @blueprint.route('/api/index_choosen/<dataset>')
    def choose_index(dataset):
        try:
            field_types = backend.get_field_types(dataset)
            categorical, continuous = backend.get_filter_values(dataset)
        except DashboardBackendError as exc:
            return _error_response(exc, 404)
        form_frame = {
            'filter_list': list(field_types.keys()),
            'field': field_types,
            'filter': {'categorical': categorical, 'continuous': continuous},
            'group_by': list(field_types.keys()),
            'aggregate': ['min', 'max', 'avg', 'sum', 'value_count', 'cardinality'],
        }
        return jsonify(form_frame)

    @blueprint.route('/api/index_choosen/meta/<dataset>')
    def index_meta(dataset):
        meta = backend.get_meta(dataset) or {}
        dash = meta.get('dashboard') or {}
        resolution = dash.get('atlas_resolution_micrometer')
        serialized = {
            'meta': {
                'aggregation_condition': dash.get('aggregation_condition'),
                'atlas_structure_acronym_column_name': dash.get('atlas_structure_acronym_column_name'),
                'metadata_calculation_name': dash.get('metadata_calculation_name'),
            },
            'acronym_volumn': None,
        }
        if resolution == 25:
            serialized['acronym_volumn'] = 'acronym_volume_25'
        elif resolution == 10:
            serialized['acronym_volumn'] = 'acronym_volume_10'
        return jsonify(serialized)

    @blueprint.route('/api/index_choosen/current_status/<dataset>')
    def index_status(dataset):
        try:
            return jsonify(backend.get_status(dataset))
        except DashboardBackendError as exc:
            return _error_response(exc, 404)

    @blueprint.route('/indexInfo')
    def index_info():
        rows = []
        for dataset in backend.list_datasets():
            meta = backend.get_meta(dataset) or {}
            fields = meta.get('fields')
            if not fields:
                try:
                    fields = backend.get_field_types(dataset)
                except DashboardBackendError:
                    continue
            for field, ftype in fields.items():
                rows.append({
                    'field': field,
                    'type': ftype,
                    'es_index': dataset,
                    'description': '',
                })
        return jsonify(rows)

    # -- querying ----------------------------------------------------------

    def _run_first_query(json_data, include_n_field):
        spec = parse_query_json(json_data, include_n_field=include_n_field)
        buckets = backend.query(spec)
        agg_list = list(json_data.get('aggregate') or [])
        density_result = apply_density(json_data, buckets, agg_list)
        return spec, density_result['response'], density_result['agg_list']

    @blueprint.route('/api/query', methods=['POST'])
    def query_data_source():
        json_data = request.get_json(silent=True)
        if not isinstance(json_data, dict):
            return _error_response('Invalid JSON payload')
        try:
            spec, buckets, agg_list = _run_first_query(json_data, include_n_field=False)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({'agg_list': boxplot_filter_out(agg_list), 'data': buckets})

    @blueprint.route('/api/query_paras', methods=['POST'])
    def query_paras():
        json_data = request.get_json(silent=True)
        if not isinstance(json_data, dict):
            return _error_response('Invalid JSON payload')
        try:
            spec, buckets_density, agg_list_density = _run_first_query(
                json_data, include_n_field=True)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)

        field = json_data['field']
        agg_list = list(json_data.get('aggregate') or [])
        serialized = json_data.get('serialized_parameters') or {}
        n_field = (serialized.get('meta') or {}).get('metadata_calculation_name')
        agg_list_filtered = boxplot_filter_out(agg_list_density)
        total_n = None

        if n_field and n_field in spec.group_by:
            for item in buckets_density:
                for agg in agg_list:
                    entry = item.get(agg + '_' + field)
                    if not (isinstance(entry, dict) and 'value' in entry):
                        # boxplot buckets carry min/q1/q2/q3/max, not value
                        continue
                    if not item.get('N'):
                        continue
                    item['avg_' + agg + '_' + field] = {
                        'value': entry['value'] / item['N']['value'],
                        'std': 0,
                    }
            total_n = total_n_count(buckets_density, serialized)
            return jsonify({
                'agg_list': agg_list_filtered,
                'data': buckets_density,
                'total_n': total_n,
            })

        if not n_field:
            return _error_response(
                'This dataset has no metadata_calculation_name configured for N normalization')

        group_by_added = list(spec.group_by) + [n_field]
        try:
            spec_added = replace(spec, group_by=group_by_added)
            buckets_added = backend.query(spec_added)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        density_result = apply_density(json_data, buckets_added)
        result = total_n_and_std(
            density_result['response'],
            buckets_density,
            list(agg_list_filtered),
            spec.group_by,
            field,
            serialized,
        )
        agg_list_final = list(agg_list_filtered)
        for agg in agg_list_filtered:
            agg_list_final.append('avg_' + agg)
        return jsonify({
            'agg_list': agg_list_final,
            'data': result['response'],
            'total_n': result['total_n'],
        })

    # -- CSV ingestion (file browser "Add to dashboard" button) ------------

    @blueprint.route('/api/add_csv', methods=['POST'])
    @login_required
    def add_csv():
        json_data = request.get_json(silent=True) or {}
        csv_path = json_data.get('path')
        if not csv_within_allowed_roots(settings, csv_path):
            return _error_response(
                'CSV path is outside the browsable roots or is not an existing CSV file', 403)
        try:
            name = sanitize_dataset_name(os.path.basename(csv_path))
            existed = backend.dataset_exists(name)
            backend.create_dataset(name, csv_path)
            meta = backend.get_meta(name) or {}
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({
            'status': 'ok',
            'dataset': name,
            'existed': existed,
            'rows': meta.get('row_count'),
            'backend': backend.name,
        })

    # -- built React single-page app ----------------------------------------

    @blueprint.route('/', defaults={'asset_path': ''})
    @blueprint.route('/<path:asset_path>')
    def dashboard(asset_path):
        if asset_path:
            candidate = os.path.realpath(os.path.join(WEB_DIR, asset_path))
            if candidate.startswith(WEB_DIR + os.sep) and os.path.isfile(candidate):
                return send_from_directory(WEB_DIR, asset_path)
        return send_from_directory(WEB_DIR, 'index.html')

    app.register_blueprint(blueprint, url_prefix=prefix)
    return app
