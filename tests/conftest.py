"""Shared fixtures for the data_dashboard tests.

All dataset writes are sandboxed to a temp datasets_dir. The Flask app
fixture registers the real data_dashboard blueprint against that temp dir,
with a mocked flask_login user loader (any id accepted). The elasticsearch
package is stubbed in sys.modules so the ElasticsearchBackend can be
constructed and its query/request logic tested without the package installed
(parquet-only deployment parity).
"""

import configparser
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = REPO_ROOT / "data_dashboard"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class FakeUser:
    def __init__(self, user_id):
        self.id = user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


def make_settings(datasets_dir, backend="parquet"):
    """A settings copy pointing [dashboard] at the temp datasets dir."""
    settings = configparser.ConfigParser(allow_no_value=True)
    settings.read(str(PACKAGE_DIR / "settings.ini"))
    settings.set("dashboard", "enabled", "True")
    settings.set("dashboard", "backend", backend)
    settings.set("dashboard", "datasets_dir", str(datasets_dir))
    return settings


@pytest.fixture()
def datasets_dir(tmp_path):
    directory = tmp_path / "datasets"
    directory.mkdir()
    return str(directory)


@pytest.fixture()
def settings(datasets_dir):
    return make_settings(datasets_dir, backend="parquet")


@pytest.fixture()
def parquet_backend(datasets_dir):
    from data_dashboard.backends.parquet import ParquetBackend
    return ParquetBackend(datasets_dir)


@pytest.fixture()
def es_backend(datasets_dir, monkeypatch):
    """ElasticsearchBackend with the elasticsearch package stubbed out."""
    import fake_es
    fake_es.install(monkeypatch)
    from data_dashboard.backends.elasticsearch import ElasticsearchBackend
    return ElasticsearchBackend(datasets_dir, es_server="http://fake:9200")


@pytest.fixture()
def dashboard_app(datasets_dir):
    """The real data_dashboard blueprint behind a minimal Flask app."""
    from flask import Flask
    from flask_login import LoginManager
    import data_dashboard.routes as dd_routes

    app = Flask(__name__)
    app.secret_key = "dashboard-test-key"
    dd_routes.init_blueprint(app, settings=make_settings(datasets_dir), prefix="/dashboard")

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def _load(user_id):
        return FakeUser(user_id)

    app.config["TESTING"] = True
    return app


@pytest.fixture()
def dashboard_client(dashboard_app):
    return dashboard_app.test_client()


@pytest.fixture()
def dashboard_login(dashboard_client):
    def _login(user_id="iana"):
        with dashboard_client.session_transaction() as sess:
            sess["_user_id"] = user_id
            sess["_fresh"] = True
    return _login


@pytest.fixture()
def cells_csv(tmp_path):
    """A small cells CSV with keyword + numeric columns. The acronyms are
    real allen mouse atlas entries so density lookups resolve."""
    path = tmp_path / "job_0101_cells.csv"
    lines = ["treatment,atlas_structure_acronym,metadata,x_raw,y_raw,z_raw"]
    for i in range(60):
        lines.append("%s,%s,%d,%f,%f,%f" % (
            ["ctrl", "stim"][i % 2], ["root", "grey", "CTX"][i % 3], i % 3,
            i * 0.5, i * 0.25, i * 0.125))
    path.write_text("\n".join(lines) + "\n")
    return str(path)


@pytest.fixture(scope="session")
def big_quoted_csv(tmp_path_factory):
    """25k rows with one quoted-comma field beyond the 20480-row sniffer
    sample — the exact shape that produced the production add_csv 500."""
    path = tmp_path_factory.mktemp("csv") / "merged_cells.csv"
    lines = ["atlas_structure_name,atlas_structure_acronym,atlas_structure_number,x_raw"]
    for i in range(25000):
        if i == 23000:
            lines.append('"Retrosplenial area, dorsal part, layer 1",RSPd1,442,55.5')
        else:
            lines.append("cortex,CTX,%d,%f" % (100 + i, i * 0.5))
    path.write_text("\n".join(lines) + "\n")
    return str(path)
