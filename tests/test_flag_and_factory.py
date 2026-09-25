"""Blueprint flag and SPA-serving behavior of data_dashboard.routes."""

import os

from flask import Flask

from conftest import make_settings

import data_dashboard.routes as dd_routes

DASHBOARD_ROUTES = [
    "/dashboard/api/indices",
    "/dashboard/api/index_choosen/<path:identifier>",
    "/dashboard/api/index_choosen/meta/<path:identifier>",
    "/dashboard/api/index_choosen/current_status/<path:identifier>",
    "/dashboard/api/query",
    "/dashboard/api/query_paras",
    "/dashboard/api/add_csv",
    "/dashboard/api/whoami",
    "/dashboard/api/merge",
    "/dashboard/api/datasets/<path:identifier>/rename",
    "/dashboard/indexInfo",
]


def test_enabled_flag_registers_routes_and_sets_config(datasets_dir):
    app = Flask(__name__)
    dd_routes.init_blueprint(app, settings=make_settings(datasets_dir), prefix="/dashboard")
    assert app.config["DATA_DASHBOARD_ENABLED"] is True
    registered = {str(rule) for rule in app.url_map.iter_rules()}
    for route in DASHBOARD_ROUTES:
        assert route in registered, "missing route: %s" % route


def test_disabled_flag_registers_nothing(datasets_dir):
    settings = make_settings(datasets_dir)
    settings.set("dashboard", "enabled", "False")
    app = Flask(__name__)
    dd_routes.init_blueprint(app, settings=settings, prefix="/dashboard")
    assert app.config["DATA_DASHBOARD_ENABLED"] is False
    registered = {str(rule) for rule in app.url_map.iter_rules()}
    assert not [r for r in registered if r.startswith("/dashboard")]


def test_broken_backend_disables_instead_of_crashing(datasets_dir):
    settings = make_settings(datasets_dir)
    settings.set("dashboard", "backend", "does_not_exist")
    app = Flask(__name__)
    dd_routes.init_blueprint(app, settings=settings, prefix="/dashboard")
    assert app.config["DATA_DASHBOARD_ENABLED"] is False


def test_spa_requires_login(dashboard_client):
    response = dashboard_client.get("/dashboard/")
    assert response.status_code in (302, 401)


def test_spa_serves_fallback_and_assets(dashboard_client, dashboard_login):
    dashboard_login("iana")
    # the shipped build (or fallback page) is served at the blueprint root
    response = dashboard_client.get("/dashboard/")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()
    # unknown SPA routes fall back to index.html (react-router)
    response = dashboard_client.get("/dashboard/some/spa/route")
    assert response.status_code == 200
    # a real asset inside web/ is served
    web_dir = os.path.join(os.path.dirname(dd_routes.__file__), "web")
    assets = [
        name for name in sorted(os.listdir(os.path.join(web_dir, "static", "js")))
        if name.endswith(".js")
    ]
    assert assets
    response = dashboard_client.get("/dashboard/static/js/" + assets[0])
    assert response.status_code == 200


def test_spa_does_not_leak_files_outside_web(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.get("/dashboard/static/../../settings.ini")
    # werkzeug normalizes the traversal; it must not serve a file outside web/
    assert b"[dashboard]" not in response.data


def test_api_routes_take_precedence_over_spa_catch_all(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.get("/dashboard/api/indices")
    assert response.status_code == 200
    assert response.is_json
    response = dashboard_client.get("/dashboard/indexInfo")
    assert response.status_code == 200
