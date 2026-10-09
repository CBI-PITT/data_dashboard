"""Translate the dashboard UI's query JSON into a backend-neutral QuerySpec.

The payload shape is the Form.js POST contract:

    {
      "INDEX": "<dataset name>",
      "field": "<aggregate field>",
      "filter": {
        "categorical": {"<field>": [<value>, ...], ...},
        "continuous":  {"<field>": [<min>, <max>], ...}
      },
      "group_by": ["<field>", ...],
      "aggregate": ["min"|"max"|"avg"|"sum"|"value_count"|"cardinality"|"boxplot", ...],
      "serialized_parameters": {"meta": {...}, ...}     # session copy of /meta
    }
"""

from .backends.base import (
    AGGREGATES,
    Aggregate,
    CategoricalFilter,
    ContinuousFilter,
    QuerySpec,
)


def parse_filters(filters):
    """Parse the Form.js `filter` dict ({categorical, continuous}) into a
    list of backend filter dataclasses. Shared by /api/query and the rows
    endpoint. Raises ValueError for malformed payloads."""
    if not isinstance(filters, dict):
        raise ValueError("'filter' must be an object")
    parsed_filters = []

    categorical = filters.get('categorical') or {}
    if not isinstance(categorical, dict):
        raise ValueError("'filter.categorical' must be an object")
    for name, values in categorical.items():
        if values is None:
            continue
        if not isinstance(values, list):
            raise ValueError("Categorical filter for %r must be a list" % (name,))
        parsed_filters.append(CategoricalFilter(field=str(name), values=values))

    continuous = filters.get('continuous') or {}
    if not isinstance(continuous, dict):
        raise ValueError("'filter.continuous' must be an object")
    for name, bounds in continuous.items():
        if not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            raise ValueError("Continuous filter for %r must be [min, max]" % (name,))
        if bounds[0] is None and bounds[1] is None:
            continue
        try:
            low = float(bounds[0]) if bounds[0] is not None else None
            high = float(bounds[1]) if bounds[1] is not None else None
        except (TypeError, ValueError):
            raise ValueError("Continuous filter for %r must have numeric bounds" % (name,))
        parsed_filters.append(ContinuousFilter(field=str(name), min=low, max=high))
    return parsed_filters


def parse_query_json(json_data, include_n_field=False):
    """Build a QuerySpec from the UI payload. Raises ValueError for malformed
    payloads. Unknown dataset/field names are rejected later by the backend
    against the dataset's own schema."""
    if not isinstance(json_data, dict):
        raise ValueError('Query payload must be a JSON object')

    dataset = json_data.get('INDEX')
    if not dataset or not isinstance(dataset, str):
        raise ValueError("Query payload must include an 'INDEX' dataset name")

    field = json_data.get('field')
    if not field or not isinstance(field, str):
        raise ValueError("Query payload must include a 'field' name")

    parsed_filters = parse_filters(json_data.get('filter') or {})

    group_by = json_data.get('group_by') or []
    if not isinstance(group_by, list) or not all(isinstance(g, str) for g in group_by):
        raise ValueError("'group_by' must be a list of field names")

    aggregates = []
    for agg_name in json_data.get('aggregate') or []:
        if agg_name not in AGGREGATES:
            raise ValueError('Unsupported aggregate: %r' % (agg_name,))
        aggregates.append(Aggregate(name=agg_name, field=field))

    n_field = None
    if include_n_field:
        serialized = json_data.get('serialized_parameters') or {}
        if not isinstance(serialized, dict):
            raise ValueError("'serialized_parameters' must be an object")
        meta_cfg = serialized.get('meta') or {}
        n_field = meta_cfg.get('metadata_calculation_name')

    return QuerySpec(
        dataset=dataset,
        field=field,
        filters=parsed_filters,
        group_by=[str(g) for g in group_by],
        aggregates=aggregates,
        n_field=n_field,
    )
