"""Shared post-processing over normalized aggregation buckets.

Faithful port of the original dashboard's bp_routes/dashboard.py functions
(density, totalN, totalN_and_std, boxplot_filterOut) operating on the
backend-neutral bucket shape, so responses are identical for every storage
backend. The quirky "acronym_volumn" key is part of the React contract
(Dataset.js reads it) and must stay as-is.
"""

import os
import re

import numpy as np
import pandas as pd

_atlas_volumes = None


def get_acronym_volumes():
    """acronym -> volume_mm dicts for the 10um and 25um allen mouse atlases
    (BrainGlobe output, shipped as package data)."""
    global _atlas_volumes
    if _atlas_volumes is None:
        csv_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'atlas', 'atlas_mouse_acronym_volume.csv')
        df = pd.read_csv(csv_file_path)
        _atlas_volumes = {
            'acronym_volume_10': df.set_index('acronym')['volume_mm_10'].to_dict(),
            'acronym_volume_25': df.set_index('acronym')['volume_mm_25'].to_dict(),
        }
    return _atlas_volumes


def apply_density(json_data, response, agg_list=None):
    """Add density_<field> = <agg> / atlas structure volume per bucket when
    the dataset meta configures it. Port of dashboard.py density()."""
    serialized = json_data.get('serialized_parameters') or {}
    meta_cfg = serialized.get('meta') or {}
    acronym_column = meta_cfg.get('atlas_structure_acronym_column_name')
    agg_condition = meta_cfg.get('aggregation_condition')

    if (json_data.get('field') == acronym_column
            and acronym_column in (json_data.get('group_by') or [])
            and agg_condition in (json_data.get('aggregate') or [])
            and serialized.get('acronym_volumn')):
        field = acronym_column
        agg = agg_condition
        resolution = get_acronym_volumes()[serialized['acronym_volumn']]

        for item in response:
            acronym = item['key'][acronym_column]
            item['density_' + field] = {'value': ''}
            if resolution.get(acronym):
                item['density_' + field]['value'] = (
                    item[agg + '_' + field]['value'] / resolution[acronym]
                )
            else:
                item['density_' + field]['value'] = 0
        if agg_list is not None:
            agg_list.append('density')
    return {'response': response, 'agg_list': agg_list}


def total_n_count(buckets, serialized_parameters):
    """Number of distinct N-field values across buckets. Port of totalN()."""
    n_field = serialized_parameters['meta']['metadata_calculation_name']
    total_n_set = set()
    for bucket in buckets:
        total_n_set.add(bucket['key'][n_field])
    return len(total_n_set)


def total_n_and_std(buckets_added, buckets, agg_original, groupby_original,
                    field, serialized_parameters):
    """Per-group mean/std when the N field is not part of group_by. Port of
    totalN_and_std()."""
    dict_std = {}
    for bucket in buckets_added:
        string_groupby = '|'.join(
            str(bucket['key'].get(gb, '')) for gb in groupby_original)
        if string_groupby not in dict_std:
            dict_std[string_groupby] = {agg + '_' + field: [] for agg in agg_original}
        for agg in agg_original:
            dict_std[string_groupby][agg + '_' + field].append(
                bucket[agg + '_' + field]['value'])

    n_field = serialized_parameters['meta']['metadata_calculation_name']
    total_n_set = {bucket['key'][n_field] for bucket in buckets_added}
    total_n = len(total_n_set)

    for bucket in buckets:
        string_groupby = '|'.join(
            str(bucket['key'].get(gb, '')) for gb in groupby_original)
        for agg in agg_original:
            std_values = dict_std.get(string_groupby, {}).get(agg + '_' + field)
            bucket['avg_' + agg + '_' + field] = {
                'value': bucket[agg + '_' + field]['value'] / bucket['N']['value'],
                # standard error of the mean across N groups
                'std': (
                    np.std(std_values) / np.sqrt(len(std_values))
                    if std_values
                    else None
                ),
            }
    return {'response': buckets, 'total_n': total_n}


def boxplot_filter_out(agg_list):
    """The UI requests boxplot for numeric fields; the boxplot values stay in
    the bucket data but the plain agg name must leave the agg_list."""
    return [s for s in agg_list if not re.match(r'^boxplot', s, re.IGNORECASE)]
