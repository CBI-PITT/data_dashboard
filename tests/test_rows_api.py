"""Rows endpoint + backend get_rows coverage for the spreadsheet view.

The dashboard spreadsheet loads dataset rows progressively: the route
POST /api/datasets/<identifier>/rows returns one page (offset/limit) with the
column schema (name + ES-flavoured type + categorical/numeric kind) and the
total row count, and accepts the same filter payload shape as /api/query so
the table can reflect the form's filter selections immediately. Continuous
filters that still carry the meta's full min/max range (untouched sliders)
are treated as no filter.
"""

import pytest

from data_dashboard.backends.base import CategoricalFilter, ContinuousFilter
from data_dashboard.query_form import parse_filters

ROWS_URL = "/dashboard/api/datasets/%s/rows"


@pytest.fixture()
def owned_dataset(parquet_backend, cells_csv):
    """A small dataset owned by iana (60 rows, keyword + numeric columns)."""
    return parquet_backend.create_dataset("job_0101_cells", cells_csv, owner="iana")


@pytest.fixture()
def es_dataset(es_backend, cells_csv):
    return es_backend.create_dataset("job_0101_cells", cells_csv, owner="iana")


@pytest.fixture()
def nulls_dataset(parquet_backend, tmp_path):
    """A dataset whose numeric column holds one NULL — the case the full-
    range skip exists for (BETWEEN would exclude the NULL row)."""
    path = tmp_path / "nulls.csv"
    lines = ["treatment,x_raw"]
    for i in range(59):
        lines.append("%s,%f" % (["ctrl", "stim"][i % 2], i * 1.0))
    lines.append("ctrl,")  # NULL x_raw in the last row
    path.write_text("\n".join(lines) + "\n")
    return parquet_backend.create_dataset("nulls", str(path), owner="iana")


# -- ParquetBackend.get_rows -------------------------------------------------


def test_parquet_get_rows_unfiltered_page(parquet_backend, owned_dataset):
    result = parquet_backend.get_rows(owned_dataset, offset=0, limit=25, owner="iana")
    assert result["columns"] == [
        "treatment", "atlas_structure_acronym", "metadata", "x_raw", "y_raw", "z_raw",
    ]
    assert len(result["rows"]) == 25
    assert result["total"] == 60
    # rows follow the CSV order: ctrl/stim alternating, x_raw = i * 0.5
    assert result["rows"][0][0] == "ctrl"
    assert result["rows"][0][3] == 0.0
    assert result["rows"][1][0] == "stim"


def test_parquet_get_rows_offset_append(parquet_backend, owned_dataset):
    first = parquet_backend.get_rows(owned_dataset, offset=0, limit=50, owner="iana")
    second = parquet_backend.get_rows(owned_dataset, offset=50, limit=50, owner="iana")
    assert len(first["rows"]) == 50 and len(second["rows"]) == 10
    assert second["rows"][0][2] == first["rows"][49][2] + 1  # metadata i continues
    beyond = parquet_backend.get_rows(owned_dataset, offset=60, limit=50, owner="iana")
    assert beyond["rows"] == [] and beyond["total"] == 60


def test_parquet_get_rows_total_from_sidecar_when_unfiltered(
        parquet_backend, owned_dataset):
    """Unfiltered totals come from the sidecar meta (no COUNT query needed);
    meta row_count is a plain int."""
    result = parquet_backend.get_rows(owned_dataset, owner="iana")
    assert isinstance(result["total"], int) and result["total"] == 60


def test_parquet_get_rows_categorical_filter(parquet_backend, owned_dataset):
    result = parquet_backend.get_rows(
        owned_dataset, owner="iana",
        filters=[CategoricalFilter("treatment", ["stim"])])
    assert result["total"] == 30
    assert all(row[0] == "stim" for row in result["rows"])
    # empty selection = no filter (query() parity)
    empty = parquet_backend.get_rows(
        owned_dataset, owner="iana", filters=[CategoricalFilter("treatment", [])])
    assert empty["total"] == 60


def test_parquet_get_rows_continuous_filter(parquet_backend, owned_dataset):
    result = parquet_backend.get_rows(
        owned_dataset, owner="iana", filters=[ContinuousFilter("x_raw", 10.0, 20.0)])
    assert result["total"] == 21  # x_raw = 10.0..20.0 step 0.5 inclusive
    assert all(10.0 <= row[3] <= 20.0 for row in result["rows"])


