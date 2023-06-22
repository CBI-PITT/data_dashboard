import json

import pandas as pd
import DSL_Query.DSL_Query as Query
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import NumpyEncoder, merge_cells_and_metadata
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
INDEX = 'klimstra4.0'

app = Flask(__name__)
CORS(app)
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/data")
def get_data():
    data = {
        "cells": [
            587,
            3336,
            411,
            175,
            73,
            808,
            29,
            275,
            44404,
            4146,
            101,
            987,
            797,
            41,
            46,
            2775,
            347,
            131,
            212,
            4241,
            711,
            233,
            378,
            4230,
            800,
            76,
            1131,
            999,
        ]
    }
    return jsonify(data)



@app.route("/api/filters")
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
    metadata_csv = "metadata.csv"
    # cells_df = pd.read_csv(cells_csv)
    metadata_df = pd.read_csv(metadata_csv)
    metadata_df = metadata_df.dropna(axis=1, how="all")
    continuous_dtypes = metadata_df.select_dtypes(include="number")
    categorical_dtypes = metadata_df.select_dtypes(exclude="number")
    continuous_columns = continuous_dtypes.columns.to_list()
    if "id" in continuous_columns:
        continuous_columns.remove("id")
    for column in continuous_columns:
        column_data = pd.to_numeric(metadata_df[column])
        if len(column_data.unique()) > 1:
            continuous[column] = {"min": column_data.min(), "max": column_data.max()}
    categorical_columns = categorical_dtypes.columns.to_list()
    if "uuid" in categorical_columns:
        categorical_columns.remove("uuid")
    if "file_path" in categorical_columns:
        categorical_columns.remove("file_path")
    for column in categorical_columns:
        unique_values = list(metadata_df[column].unique())
        print("column", column)
        for v in unique_values:
            print(v, type(v))
        if len(unique_values) > 1:
            categorical[column] = unique_values
    data["categorical"] = categorical
    data["continuous"] = continuous
    print("Data", data)
    data_str = json.dumps(
        data,
        indent=4,
        sort_keys=True,
        separators=(", ", ": "),
        ensure_ascii=False,
        cls=NumpyEncoder,
    )
    print("Data str", data_str)
    response = jsonify(data_str)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/get-xy")
def get_axis_options():
    """
    response format:
    {"data": ["id", "time_point", "structure_id"]}
    :return: list of column names from the metadata table
    # TODO: join with cels table
    """
    data = {}
    df = merge_cells_and_metadata()
    data["data"] = df.columns.to_list()
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/get-group-by")
def get_group_by_options():
    """
    response format:
    {"data": ["id", "time_point", "structure_id"]}
    :return: list of column names from the metadata table
    # TODO: join with cels table
    """
    data = {}
    df = merge_cells_and_metadata()
    data["data"] = df.columns.to_list()
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/get-aggregate")
def get_aggregate_options():
    """
    response format:
    {"data": ["count of distinct", "count of all", "total sum", "average", "min", "max"]}
    """
    data = {
        "data": [
            "count of distinct",
            "count of all",
            "total sum",
            "average",
            "min",
            "max",
        ]
    }
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/query", methods=["POST"])
def query_data_source():
    """
    request JSON format:
    {
        "x": "<column_name>",
        "y": "<column_name>",
        "filter": {
            "categorical": {"<column_name>": [<value1>, <value2>], "<column_name>": [<value1>, <value2>]},
            "continuous": {"<column_name>": [<min>, <max>], "<column_name>": [<min>, <max>]}
        },
        "group_by": ["<column_name1>", "<column_name2>"],
        "aggregate": <value>
    }

    :return: json with filtered/grouped/aggregated data
    """
    json_data = request.json

    # # Test data
    # json_data = {
    #     # "y": "metadata",
    #     "y": "uuid",
    #     "x": "time_point",
    #     "filter": {
    #         "categorical": {},
    #         "continuous": {}
    #     },
    #     "group_by": ["time_point"],
    #     "aggregate": "count of distinct"
    # }

    # Read the data into a Pandas DataFrame
    data = merge_cells_and_metadata()

    # Get the values from the JSON
    x = json_data["x"]
    y = json_data["y"]
    filter_cat = json_data["filter"]["categorical"]
    filter_cont = json_data["filter"]["continuous"]
    group_by = json_data["group_by"]
    aggregate = json_data["aggregate"]

    # Apply filters to the data
    for column, values in filter_cat.items():
        data = data[data[column].isin(values)]

    for column, (min_val, max_val) in filter_cont.items():
        data = data[(data[column] >= min_val) & (data[column] <= max_val)]

    # Group the data
    data_grouped = data.groupby(group_by)

    # Aggregate the data
    if aggregate == "count of distinct":
        agg_data = data_grouped[y].nunique()
    elif aggregate == "count of all":
        agg_data = data_grouped[y].count()
    elif aggregate == "total sum":
        agg_data = data_grouped[y].sum()
    elif aggregate == "average":
        agg_data = data_grouped[y].mean()
    elif aggregate == "min":
        agg_data = data_grouped[y].min()
    elif aggregate == "max":
        agg_data = data_grouped[y].max()
    group_by_str = ""
    for val in group_by:
        group_by_str = val + "_"

    print(group_by_str)
    print(aggregate)

    # Create a new DataFrame with x, y, and aggregated data
    result = pd.DataFrame({group_by_str: agg_data.index})
    result[aggregate] = agg_data.values

    print("==================Result================", result)

    # Convert the DataFrame to JSON and return it
    data = result.to_json(orient="records")
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

query = Query.Query()
@app.route("/api/test")
def test():
    data = {}
    categorical = {}
    continuous = {}
    
    fileds = list(es.indices.get_mapping(index = INDEX)[INDEX]['mappings']['properties'].keys())
    # print(fileds)
    
    # munually setting cate and conti list
    categorical_list = ['route', 'time_point', 'treatment']
    continuous_list = ['x_raw', 'y_raw', 'z_raw', 'x_transformed', 'y_transformed', 'z_transformed']
    
    for key in categorical_list:
        resp = es.search(index = INDEX, body=query.filterCategorical(key))
        # print(resp.body["aggregations"][key]["buckets"])
        temp_dict = resp.body["aggregations"][key]["buckets"]
        # print (temp_dict[0])
        categorical[key] = []
        for val in temp_dict:
            categorical[key].append(val['key'])
    # print (categorical)

    for key in continuous_list:
        resp = es.search(index = INDEX, body=query.filterContinuous(key))
        # print(resp.body["aggregations"][key]["buckets"])
        continuous[key] = {}
        continuous[key]["min"]  = resp.body["aggregations"]['min' + '_' + key]['value']
        continuous[key]["max"]  = resp.body["aggregations"]['max' + '_' + key]['value']
        
    # print (continuous)

    data['continuous'] = continuous
    data['categorical'] = categorical
    print(data)
    return "success"




if __name__ == "__main__":
    app.run(debug=True)
