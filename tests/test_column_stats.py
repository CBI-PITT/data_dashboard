"""Column statistics endpoint + backend get_column_stats coverage.

The spreadsheet's numiqo-style column picker shows type-colored column names
below the table; clicking one computes its descriptive stats. Numeric columns
report min/max/mean/median/q25/q75/std (NULLs ignored, valid/missing counted),
categorical columns report a frequency table (top COLUMN_STATS_VALUE_CAP
values by occurrences, fraction relative to the non-null values), dates report
min/max/count.
"""

import math

import pytest

from data_dashboard.backends.base import UnknownDatasetError

STATS_URL = "/dashboard/api/datasets/%s/column_stats"


@pytest.fixture()
def owned_dataset(parquet_backend, cells_csv):
    """cells_csv: 60 rows, treatment 30/30, acronyms 20/20/20, x_raw = i*0.5."""
    return parquet_backend.create_dataset("job_0101_cells", cells_csv, owner="iana")


@pytest.fixture()
def es_dataset(es_backend, cells_csv):
    return es_backend.create_dataset("job_0101_cells", cells_csv, owner="iana")


@pytest.fixture()
def nulls_dataset(parquet_backend, tmp_path):
    """59 numeric values + one NULL in a numeric and one in a categorical
    column: NULLs are ignored by the aggregates and counted as missing."""
    path = tmp_path / "nulls.csv"
    lines = ["treatment,x_raw"]
    for i in range(59):
        lines.append("%s,%f" % (["ctrl", "stim"][i % 2], i * 1.0))
    lines.append(",,")  # NULL treatment AND NULL x_raw
    path.write_text("\n".join(lines) + "\n")
    return parquet_backend.create_dataset("nulls", str(path), owner="iana")


# -- ParquetBackend.get_column_stats ------------------------------------------


def test_numeric_stats_known_values(parquet_backend, owned_dataset):
    result = parquet_backend.get_column_stats(owned_dataset, "x_raw", owner="iana")
    assert result["column"] == "x_raw"
    assert result["kind"] == "numeric" and result["type"] in ("long", "float")
    s = result["stats"]
    xs = [i * 0.5 for i in range(60)]
    mean = sum(xs) / len(xs)
    std = math.sqrt(sum((v - mean) ** 2 for v in xs) / (len(xs) - 1))
    assert abs(s["min"] - 0.0) < 1e-9
    assert abs(s["max"] - 29.5) < 1e-9
    assert abs(s["mean"] - mean) < 1e-9
    assert abs(s["median"] - 14.75) < 1e-9
    assert abs(s["q25"] - 7.375) < 1e-9
    assert abs(s["q75"] - 22.125) < 1e-9
    assert abs(s["std"] - std) < 1e-6
    assert s["valid"] == 60 and s["missing"] == 0 and s["total"] == 60


def test_numeric_stats_ignore_nulls(parquet_backend, nulls_dataset):
    result = parquet_backend.get_column_stats(nulls_dataset, "x_raw", owner="iana")
    s = result["stats"]
    assert abs(s["min"] - 0.0) < 1e-9 and abs(s["max"] - 58.0) < 1e-9
    assert abs(s["median"] - 29.0) < 1e-9
    assert abs(s["q25"] - 14.5) < 1e-9 and abs(s["q75"] - 43.5) < 1e-9
    assert s["valid"] == 59 and s["missing"] == 1 and s["total"] == 60


def test_categorical_frequency_table(parquet_backend, owned_dataset):
    result = parquet_backend.get_column_stats(
        owned_dataset, "treatment", owner="iana")
    assert result["kind"] == "categorical" and result["type"] == "keyword"
    assert len(result["values"]) == 2
    counts = {v["value"]: v["count"] for v in result["values"]}
    assert counts == {"ctrl": 30, "stim": 30}
    assert all(abs(v["fraction"] - 0.5) < 1e-9 for v in result["values"])
    assert result["distinct"] == 2
    assert result["missing"] == 0 and result["total"] == 60
    assert result["truncated"] is False
    # ordered by occurrences desc, value asc
    counts_in_order = [v["count"] for v in result["values"]]
    assert counts_in_order == sorted(counts_in_order, reverse=True)


