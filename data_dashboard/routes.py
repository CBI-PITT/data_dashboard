"""Flask blueprint for the PEACE data dashboard.

Bundling follows the flask_file_browser pattern: one init_blueprint(app,
prefix=...) factory creates the Blueprint with package-absolute template and
web (built React app) directories, wires the storage backend chosen in
settings.ini, registers the JSON API routes and the single-page-app catch-all,
then registers itself and returns the app.

Every route is login-protected: datasets are owned by a user (one folder per
user under datasets_dir), users only see and access their own datasets, and
CBI_Admin (configurable via [dashboard] admins) sees everything. Dataset
identifiers combine as `owner/name`; ownerless/legacy datasets are addressed
with a plain name and are admin-only.

When [dashboard] enabled is false, no routes are registered (the navbar link
is hidden via the app config flag DATA_DASHBOARD_ENABLED).
"""

import os
from dataclasses import replace

from flask import Blueprint, jsonify, request, send_from_directory
from flask_login import current_user, login_required

from .backends import get_backend
from .backends.base import (
    DashboardBackendError,
    UnknownDatasetError,
    build_identifier,
    parse_identifier,
)
from .postprocess import (
    apply_density,
    boxplot_filter_out,
    total_n_and_std,
    total_n_count,
)
from .query_form import parse_query_json
from .utils import (
    csv_within_allowed_roots,
    get_config,
    sanitize_dataset_name,
    sanitize_username,
)

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

    admins = [
        sanitize_username(name.strip())
        for name in settings.get('dashboard', 'admins', fallback='CBI_Admin').split(',')
        if name.strip()
    ]

    blueprint = Blueprint('data_dashboard', __name__)

    def _error_response(exc, status=400):
        return jsonify({'error': str(exc)}), status

    def _current_username():
        """Sanitized username of the logged-in user (for the per-user folder)."""
        return sanitize_username(current_user.get_id())

    def _is_admin(username):
        return username in admins

    def _resolve_identifier(identifier, username):
        """(name, owner) for an identifier, enforcing ownership: users may
        only access their own datasets; admins may access anything, including
        ownerless/legacy datasets (plain-name identifiers)."""
        try:
            name, owner = parse_identifier(identifier)
        except DashboardBackendError as exc:
            raise PermissionError(str(exc))
        # '..' in the name part would escape the per-user folder in every
        # backend path join; reject it at this choke point so no dataset
        # operation (delete, rename, merge, query, read) can traverse.
        if '..' in name.replace('\\', '/').split('/'):
            raise PermissionError(
                'Dataset name must not contain path traversal segments: %r' % (name,))
        if owner is None:
            # ownerless/legacy dataset: admin-only
            if not _is_admin(username):
                raise PermissionError(
                    'Legacy datasets are only accessible to admins')
        elif owner != username and not _is_admin(username):
            raise PermissionError(
                'You can only access your own datasets')
        return name, owner

    # -- session -----------------------------------------------------------

    @blueprint.route('/api/whoami')
    @login_required
    def whoami():
        username = _current_username()
        return jsonify({'user': username, 'is_admin': _is_admin(username)})

    # -- dataset catalog ---------------------------------------------------

    @blueprint.route('/api/indices')
    @login_required
    def get_indices():
        username = _current_username()
        owner = None if _is_admin(username) else username
        return jsonify(backend.list_datasets(owner))

    @blueprint.route('/api/index_choosen/<path:identifier>')
    @login_required
    def choose_index(identifier):
        username = _current_username()
        try:
            name, owner = _resolve_identifier(identifier, username)
            field_types = backend.get_field_types(name, owner)
            categorical, continuous = backend.get_filter_values(name, owner)
        except PermissionError as exc:
            return _error_response(exc, 403)
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

    @blueprint.route('/api/index_choosen/meta/<path:identifier>')
    @login_required
    def index_meta(identifier):
        username = _current_username()
        try:
            name, owner = _resolve_identifier(identifier, username)
            meta = backend.get_meta(name, owner) or {}
        except PermissionError as exc:
            return _error_response(exc, 403)
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

    @blueprint.route('/api/index_choosen/current_status/<path:identifier>')
    @login_required
    def index_status(identifier):
        username = _current_username()
        try:
            name, owner = _resolve_identifier(identifier, username)
            return jsonify(backend.get_status(name, owner))
        except PermissionError as exc:
            return _error_response(exc, 403)
        except DashboardBackendError as exc:
            return _error_response(exc, 404)

    @blueprint.route('/indexInfo')
    @login_required
    def index_info():
        username = _current_username()
        owner = None if _is_admin(username) else username
        rows = []
        for identifier in backend.list_datasets(owner):
            name, dataset_owner = parse_identifier(identifier)
            meta = backend.get_meta(name, dataset_owner) or {}
            fields = meta.get('fields')
            if not fields:
                try:
                    fields = backend.get_field_types(name, dataset_owner)
                except DashboardBackendError:
                    continue
            for field, ftype in fields.items():
                rows.append({
                    'field': field,
                    'type': ftype,
                    'es_index': identifier,
                    'description': '',
                })
        return jsonify(rows)

    # -- querying ----------------------------------------------------------

    def _run_first_query(json_data, username, include_n_field):
        spec = parse_query_json(json_data, include_n_field=include_n_field)
        name, owner = _resolve_identifier(spec.dataset, username)
        spec = replace(spec, dataset=name, owner=owner)
        buckets = backend.query(spec)
        agg_list = list(json_data.get('aggregate') or [])
        density_result = apply_density(json_data, buckets, agg_list)
        return spec, density_result['response'], density_result['agg_list']

    @blueprint.route('/api/query', methods=['POST'])
    @login_required
    def query_data_source():
        username = _current_username()
        json_data = request.get_json(silent=True)
        if not isinstance(json_data, dict):
            return _error_response('Invalid JSON payload')
        try:
            spec, buckets, agg_list = _run_first_query(json_data, username, include_n_field=False)
        except PermissionError as exc:
            return _error_response(exc, 403)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({'agg_list': boxplot_filter_out(agg_list), 'data': buckets})

    @blueprint.route('/api/query_paras', methods=['POST'])
    @login_required
    def query_paras():
        username = _current_username()
        json_data = request.get_json(silent=True)
        if not isinstance(json_data, dict):
            return _error_response('Invalid JSON payload')
        try:
            spec, buckets_density, agg_list_density = _run_first_query(
                json_data, username, include_n_field=True)
        except PermissionError as exc:
            return _error_response(exc, 403)
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
        username = _current_username()
        try:
            name = sanitize_dataset_name(os.path.basename(csv_path))
            final = backend.create_dataset(name, csv_path, owner=username)
            meta = backend.get_meta(final, username) or {}
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({
            'status': 'ok',
            'dataset': build_identifier(meta.get('name', final), username),
            'rows': meta.get('row_count'),
            'backend': backend.name,
        })

    # -- dataset management (rename / delete / merge) -----------------------

    @blueprint.route('/api/datasets/<path:identifier>/rename', methods=['POST'])
    @login_required
    def rename_dataset(identifier):
        username = _current_username()
        json_data = request.get_json(silent=True) or {}
        new_name = json_data.get('new_name')
        try:
            name, owner = _resolve_identifier(identifier, username)
            final = backend.rename_dataset(name, new_name, owner)
        except PermissionError as exc:
            return _error_response(exc, 403)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({'status': 'ok', 'dataset': build_identifier(final, owner)})

    @blueprint.route('/api/datasets/<path:identifier>/delete', methods=['POST'])
    @login_required
    def delete_dataset(identifier):
        username = _current_username()
        try:
            name, owner = _resolve_identifier(identifier, username)
            if not backend.dataset_exists(name, owner):
                raise UnknownDatasetError(name)
            # The backends re-check containment (ensure_within) before any
            # file is removed, so only files inside the dashboard folder can
            # ever be deleted; the original CSVs are never touched.
            backend.delete_dataset(name, owner)
        except PermissionError as exc:
            return _error_response(exc, 403)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({'status': 'ok'})

    @blueprint.route('/api/merge', methods=['POST'])
    @login_required
    def merge_datasets():
        username = _current_username()
        json_data = request.get_json(silent=True) or {}
        sources = json_data.get('datasets') or []
        fields = json_data.get('fields') or {}
        new_name = json_data.get('name')
        if not isinstance(sources, list) or len(sources) < 2:
            return _error_response('Merging requires at least two datasets')
        if not new_name or not isinstance(new_name, str):
            return _error_response("A 'name' for the merged dataset is required")
        if not isinstance(fields, dict):
            return _error_response("'fields' must be an object keyed by dataset identifier")
        prepared = []
        try:
            for identifier in sources:
                name, owner = _resolve_identifier(identifier, username)
                source_fields = fields.get(identifier) or {}
                if not isinstance(source_fields, dict):
                    return _error_response(
                        "Fields for %r must be an object of key/value pairs" % (identifier,))
                prepared.append((name, owner, source_fields))
            final = backend.merge_datasets(prepared, new_name, owner=username)
        except PermissionError as exc:
            return _error_response(exc, 403)
        except (ValueError, DashboardBackendError) as exc:
            return _error_response(exc)
        return jsonify({'status': 'ok', 'dataset': build_identifier(final, username)})

    # -- built React single-page app ----------------------------------------

    @blueprint.route('/', defaults={'asset_path': ''})
    @blueprint.route('/<path:asset_path>')
    @login_required
    def dashboard(asset_path):
        if asset_path:
            candidate = os.path.realpath(os.path.join(WEB_DIR, asset_path))
            if candidate.startswith(WEB_DIR + os.sep) and os.path.isfile(candidate):
                return send_from_directory(WEB_DIR, asset_path)
        return send_from_directory(WEB_DIR, 'index.html')

    app.register_blueprint(blueprint, url_prefix=prefix)
    return app
