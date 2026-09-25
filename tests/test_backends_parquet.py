"""ParquetBackend (DuckDB) tests: ingest, the quoted-CSV regression, and the
full query matrix."""

import json
import os

import pytest

from conftest import make_settings

from data_dashboard.backends import get_backend
from data_dashboard.backends.base import (
    Aggregate,
    CategoricalFilter,
    ContinuousFilter,
    QuerySpec,
    load_meta,
)
from data_dashboard.utils import sanitize_dataset_name


def ingest_cells(backend, cells_csv):
    """Ingest like the add_csv route does: dataset name from the basename."""
    import os
    from data_dashboard.utils import sanitize_dataset_name
    name = sanitize_dataset_name(os.path.basename(cells_csv))
    backend.create_dataset(name, cells_csv)
    return name


# -- ingestion ---------------------------------------------------------------


def test_create_dataset_writes_parquet_and_sidecar(parquet_backend, cells_csv, datasets_dir):
    name = ingest_cells(parquet_backend, cells_csv)
    assert name == "job_0101_cells"
    parquet_path = os.path.join(datasets_dir, name + ".parquet")
    meta_path = os.path.join(datasets_dir, name + ".dashboard_meta.json")
    assert os.path.isfile(parquet_path)
    assert os.path.isfile(meta_path)
    meta = load_meta(datasets_dir, name)
    assert meta["backend"] == "parquet"
    assert meta["row_count"] == 60


def test_dtype_inference(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    fields = parquet_backend.get_field_types("job_0101_cells")
    assert fields["treatment"] == "keyword"
    assert fields["atlas_structure_acronym"] == "keyword"
    assert fields["metadata"] == "long"
    assert fields["x_raw"] == "float"
    assert fields["y_raw"] == "float"


def test_categorical_and_continuous_cache(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    categorical, continuous = parquet_backend.get_filter_values("job_0101_cells")
    assert categorical["treatment"] == ["ctrl", "stim"]
    assert categorical["atlas_structure_acronym"] == ["CTX", "grey", "root"]
    assert continuous["x_raw"] == [0.0, 29.5]
    assert continuous["metadata"] == [0, 2]


def test_list_datasets_and_exists_and_delete(parquet_backend, cells_csv):
    parquet_backend.create_dataset("alpha", cells_csv)
    parquet_backend.create_dataset("beta", cells_csv)
    assert parquet_backend.list_datasets() == ["alpha", "beta"]
    assert parquet_backend.dataset_exists("alpha")
    parquet_backend.delete_dataset("alpha")
    assert not parquet_backend.dataset_exists("alpha")
    assert parquet_backend.list_datasets() == ["beta"]


def test_sanitize_dataset_name():
    assert sanitize_dataset_name("/a/b/cells.csv") == "cells"
    assert sanitize_dataset_name("Cells Data (v2).csv") == "Cells_Data_v2"
    assert sanitize_dataset_name("job_0101_df.csv") == "job_0101_df"
    with pytest.raises(ValueError):
        sanitize_dataset_name(".csv")
    with pytest.raises(ValueError):
        sanitize_dataset_name("///")


# -- quoted-CSV regression (the production add_csv 500) ----------------------


def test_quoted_field_beyond_sniffer_sample(parquet_backend, big_quoted_csv):
    """DuckDB's sniffer samples only the first 20480 rows to detect the quote
    character; quoted fields later in the file misparse without explicit
    CSV_OPTIONS (quote='"', escape='"', sample_size=-1)."""
    name = parquet_backend.create_dataset("quoted_cells", big_quoted_csv)
    fields = parquet_backend.get_field_types(name)
    assert fields["atlas_structure_number"] == "long"
    assert fields["atlas_structure_name"] == "keyword"
    categorical, continuous = parquet_backend.get_filter_values(name)
    assert "RSPd1" in categorical["atlas_structure_acronym"]
    assert '" layer 1"' not in [v for v in categorical["atlas_structure_name"]]
    buckets = parquet_backend.query(QuerySpec(
        dataset=name, field="x_raw", filters=[],
        group_by=["atlas_structure_acronym"],
        aggregates=[Aggregate("avg", "x_raw")]))
    rsp = [b for b in buckets if b["key"]["atlas_structure_acronym"] == "RSPd1"]
    assert rsp and rsp[0]["avg_x_raw"]["value"] == 55.5


# -- querying ----------------------------------------------------------------


def test_query_bucket_shape_parity(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw", filters=[],
        group_by=["treatment"],
        aggregates=[Aggregate("avg", "x_raw"), Aggregate("value_count", "x_raw")]))
    assert buckets[0]["doc_count"] == 30
    assert buckets[0]["key"] == {"treatment": "ctrl"}
    assert isinstance(buckets[0]["avg_x_raw"]["value"], float)
    assert buckets[0]["value_count_x_raw"]["value"] == 30


def test_query_categorical_filter(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw",
        filters=[CategoricalFilter("treatment", ["stim"])],
        group_by=["treatment"], aggregates=[Aggregate("value_count", "x_raw")]))
    assert len(buckets) == 1
    assert buckets[0]["key"]["treatment"] == "stim"
    assert buckets[0]["value_count_x_raw"]["value"] == 30