def test_categorical_fraction_relative_to_non_null(parquet_backend, nulls_dataset):
    """A NULL in the categorical column is missing; fractions are relative to
    the non-null values (they sum to 1 across the listed values)."""
    result = parquet_backend.get_column_stats(nulls_dataset, "treatment", owner="iana")
    assert result["missing"] == 1 and result["total"] == 60
    non_null = result["total"] - result["missing"]
    assert non_null == 59
    fraction_sum = sum(v["fraction"] for v in result["values"])
    assert abs(fraction_sum - 1.0) < 1e-9
    assert all(abs(v["fraction"] - v["count"] / non_null) < 1e-9
               for v in result["values"])


def test_categorical_truncated_to_cap(parquet_backend, tmp_path):
    path = tmp_path / "many.csv"
    lines = ["grp,n"]
    for i in range(150):
        lines.append("g%d,%d" % (i, i + 1))
    path.write_text("\n".join(lines) + "\n")
    name = parquet_backend.create_dataset("many", str(path), owner="iana")
    result = parquet_backend.get_column_stats(name, "grp", owner="iana")
    from data_dashboard.backends.parquet import COLUMN_STATS_VALUE_CAP
    assert len(result["values"]) == COLUMN_STATS_VALUE_CAP == 100
    assert result["distinct"] == 150
    assert result["truncated"] is True
    # top values by occurrences (each once here), value asc tie-break
    assert result["values"][0]["count"] == 1


def test_date_stats_min_max_only(parquet_backend, tmp_path):
    path = tmp_path / "dates.csv"
    lines = ["day,value"]
    for i in range(10):
        lines.append("2026-01-%02d,%d" % (i + 1, i))
    path.write_text("\n".join(lines) + "\n")
    name = parquet_backend.create_dataset("dates", str(path), owner="iana")
    result = parquet_backend.get_column_stats(name, "day", owner="iana")
    assert result["kind"] == "date"
    s = result["stats"]
    assert s["min"] == "2026-01-01" and s["max"] == "2026-01-10"
    assert "std" not in s and "q25" not in s
    assert s["valid"] == 10 and s["missing"] == 0


def test_boolean_column_is_categorical(parquet_backend, tmp_path):
    path = tmp_path / "bools.csv"
    lines = ["flag,value"]
    for i in range(10):
        lines.append("%s,%d" % (["true", "false"][i % 2], i))
    path.write_text("\n".join(lines) + "\n")
    name = parquet_backend.create_dataset("bools", str(path), owner="iana")
    result = parquet_backend.get_column_stats(name, "flag", owner="iana")
    assert result["kind"] == "categorical"
    # DuckDB BOOLEAN arrives as Python bools (JSON true/false for the UI)
    counts = {str(v["value"]).lower(): v["count"] for v in result["values"]}
    assert counts == {"false": 5, "true": 5}


def test_unknown_column_and_dataset(parquet_backend, owned_dataset):
    with pytest.raises(UnknownDatasetError):
        parquet_backend.get_column_stats(owned_dataset, "nope", owner="iana")
    with pytest.raises(UnknownDatasetError):
        parquet_backend.get_column_stats("ghost", "x_raw", owner="iana")


# -- /api/datasets/<identifier>/column_stats route -----------------------------


