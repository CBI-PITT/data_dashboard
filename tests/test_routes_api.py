"""API route contract tests through the real blueprint (Flask test client).

Every route is login-protected: users see and access only their own datasets
(identifiers are `owner/name`), admins (CBI_Admin) see everything. The JSON
contracts are pinned to the original dashboard's bp_routes/dashboard.py
shapes so the React code keeps working unchanged.
"""

import json
import os

import pytest

from conftest import FakeUser

from data_dashboard.backends.base import write_meta


@pytest.fixture()
def dataset(dashboard_app, parquet_backend, cells_csv):
    parquet_backend.create_dataset("job_0101_cells", cells_csv, owner="iana")
    return "iana/job_0101_cells"


@pytest.fixture()
def dataset_with_dashboard_params(dataset, parquet_backend):
    meta = parquet_backend.get_meta("job_0101_cells", "iana") or {}
    meta["dashboard"] = {
        "aggregation_condition": "value_count",
        "atlas_structure_acronym_column_name": "atlas_structure_acronym",
        "metadata_calculation_name": "metadata",
        "atlas_resolution_micrometer": 25,
    }
    write_meta(parquet_backend._user_dir("iana"), "job_0101_cells", meta)
    return dataset


def payload(dataset="iana/job_0101_cells", **overrides):
    body = {
        "INDEX": dataset,
        "field": "x_raw",
        "filter": {
            "categorical": {"treatment": ["ctrl"]},
            "continuous": {"x_raw": [0.0, 100.0]},
        },
        "group_by": ["treatment"],
        "aggregate": ["avg", "boxplot"],
    }
    body.update(overrides)
    return body


# -- session -----------------------------------------------------------------


def test_whoami(dashboard_client, dashboard_login):
    dashboard_login("iana")
    body = dashboard_client.get("/dashboard/api/whoami").get_json()
    assert body == {"user": "iana", "is_admin": False}
    dashboard_login("CBI_Admin")
    body = dashboard_client.get("/dashboard/api/whoami").get_json()
    assert body == {"user": "CBI_Admin", "is_admin": True}


def test_routes_require_login(dashboard_client, dataset):
    for url in (
        "/dashboard/api/indices",
        "/dashboard/api/index_choosen/" + dataset,
        "/dashboard/api/index_choosen/meta/" + dataset,
        "/dashboard/api/index_choosen/current_status/" + dataset,
        "/dashboard/indexInfo",
        "/dashboard/api/whoami",
        "/dashboard/",
    ):
        response = dashboard_client.get(url)
        assert response.status_code in (302, 401), (
            "%s must be login-protected" % url)
    for url, json_body in (
        ("/dashboard/api/query", payload()),
        ("/dashboard/api/merge", {}),
        ("/dashboard/api/datasets/" + dataset + "/rename", {}),
        ("/dashboard/api/datasets/" + dataset + "/delete", {}),
    ):
        response = dashboard_client.post(url, json=json_body)
        assert response.status_code in (302, 401), (
            "%s must be login-protected" % url)


# -- catalog -----------------------------------------------------------------