def test_parquet_get_rows_full_range_treated_as_no_filter(
        parquet_backend, nulls_dataset):
    """Untouched sliders carry the meta's full [min, max]; that must behave
    as no filter — the NULL row stays visible (BETWEEN would drop it)."""
    meta = parquet_backend.get_meta(nulls_dataset, "iana")
    low, high = meta["continuous"]["x_raw"]
    result = parquet_backend.get_rows(
        nulls_dataset, owner="iana", filters=[ContinuousFilter("x_raw", low, high)])
    assert result["total"] == 60  # NULL row included
    filtered = parquet_backend.get_rows(
        nulls_dataset, owner="iana", filters=[ContinuousFilter("x_raw", 10.0, 20.0)])
    assert filtered["total"] == 11  # a real subset range still filters


def test_parquet_get_rows_unknown_field(parquet_backend, owned_dataset):
    with pytest.raises(Exception):
        parquet_backend.get_rows(
            owned_dataset, owner="iana",
            filters=[CategoricalFilter("nope", ["x"])])


def test_parquet_get_rows_missing_dataset(parquet_backend, datasets_dir):
    from data_dashboard.backends.base import UnknownDatasetError
    with pytest.raises(UnknownDatasetError):
        parquet_backend.get_rows("ghost", owner="iana")


# -- query_form.parse_filters (shared with /api/query) ------------------------


def test_parse_filters_payload_parity():
    filters = parse_filters({
        "categorical": {"treatment": ["ctrl"]},
        "continuous": {"x_raw": [0, 100]},
    })
    assert [f.field for f in filters] == ["treatment", "x_raw"]
    assert isinstance(filters[0], CategoricalFilter)
    assert isinstance(filters[1], ContinuousFilter)
    assert filters[1].min == 0.0 and filters[1].max == 100.0


def test_parse_filters_empty_payload():
    assert parse_filters({}) == []
    assert parse_filters({"categorical": {}, "continuous": {}}) == []


def test_parse_filters_rejects_malformed():
    with pytest.raises(ValueError):
        parse_filters({"categorical": {"treatment": "ctrl"}})
    with pytest.raises(ValueError):
        parse_filters({"continuous": {"x_raw": [1]}})
    with pytest.raises(ValueError):
        parse_filters("nope")


# -- /api/datasets/<identifier>/rows route ------------------------------------