def test_stats_route_happy_path(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    response = dashboard_client.post(
        STATS_URL % ("iana/" + owned_dataset), json={"column": "x_raw"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["column"] == "x_raw" and data["kind"] == "numeric"
    assert data["stats"]["valid"] == 60
    response = dashboard_client.post(
        STATS_URL % ("iana/" + owned_dataset), json={"column": "treatment"})
    data = response.get_json()
    assert response.status_code == 200 and data["kind"] == "categorical"
    assert {v["value"]: v["count"] for v in data["values"]} == {
        "ctrl": 30, "stim": 30}


def test_stats_route_invalid_payload(dashboard_client, dashboard_login, owned_dataset):
    dashboard_login("iana")
    for body in ({}, {"column": ""}, {"column": 123}, None):
        response = dashboard_client.post(
            STATS_URL % ("iana/" + owned_dataset), json=body)
        assert response.status_code == 400, body
    response = dashboard_client.post(
        STATS_URL % ("iana/" + owned_dataset), json={"column": "nope"})
    assert response.status_code == 400


def test_stats_route_unknown_dataset(dashboard_client, dashboard_login):
    dashboard_login("iana")
    response = dashboard_client.post(
        STATS_URL % "iana/ghost", json={"column": "x_raw"})
    assert response.status_code == 400
    # ownerless identifiers are admin-only (parity with the other routes)
    response = dashboard_client.post(
        STATS_URL % "ghost", json={"column": "x_raw"})
    assert response.status_code == 403


def test_stats_route_ownership(dashboard_client, dashboard_login,
                               parquet_backend, owned_dataset):
    dashboard_login("mallory")
    response = dashboard_client.post(
        STATS_URL % ("iana/" + owned_dataset), json={"column": "x_raw"})
    assert response.status_code == 403


def test_stats_route_login_required(dashboard_app, parquet_backend, owned_dataset):
    client = dashboard_app.test_client()
    response = client.post(
        STATS_URL % ("iana/" + owned_dataset), json={"column": "x_raw"})
    assert response.status_code == 401


# -- Elasticsearch parity (fake ES client) -------------------------------------


def test_es_numeric_stats_parity(parquet_backend, es_backend,
                                 owned_dataset, es_dataset):
    r_pq = parquet_backend.get_column_stats(owned_dataset, "x_raw", owner="iana")
    r_es = es_backend.get_column_stats(es_dataset, "x_raw", owner="iana")
    for key in ("min", "max", "mean", "median", "q25", "q75", "std"):
        assert abs(r_es["stats"][key] - r_pq["stats"][key]) < 1e-6, key
    assert r_es["stats"]["valid"] == r_pq["stats"]["valid"] == 60
    assert r_es["stats"]["missing"] == r_pq["stats"]["missing"] == 0
    assert r_es["kind"] == r_pq["kind"] == "numeric"


def test_es_categorical_stats_parity(parquet_backend, es_backend,
                                     owned_dataset, es_dataset):
    r_pq = parquet_backend.get_column_stats(owned_dataset, "treatment", owner="iana")
    r_es = es_backend.get_column_stats(es_dataset, "treatment", owner="iana")
    assert {v["value"]: v["count"] for v in r_es["values"]} == \
        {v["value"]: v["count"] for v in r_pq["values"]}
    assert all(abs(a["fraction"] - b["fraction"]) < 1e-9
               for a, b in zip(r_es["values"], r_pq["values"]))
    assert r_es["kind"] == r_pq["kind"] == "categorical"
    assert r_es["missing"] == r_pq["missing"] == 0


def test_es_truncated_flag_uses_other_doc_count(es_backend, tmp_path):
    path = tmp_path / "many.csv"
    lines = ["grp,n"]
    for i in range(150):
        lines.append("g%d,%d" % (i, i + 1))
    path.write_text("\n".join(lines) + "\n")
    name = es_backend.create_dataset("many", str(path), owner="iana")
    result = es_backend.get_column_stats(name, "grp", owner="iana")
    from data_dashboard.backends.elasticsearch import COLUMN_STATS_VALUE_CAP
    assert len(result["values"]) == COLUMN_STATS_VALUE_CAP
    assert result["truncated"] is True
    assert result["distinct"] == 150


def test_es_numeric_stats_body_contract(es_backend, es_dataset):
    """One search carries extended_stats + percentiles; categorical carries
    terms + cardinality."""
    es_backend.es.search_calls = []
    es_backend.get_column_stats(es_dataset, "x_raw", owner="iana")
    bodies = [body for _, body in es_backend.es.search_calls]
    assert any(
        "extended_stats" in ((body.get("aggs") or {}).get("col_stats") or {})
        for body in bodies
    ), "numeric stats must use extended_stats"
    assert any(
        "col_percentiles" in (body.get("aggs") or {}) for body in bodies
    ), "numeric stats must use percentiles"

    es_backend.es.search_calls = []
    es_backend.get_column_stats(es_dataset, "treatment", owner="iana")
    bodies = [body for _, body in es_backend.es.search_calls]
    terms_body = next(
        body for body in bodies
        if "treatment" in (body.get("aggs") or {})
        and "terms" in body["aggs"]["treatment"]
    )
    assert "cardinality" in terms_body["aggs"]["distinct"]
    assert terms_body["aggs"]["treatment"]["terms"]["size"] == 100
