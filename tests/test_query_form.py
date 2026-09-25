"""query_form.parse_query_json: the React Form.js POST contract -> QuerySpec."""

import pytest

from data_dashboard.query_form import parse_query_json


def full_payload(**overrides):
    payload = {
        "INDEX": "klimstra5.0",
        "field": "x_raw",
        "filter": {
            "categorical": {"treatment": ["ctrl", "stim"]},
            "continuous": {"x_raw": [0.0, 10.0], "y_raw": [None, None]},
        },
        "group_by": ["treatment"],
        "aggregate": ["avg", "boxplot"],
    }
    payload.update(overrides)
    return payload


def test_parse_full_payload():
    spec = parse_query_json(full_payload())
    assert spec.dataset == "klimstra5.0"
    assert spec.field == "x_raw"
    assert spec.group_by == ["treatment"]
    kinds = {(type(f).__name__, f.field) for f in spec.filters}
    assert ("CategoricalFilter", "treatment") in kinds
    assert ("ContinuousFilter", "x_raw") in kinds
    names = [a.name for a in spec.aggregates]
    assert names == ["avg", "boxplot"]
    assert all(a.field == "x_raw" for a in spec.aggregates)
    assert spec.n_field is None  # not requested without include_n_field


def test_parse_all_none_continuous_bounds_skipped():
    payload = full_payload(filter={"continuous": {"y_raw": [None, None]}})
    spec = parse_query_json(payload)
    assert spec.filters == []


def test_parse_include_n_field_reads_serialized_parameters():
    payload = full_payload(serialized_parameters={
        "meta": {"metadata_calculation_name": "metadata"}})
    spec = parse_query_json(payload, include_n_field=True)
    assert spec.n_field == "metadata"
    # without the flag the N field stays None even when present
    assert parse_query_json(payload).n_field is None


def test_missing_index_and_field_rejected():
    with pytest.raises(ValueError):
        parse_query_json({"field": "x_raw"})
    with pytest.raises(ValueError):
        parse_query_json({"INDEX": "idx"})


def test_unsupported_aggregate_rejected():
    payload = full_payload(aggregate=["percentile"])
    with pytest.raises(ValueError):
        parse_query_json(payload)


def test_group_by_must_be_string_list():
    with pytest.raises(ValueError):
        parse_query_json(full_payload(group_by=[1, 2]))
    with pytest.raises(ValueError):
        parse_query_json(full_payload(group_by="treatment"))


def test_malformed_filters_rejected():
    with pytest.raises(ValueError):
        parse_query_json(full_payload(filter={"categorical": {"t": "ctrl"}}))
    with pytest.raises(ValueError):
        parse_query_json(full_payload(filter={"continuous": {"x": [1]}}))
    with pytest.raises(ValueError):
        parse_query_json(full_payload(filter={"continuous": {"x": ["a", "b"]}}))


def test_non_dict_payload_rejected():
    with pytest.raises(ValueError):
        parse_query_json([1, 2])