def test_rows_route_happy_path(dashboard_client, dashboard_login,
                               parquet_backend, owned_dataset):
    dashboard_login("iana")
    response = dashboard_client.post(ROWS_URL % ("iana/" + owned_dataset), json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 60
    assert data["offset"] == 0 and data["limit"] == 200
    assert len(data["rows"]) == 60
    kinds = {col["name"]: col["kind"] for col in data["columns"]}
    types = {col["name"]: col["type"] for col in data["columns"]}
    assert kinds["treatment"] == "categorical" and types["treatment"] == "keyword"
    assert kinds["atlas_structure_acronym"] == "categorical"
    assert kinds["x_raw"] == "numeric" and types["x_raw"] in ("long", "float")
    # header order matches row order
    names = [col["name"] for col in data["columns"]]
    assert names == ["treatment", "atlas_structure_acronym", "metadata",
                     "x_raw", "y_raw", "z_raw"]
    assert len(data["rows"][0]) == len(names)


def test_rows_route_pagination(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    first = dashboard_client.post(ROWS_URL % ("iana/" + owned_dataset), json={"limit": 25})
    second = dashboard_client.post(
        ROWS_URL % ("iana/" + owned_dataset), json={"offset": 25, "limit": 25})
    assert first.status_code == 200 and second.status_code == 200
    assert len(first.get_json()["rows"]) == 25
    assert second.get_json()["offset"] == 25
    assert first.get_json()["rows"][0] != second.get_json()["rows"][0]


def test_rows_route_limit_capped(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    response = dashboard_client.post(
        ROWS_URL % ("iana/" + owned_dataset), json={"limit": 5000})
    assert response.status_code == 200
    assert response.get_json()["limit"] == 1000  # ROWS_PAGE_CAP


def test_rows_route_filters_applied(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    response = dashboard_client.post(ROWS_URL % ("iana/" + owned_dataset), json={
        "filter": {"categorical": {"treatment": ["ctrl"]},
                   "continuous": {"x_raw": [0, 10]}}})
    data = response.get_json()
    assert response.status_code == 200
    assert data["total"] == 11  # x_raw 0..10 step 0.5, ctrl only
    assert all(row[0] == "ctrl" for row in data["rows"])


def test_rows_route_full_range_filter_ignored(dashboard_client, dashboard_login,
                                              parquet_backend, nulls_dataset):
    """Sending the untouched full-range slider values must not filter (the
    NULL row stays visible)."""
    dashboard_login("iana")
    meta = parquet_backend.get_meta(nulls_dataset, "iana")
    low, high = meta["continuous"]["x_raw"]
    response = dashboard_client.post(ROWS_URL % ("iana/" + nulls_dataset), json={
        "filter": {"categorical": {"treatment": []},
                   "continuous": {"x_raw": [low, high]}}})
    assert response.get_json()["total"] == 60


def test_rows_route_invalid_payload(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    for body in ({"offset": -1}, {"offset": "x"}, {"limit": "x"}, None):
        response = dashboard_client.post(ROWS_URL % ("iana/" + owned_dataset), json=body)
        assert response.status_code == 400, body
    response = dashboard_client.post(
        ROWS_URL % ("iana/" + owned_dataset), json={"filter": {"continuous": {"x_raw": [1]}}})
    assert response.status_code == 400


def test_rows_route_unknown_dataset(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.post(ROWS_URL % "iana/ghost", json={})
    assert response.status_code == 400
    # ownerless identifiers are admin-only (parity with the delete route)
    response = dashboard_client.post(ROWS_URL % "ghost", json={})
    assert response.status_code == 403


def test_rows_route_ownership(dashboard_client, dashboard_login,
                              parquet_backend, owned_dataset):
    dashboard_login("mallory")
    response = dashboard_client.post(ROWS_URL % ("iana/" + owned_dataset), json={})
    assert response.status_code == 403


def test_rows_route_login_required(dashboard_app, parquet_backend, owned_dataset):
    client = dashboard_app.test_client()
    response = client.post(ROWS_URL % ("iana/" + owned_dataset), json={})
    assert response.status_code == 401


# -- Elasticsearch parity (fake ES client) ------------------------------------


def test_es_get_rows_parity_with_parquet(parquet_backend, es_backend,
                                         owned_dataset, es_dataset):
    r_pq = parquet_backend.get_rows(owned_dataset, offset=0, limit=50, owner="iana")
    r_es = es_backend.get_rows(es_dataset, offset=0, limit=50, owner="iana")
    assert r_es["columns"] == r_pq["columns"]
    assert r_es["total"] == r_pq["total"] == 60
    assert r_es["rows"] == r_pq["rows"]


def test_es_get_rows_offset_and_filters(es_backend, es_dataset):
    second = es_backend.get_rows(es_dataset, offset=50, limit=50, owner="iana")
    assert len(second["rows"]) == 10 and second["total"] == 60
    filtered = es_backend.get_rows(
        es_dataset, owner="iana", filters=[CategoricalFilter("treatment", ["ctrl"])])
    assert filtered["total"] == 30
    assert all(row[0] == "ctrl" for row in filtered["rows"])


def test_es_get_rows_full_range_ignored(es_backend, parquet_backend, es_dataset,
                                        owned_dataset):
    meta = parquet_backend.get_meta(owned_dataset, "iana")
    low, high = meta["continuous"]["x_raw"]
    result = es_backend.get_rows(
        es_dataset, owner="iana", filters=[ContinuousFilter("x_raw", low, high)])
    assert result["total"] == 60


def test_es_get_rows_unknown_field_and_missing(es_backend, es_dataset):
    from data_dashboard.backends.base import UnknownDatasetError
    with pytest.raises(UnknownDatasetError):
        es_backend.get_rows(es_dataset, owner="iana",
                            filters=[CategoricalFilter("nope", ["x"])])
    with pytest.raises(UnknownDatasetError):
        es_backend.get_rows("ghost", owner="iana")


def test_es_get_rows_uses_count_and_hits_search(es_backend, es_dataset):
    es_backend.get_rows(es_dataset, offset=0, limit=10, owner="iana")
    searches = [body for _, body in es_backend.es.search_calls]
    assert any(
        body.get("from") == 0 and body.get("size") == 10 and "aggs" not in body
        for body in searches
    ), "spreadsheet search must be a plain from/size hits query"