def test_indices_lists_own_datasets(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    assert dashboard_client.get("/dashboard/api/indices").get_json() == [dataset]


def test_admin_sees_every_users_datasets(dashboard_client, dashboard_login,
                                         parquet_backend, cells_csv, dataset):
    parquet_backend.create_dataset("other_cells", cells_csv, owner="dutta-p")
    parquet_backend.create_dataset("root_cells", cells_csv, owner=None)
    dashboard_login("CBI_Admin")
    indices = dashboard_client.get("/dashboard/api/indices").get_json()
    assert set(indices) == {dataset, "dutta-p/other_cells", "root_cells"}


def test_user_does_not_see_other_users_datasets(dashboard_client, dashboard_login,
                                                parquet_backend, cells_csv, dataset):
    parquet_backend.create_dataset("other_cells", cells_csv, owner="dutta-p")
    dashboard_login("iana")
    assert dashboard_client.get("/dashboard/api/indices").get_json() == [dataset]


def test_index_choosen_formframe_contract(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    response = dashboard_client.get("/dashboard/api/index_choosen/" + dataset)
    assert response.status_code == 200
    frame = response.get_json()
    # pinned to the original choosen_index() contract
    assert set(frame.keys()) == {"filter_list", "field", "filter", "group_by", "aggregate"}
    assert frame["field"]["treatment"] == "keyword"
    assert frame["field"]["x_raw"] == "float"
    assert frame["filter"]["categorical"]["treatment"] == ["ctrl", "stim"]
    assert len(frame["filter"]["continuous"]["x_raw"]) == 2
    assert frame["aggregate"] == ["min", "max", "avg", "sum", "value_count", "cardinality"]
    assert frame["group_by"] == frame["filter_list"]


def test_index_choosen_unknown_dataset_404(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.get("/dashboard/api/index_choosen/iana/missing")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_cross_user_access_403(dashboard_client, dashboard_login, parquet_backend,
                               cells_csv):
    parquet_backend.create_dataset("not_yours", cells_csv, owner="dutta-p")
    dashboard_login("iana")
    response = dashboard_client.get("/dashboard/api/index_choosen/dutta-p/not_yours")
    assert response.status_code == 403
    response = dashboard_client.post(
        "/dashboard/api/query", json=payload(dataset="dutta-p/not_yours"))
    assert response.status_code == 403


def test_ownerless_identifier_admin_only(dashboard_client, dashboard_login,
                                         parquet_backend, cells_csv):
    parquet_backend.create_dataset("legacy", cells_csv, owner=None)
    dashboard_login("iana")
    assert dashboard_client.get(
        "/dashboard/api/index_choosen/legacy").status_code == 403
    dashboard_login("CBI_Admin")
    assert dashboard_client.get(
        "/dashboard/api/index_choosen/legacy").status_code == 200


def test_current_status_contract(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    status = dashboard_client.get(
        "/dashboard/api/index_choosen/current_status/" + dataset).get_json()
    assert set(status.keys()) == {"health", "status", "storage_size", "docs_count"}
    assert status["health"] == "green"
    assert status["docs_count"] == "60"


def test_meta_defaults_when_unconfigured(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    meta = dashboard_client.get("/dashboard/api/index_choosen/meta/" + dataset).get_json()
    assert meta == {
        "meta": {
            "aggregation_condition": None,
            "atlas_structure_acronym_column_name": None,
            "metadata_calculation_name": None,
        },
        "acronym_volumn": None,
    }


def test_meta_maps_atlas_resolution(dashboard_client, dashboard_login,
                                    dataset_with_dashboard_params):
    dashboard_login("iana")
    meta = dashboard_client.get(
        "/dashboard/api/index_choosen/meta/iana/job_0101_cells").get_json()
    assert meta["acronym_volumn"] == "acronym_volume_25"
    assert meta["meta"]["metadata_calculation_name"] == "metadata"


def test_index_info_rows_scoped(dashboard_client, dashboard_login, dataset,
                                parquet_backend, cells_csv):
    parquet_backend.create_dataset("other_cells", cells_csv, owner="dutta-p")
    dashboard_login("iana")
    rows = dashboard_client.get("/dashboard/indexInfo").get_json()
    assert rows
    for row in rows:
        assert set(row.keys()) == {"field", "type", "es_index", "description"}
        assert row["es_index"] == "iana/job_0101_cells"


# -- queries ------------------------------------------------------------------


def test_query_contract(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    response = dashboard_client.post("/dashboard/api/query", json=payload())
    assert response.status_code == 200
    data = response.get_json()
    assert set(data.keys()) == {"agg_list", "data"}
    assert data["agg_list"] == ["avg"]  # boxplot stripped, like dashboard.py
    bucket = data["data"][0]
    assert bucket["key"] == {"treatment": "ctrl"}
    assert bucket["avg_x_raw"]["value"] == pytest.approx(
        sum(0.5 * i for i in range(0, 60, 2)) / 30)
    # boxplot values stay in the bucket data for the Box chart
    assert sorted(bucket["boxplot_x_raw"].keys()) == ["max", "min", "q1", "q2", "q3"]


def test_query_density_applied_from_sidecar(dashboard_client, dashboard_login,
                                            dataset_with_dashboard_params):
    dashboard_login("iana")
    body = payload(
        field="atlas_structure_acronym",
        aggregate=["value_count"],
        group_by=["atlas_structure_acronym"],
        filter={"categorical": {}, "continuous": {}},
        serialized_parameters={
            "meta": {
                "aggregation_condition": "value_count",
                "atlas_structure_acronym_column_name": "atlas_structure_acronym",
                "metadata_calculation_name": "metadata",
            },
            "acronym_volumn": "acronym_volume_25",
        })
    data = dashboard_client.post("/dashboard/api/query", json=body).get_json()
    assert "density" in data["agg_list"]
    bucket = data["data"][0]
    assert bucket["density_atlas_structure_acronym"]["value"] > 0


def test_query_paras_n_in_group_by(dashboard_client, dashboard_login,
                                   dataset_with_dashboard_params):
    dashboard_login("iana")
    body = payload(
        aggregate=["value_count"],
        serialized_parameters={
            "meta": {
                "aggregation_condition": None,
                "atlas_structure_acronym_column_name": None,
                "metadata_calculation_name": "metadata",
            },
            "acronym_volumn": None,
        })
    body["group_by"] = ["metadata"]
    data = dashboard_client.post("/dashboard/api/query_paras", json=body).get_json()
    assert set(data.keys()) == {"agg_list", "data", "total_n"}
    assert data["total_n"] == 3  # metadata values 0, 1, 2
    bucket = data["data"][0]
    assert bucket["avg_value_count_x_raw"]["std"] == 0
    assert bucket["avg_value_count_x_raw"]["value"] == pytest.approx(
        bucket["value_count_x_raw"]["value"] / bucket["N"]["value"])


def test_query_paras_n_not_in_group_by_adds_second_grouped_query(
        dashboard_client, dashboard_login, dataset_with_dashboard_params):
    dashboard_login("iana")
    body = payload(
        aggregate=["value_count"],
        serialized_parameters={
            "meta": {
                "aggregation_condition": None,
                "atlas_structure_acronym_column_name": None,
                "metadata_calculation_name": "metadata",
            },
            "acronym_volumn": None,
        })
    data = dashboard_client.post("/dashboard/api/query_paras", json=body).get_json()
    assert set(data.keys()) == {"agg_list", "data", "total_n"}
    # agg_list gains the avg_ entries, like dashboard.py's else branch
    assert data["agg_list"] == ["value_count", "avg_value_count"]
    bucket = data["data"][0]
    assert bucket["avg_value_count_x_raw"]["value"] == pytest.approx(
        bucket["value_count_x_raw"]["value"] / bucket["N"]["value"])
    assert bucket["avg_value_count_x_raw"]["std"] is not None
    assert data["total_n"] == 3


def test_query_paras_without_n_config_returns_400(dashboard_client, dashboard_login,
                                                  dataset):
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/query_paras", json=payload(aggregate=["avg"]))
    assert response.status_code == 400
    assert "metadata_calculation_name" in response.get_json()["error"]


def test_malformed_payloads_return_400(dashboard_client, dashboard_login, dataset):
    dashboard_login("iana")
    assert dashboard_client.post("/dashboard/api/query", json=None).status_code == 400
    assert dashboard_client.post("/dashboard/api/query", json={"field": "x"}).status_code == 400
    assert dashboard_client.post(
        "/dashboard/api/query", json=payload(dataset="iana/missing")).status_code == 400
    assert dashboard_client.post(
        "/dashboard/api/query",
        json=payload(aggregate=["percentile"])).status_code == 400
    assert dashboard_client.post(
        "/dashboard/api/query", json=payload(group_by=["nope"])).status_code == 400


# -- add_csv ------------------------------------------------------------------


def test_add_csv_requires_login(dashboard_client, dataset, cells_csv):
    response = dashboard_client.post(
        "/dashboard/api/add_csv", json={"path": cells_csv})
    # flask_login: 302 redirect when a login_view is configured, else 401
    assert response.status_code in (302, 401)


def test_add_csv_creates_new_dataset_with_suffix(dashboard_client, dashboard_login,
                                                 cells_csv, tmp_path, monkeypatch):
    dashboard_login("iana")
    import data_dashboard.routes as dd_routes
    monkeypatch.setattr(dd_routes, "csv_within_allowed_roots", lambda settings, path: True)
    # a second CSV with the same basename must get a _2 suffix, never overwrite
    second = tmp_path / "job_0101_cells.csv"
    second.write_text("treatment,atlas_structure_acronym,metadata,x_raw,y_raw,z_raw\nctrl,root,1,1.0,1.0,1.0\n")
    response = dashboard_client.post("/dashboard/api/add_csv", json={"path": str(second)})
    assert response.status_code == 200
    body = response.get_json()
    assert body["dataset"] == "iana/job_0101_cells"
    assert dashboard_client.get("/dashboard/api/indices").get_json() == ["iana/job_0101_cells"]
    response = dashboard_client.post("/dashboard/api/add_csv", json={"path": str(second)})
    assert response.get_json()["dataset"] == "iana/job_0101_cells_2"
    assert dashboard_client.get("/dashboard/api/indices").get_json() == [
        "iana/job_0101_cells", "iana/job_0101_cells_2"]


def test_add_csv_rejects_outside_roots(dashboard_client, dashboard_login, tmp_path):
    dashboard_login("iana")
    outside = tmp_path / "outside.csv"
    outside.write_text("a,b\n1,2\n")
    response = dashboard_client.post(
        "/dashboard/api/add_csv", json={"path": str(outside)})
    assert response.status_code == 403
    assert "error" in response.get_json()


# -- rename -------------------------------------------------------------------


def test_rename_dataset(dashboard_client, dashboard_login, dataset, parquet_backend):
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/" + dataset + "/rename",
        json={"new_name": "renamed_cells"})
    assert response.status_code == 200
    assert response.get_json()["dataset"] == "iana/renamed_cells"
    assert parquet_backend.dataset_exists("renamed_cells", "iana")
    assert not parquet_backend.dataset_exists("job_0101_cells", "iana")
    meta = parquet_backend.get_meta("renamed_cells", "iana")
    assert meta["name"] == "renamed_cells"
    assert dashboard_client.get("/dashboard/api/indices").get_json() == ["iana/renamed_cells"]


def test_rename_collision_400(dashboard_client, dashboard_login, dataset,
                              parquet_backend, cells_csv):
    parquet_backend.create_dataset("taken", cells_csv, owner="iana")
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/" + dataset + "/rename",
        json={"new_name": "taken"})
    assert response.status_code == 400


def test_rename_other_users_dataset_403(dashboard_client, dashboard_login,
                                        parquet_backend, cells_csv):
    parquet_backend.create_dataset("theirs", cells_csv, owner="dutta-p")
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/dutta-p/theirs/rename",
        json={"new_name": "mine"})
    assert response.status_code == 403


def test_rename_rejects_path_traversal_403(dashboard_client, dashboard_login,
                                           parquet_backend, dataset, tmp_path):
    """'..' in the identifier name is rejected at the _resolve_identifier
    choke point, before rename's raw src path could address a file outside
    the dashboard datasets folder. The decoy sits exactly at the path
    datasets_dir/iana/../../escape.parquet resolves to."""
    outside = os.path.abspath(
        os.path.join(parquet_backend._user_dir("iana"), "..", "..", "escape.parquet"))
    with open(outside, "w") as fh:
        fh.write("do not delete")
    try:
        dashboard_login("iana")
        response = dashboard_client.post(
            "/dashboard/api/datasets/iana/../../escape/rename",
            json={"new_name": "sneaky"})
        assert response.status_code == 403
        with open(outside) as fh:
            assert fh.read() == "do not delete"
        assert parquet_backend.dataset_exists("job_0101_cells", "iana")
    finally:
        if os.path.isfile(outside):
            os.remove(outside)


# -- delete -------------------------------------------------------------------


def test_delete_dataset(dashboard_client, dashboard_login, dataset,
                        parquet_backend, cells_csv):
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/" + dataset + "/delete")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    # the parquet copy and its sidecar are gone from the dashboard folder
    assert not parquet_backend.dataset_exists("job_0101_cells", "iana")
    assert not os.path.isfile(parquet_backend._meta_file("job_0101_cells", "iana"))
    assert dashboard_client.get("/dashboard/api/indices").get_json() == []
    # the original CSV the dataset was ingested from stays intact
    assert os.path.isfile(cells_csv)


def test_delete_unknown_dataset_400(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/iana/nothere/delete")
    assert response.status_code == 400


def test_delete_other_users_dataset_403(dashboard_client, dashboard_login,
                                        parquet_backend, cells_csv):
    parquet_backend.create_dataset("theirs", cells_csv, owner="dutta-p")
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/dutta-p/theirs/delete")
    assert response.status_code == 403
    assert parquet_backend.dataset_exists("theirs", "dutta-p")


def test_delete_rejects_path_traversal_403(dashboard_client, dashboard_login,
                                           parquet_backend, dataset, tmp_path):
    """identifier 'iana/../../escape' passes the ownership check but resolves
    outside the dashboard datasets folder (datasets_dir/iana/../../) — the
    containment checks must abort with 403 and leave the decoy file at the
    escape target intact."""
    outside = os.path.abspath(
        os.path.join(parquet_backend._user_dir("iana"), "..", "..", "escape.parquet"))
    with open(outside, "w") as fh:
        fh.write("do not delete")
    try:
        dashboard_login("iana")
        response = dashboard_client.post(
            "/dashboard/api/datasets/iana/../../escape/delete")
        assert response.status_code == 403
        with open(outside) as fh:
            assert fh.read() == "do not delete"
        assert parquet_backend.dataset_exists("job_0101_cells", "iana")
    finally:
        if os.path.isfile(outside):
            os.remove(outside)


def test_delete_ownerless_traversal_rejected_for_admin_403(dashboard_client,
                                                           dashboard_login,
                                                           parquet_backend,
                                                           dataset, tmp_path):
    """Ownerless (plain-name) identifiers are admin-only, so a '..' name can
    only reach the backends as an admin — still rejected by containment."""
    outside = os.path.abspath(
        os.path.join(parquet_backend.datasets_dir, "..", "..", "escape.parquet"))
    with open(outside, "w") as fh:
        fh.write("do not delete")
    try:
        dashboard_login("CBI_Admin")
        response = dashboard_client.post(
            "/dashboard/api/datasets/../../escape/delete")
        assert response.status_code == 403
        with open(outside) as fh:
            assert fh.read() == "do not delete"
    finally:
        if os.path.isfile(outside):
            os.remove(outside)


def test_delete_rejects_symlink_escape_403(dashboard_client, dashboard_login,
                                           parquet_backend, dataset, tmp_path):
    """A symlink inside the owner's folder that points outside the dashboard
    datasets folder must be refused by the realpath containment check."""
    outside = os.path.join(str(tmp_path), "outside_target.parquet")
    with open(outside, "w") as fh:
        fh.write("keep me")
    link = os.path.join(parquet_backend._user_dir("iana"), "escape_link.parquet")
    os.symlink(outside, link)
    dashboard_login("iana")
    response = dashboard_client.post(
        "/dashboard/api/datasets/iana/escape_link/delete")
    assert response.status_code == 403
    with open(outside) as fh:
        assert fh.read() == "keep me"
    assert os.path.isfile(link)
    assert parquet_backend.dataset_exists("job_0101_cells", "iana")


# -- merge --------------------------------------------------------------------


def test_merge_bakes_fields_and_sample_column(dashboard_client, dashboard_login,
                                              parquet_backend, cells_csv):
    parquet_backend.create_dataset("brain_a", cells_csv, owner="iana")
    parquet_backend.create_dataset("brain_b", cells_csv, owner="iana")
    dashboard_login("iana")
    response = dashboard_client.post("/dashboard/api/merge", json={
        "datasets": ["iana/brain_a", "iana/brain_b"],
        "name": "experiment",
        "fields": {"iana/brain_a": {"treatment": "ctrl"},
                   "iana/brain_b": {"treatment": "stim"}},
    })
    assert response.status_code == 200
    assert response.get_json()["dataset"] == "iana/experiment"

    from data_dashboard.backends.base import Aggregate, QuerySpec
    buckets = parquet_backend.query(QuerySpec(
        dataset="experiment", field="x_raw", owner="iana", filters=[],
        group_by=["treatment"],
        aggregates=[Aggregate("value_count", "x_raw")]))
    by_treatment = {b["key"]["treatment"]: b["value_count_x_raw"]["value"] for b in buckets}
    assert by_treatment == {"ctrl": 60, "stim": 60}  # both sources are the 60-row fixture
    # sample column tags every source
    samples = parquet_backend.get_filter_values("experiment", "iana")[0]["sample"]
    assert samples == ["brain_a", "brain_b"]
    # sources are untouched
    assert parquet_backend.dataset_exists("brain_a", "iana")
    assert parquet_backend.dataset_exists("brain_b", "iana")
    meta = parquet_backend.get_meta("experiment", "iana")
    assert [s["name"] for s in meta["samples"]] == ["brain_a", "brain_b"]
    assert meta["samples"][0]["fields"] == {"treatment": "ctrl"}


def test_merge_requires_two_datasets(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.post("/dashboard/api/merge", json={
        "datasets": ["iana/one"], "name": "x"})
    assert response.status_code == 400


def test_merge_requires_name(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.post("/dashboard/api/merge", json={
        "datasets": ["iana/one", "iana/two"]})
    assert response.status_code == 400


def test_merge_other_users_dataset_403(dashboard_client, dashboard_login,
                                       parquet_backend, cells_csv):
    parquet_backend.create_dataset("theirs", cells_csv, owner="dutta-p")
    parquet_backend.create_dataset("mine", cells_csv, owner="iana")
    dashboard_login("iana")
    response = dashboard_client.post("/dashboard/api/merge", json={
        "datasets": ["iana/mine", "dutta-p/theirs"], "name": "sneaky"})
    assert response.status_code == 403
    assert not parquet_backend.dataset_exists("sneaky", "iana")
