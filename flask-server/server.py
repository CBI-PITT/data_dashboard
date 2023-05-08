import json

import pandas as pd
from flask import Flask, jsonify

from utils import NumpyEncoder


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/data')
def get_data():
    data = {
        "cells": [587, 3336, 411, 175, 73, 808, 29, 275, 44404, 4146, 101, 987, 797, 41, 46, 2775, 347, 131, 212, 4241, 711, 233, 378, 4230, 800, 76, 1131, 999]
    }
    return jsonify(data)


@app.route('/api/filters')
def get_filters():
    """
    response format:
    {
        "categorical": { "Treatment": ["eeev", "veev","weev"], "Time_point": [24, 48, 72, 96],"Route": ['subcutaneous'] },
        "continuous": { "Age": { "min": 0.5, "max": 5 },"Metadata":{"min":1,"max":29} }
    }
    # TODO: join with cels table
    """
    data = {}
    categorical = {}
    continuous = {}
    # cells_csv = 'Integrated.csv'
    metadata_csv = 'metadata.csv'
    # cells_df = pd.read_csv(cells_csv)
    metadata_df = pd.read_csv(metadata_csv)
    metadata_df = metadata_df.dropna(axis=1, how='all')
    continuous_dtypes = metadata_df.select_dtypes(include='number')
    categorical_dtypes = metadata_df.select_dtypes(exclude='number')
    continuous_columns = continuous_dtypes.columns.to_list()
    if 'id' in continuous_columns:
        continuous_columns.remove('id')
    for column in continuous_columns:
        column_data = pd.to_numeric(metadata_df[column])
        if len(column_data.unique()) > 1:
            continuous[column] = {"min": column_data.min(), "max": column_data.max()}
    categorical_columns = categorical_dtypes.columns.to_list()
    if 'uuid' in categorical_columns:
        categorical_columns.remove('uuid')
    if 'file_path' in categorical_columns:
        categorical_columns.remove('file_path')
    for column in categorical_columns:
        unique_values = list(metadata_df[column].unique())
        if len(unique_values) > 1:
            categorical[column] = unique_values
    data['categorical'] = categorical
    data['continuous'] = continuous
    data_str = json.dumps(
        data, indent=4, sort_keys=True,
        separators=(', ', ': '), ensure_ascii=False,
        cls=NumpyEncoder
    )
    return data_str


@app.route('/api/get-xy')
def get_axis_options():
    """
    response format:
    {"data": ["id", "time_point", "structure_id"]}
    :return: list of column names from the metadata table
    # TODO: join with cels table
    """
    data = {}
    metadata_csv = 'metadata.csv'
    metadata_df = pd.read_csv(metadata_csv)
    metadata_df = metadata_df.dropna(axis=1, how='all')
    data['data'] = metadata_df.columns.to_list()
    return jsonify(data)


@app.route('/api/get-group-by')
def get_group_by_options():
    """
    response format:
    {"data": ["id", "time_point", "structure_id"]}
    :return: list of column names from the metadata table
    # TODO: join with cels table
    """
    data = {}
    metadata_csv = 'metadata.csv'
    metadata_df = pd.read_csv(metadata_csv)
    metadata_df = metadata_df.dropna(axis=1, how='all')
    data['data'] = metadata_df.columns.to_list()
    return jsonify(data)


@app.route('/api/get-aggregate')
def get_aggregate_options():
    """
    response format:
    {"data": ["count of distinct", "count of all", "total sum", "average", "min", "max"]}
    """
    data = {"data": ["count of distinct", "count of all", "total sum", "average", "min", "max"]}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