def test_query_empty_categorical_selection_means_no_filter(parquet_backend, cells_csv):
    """ES empty-should parity: untouched categorical fields arrive as [] and
    must not filter anything."""
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw",
        filters=[CategoricalFilter("treatment", [])],
        group_by=["treatment"], aggregates=[Aggregate("value_count", "x_raw")]))
    assert sorted(b["key"]["treatment"] for b in buckets) == ["ctrl", "stim"]


def test_query_continuous_filter(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw",
        filters=[ContinuousFilter("x_raw", 0.0, 10.0)],
        group_by=["treatment"], aggregates=[Aggregate("value_count", "x_raw")]))
    total = sum(b["doc_count"] for b in buckets)
    assert total == 21  # x_raw = i*0.5 <= 10 -> i <= 20 -> 21 rows of 60
    for b in buckets:
        assert b["key"]["treatment"] in ("ctrl", "stim")


def test_query_all_aggregates_and_boxplot_shape(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw", filters=[],
        group_by=["treatment"],
        aggregates=[
            Aggregate("min", "x_raw"), Aggregate("max", "x_raw"),
            Aggregate("avg", "x_raw"), Aggregate("sum", "x_raw"),
            Aggregate("value_count", "x_raw"), Aggregate("cardinality", "x_raw"),
            Aggregate("boxplot", "x_raw"),
        ]))
    b = buckets[0]
    assert b["min_x_raw"]["value"] == 0.0
    assert b["max_x_raw"]["value"] == 29.0  # ctrl rows: i even -> max i=58
    assert b["sum_x_raw"]["value"] == sum(0.5 * i for i in range(0, 60, 2))
    assert b["cardinality_x_raw"]["value"] == 30
    box = b["boxplot_x_raw"]
    assert sorted(box.keys()) == ["max", "min", "q1", "q2", "q3"]
    assert box["min"] <= box["q1"] <= box["q2"] <= box["q3"] <= box["max"]


def test_query_n_aggregation(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    buckets = parquet_backend.query(QuerySpec(
        dataset="job_0101_cells", field="x_raw", filters=[],
        group_by=["atlas_structure_acronym"],
        aggregates=[Aggregate("avg", "x_raw")], n_field="treatment"))
    # every acronym group contains both treatments
    assert all(b["N"]["value"] == 2 for b in buckets)


def test_query_null_group_keys_excluded(parquet_backend, datasets_dir):
    csv_path = os.path.join(datasets_dir, "with_nulls.csv")
    with open(csv_path, "w") as fh:
        fh.write("treatment,x_raw\nctrl,1.0\nctrl,2.0\n,3.0\n")
    parquet_backend.create_dataset("with_nulls", csv_path)
    buckets = parquet_backend.query(QuerySpec(
        dataset="with_nulls", field="x_raw", filters=[],
        group_by=["treatment"], aggregates=[Aggregate("value_count", "x_raw")]))
    assert len(buckets) == 1  # NULL group key skipped, like ES composite terms
    assert buckets[0]["key"]["treatment"] == "ctrl"


def test_query_unknown_dataset_and_field(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    with pytest.raises(Exception):
        parquet_backend.query(QuerySpec(
            dataset="missing", field="x_raw", filters=[], group_by=["treatment"],
            aggregates=[Aggregate("avg", "x_raw")]))
    with pytest.raises(Exception):
        parquet_backend.query(QuerySpec(
            dataset="job_0101_cells", field="x_raw", filters=[], group_by=["nope"],
            aggregates=[Aggregate("avg", "x_raw")]))


def test_query_numeric_agg_on_keyword_field_rejected(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    with pytest.raises(ValueError):
        parquet_backend.query(QuerySpec(
            dataset="job_0101_cells", field="treatment", filters=[],
            group_by=["treatment"], aggregates=[Aggregate("avg", "treatment")]))


def test_get_status(parquet_backend, cells_csv):
    ingest_cells(parquet_backend, cells_csv)
    status = parquet_backend.get_status("job_0101_cells")
    assert status["health"] == "green"
    assert status["status"] == "open"
    assert status["storage_size"].endswith(("b", "kb", "mb", "gb", "tb"))
    assert status["docs_count"] == "60"


# -- backend selection -------------------------------------------------------


def test_get_backend_selects_parquet(datasets_dir, settings):
    backend = get_backend(settings)
    assert backend.name == "parquet"
    assert str(backend.datasets_dir) == str(datasets_dir)


def test_get_backend_unknown_name(tmp_path, settings):
    settings.set("dashboard", "backend", "clickhouse")
    with pytest.raises(ValueError):
        get_backend(settings)


def test_get_backend_missing_datasets_dir(settings):
    settings.set("dashboard", "datasets_dir", "")
    with pytest.raises(ValueError):
        get_backend(settings)
