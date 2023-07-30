import json

import pandas as pd
import DSL_Query.DSL_Query as Query
import time
import datasets.klimstra as klimstra
import datasets.datasets_collection as datasets_collection
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import NumpyEncoder, merge_cells_and_metadata
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")




app = Flask(__name__)
CORS(app)
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })

collection = datasets_collection.datasets_collection()

dataset = klimstra.klimstra()
INDEX = dataset.index

@app.route("/")
def index():
    return app.send_static_file("index.html")

# to be constructed 
# @app.route("/index")
# def index():
#   GET /_cat/indices or GET /_cat/indices?h=index


@app.route("/api/datasets")
def get_dataset():
    return list(collection.indexMap.keys())

# to be constructed 
# receive dataset users select
# to do in future
@app.route("/api/dataset_choosen/<dataset_name>")
def choose_dataset(dataset_name):
    formFrame = collection.indexMap.get(dataset_name).__dict__
    
    
    categorical = {}
    continuous = {}

    # fileds = list(
    #     es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys()
    # )
    # print(fileds)

    
    continuous_list = formFrame['filter']['continuous']
    categorical_list = formFrame['filter']['categorical']
    print('----------------',categorical_list)

    for key in categorical_list:
        resp = es.search(index=INDEX, body=query.filterCategorical(key))
        # print(resp.body["aggregations"][key]["buckets"])
        temp_dict = resp.body["aggregations"][key]["buckets"]
        # print("--------------",temp_dict)
        # print (temp_dict[0])
        categorical[key] = []
        for val in temp_dict:
            categorical[key].append(val["key"])
    # print (categorical)

    for key in continuous_list:
        resp = es.search(index=INDEX, body=query.filterContinuous(key))
        # print(resp.body["aggregations"][key]["buckets"])
        continuous[key] = {}
        continuous[key]["min"] = resp.body["aggregations"]["min" + "_" + key]["value"]
        continuous[key]["max"] = resp.body["aggregations"]["max" + "_" + key]["value"]

    # print (continuous)

    formFrame['filter']['continuous'] = continuous
    formFrame['filter']['categorical'] = categorical
    response = jsonify(formFrame)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return formFrame

@app.route("/api/field")
def get_field():
    # fields = es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"]
    # fields_dict = {}
    # for field in fields:
    #     fields_dict[field] = fields[field].get('type')
    # response = jsonify(fields_dict)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # return response

    field = dataset.field
    response = jsonify(field)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/filter")
def get_filters2():
    data = {}
    categorical = {}
    continuous = {}

    # fileds = list(
    #     es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys()
    # )
    # print(fileds)

    # manually setting cate and conti list
    # categorical_list = ["route", "time_point", "treatment"]
    continuous_list = dataset.filter['continuous']
    categorical_list = dataset.filter['categorical']
    

    for key in categorical_list:
        resp = es.search(index=INDEX, body=query.filterCategorical(key))
        # print(resp.body["aggregations"][key]["buckets"])
        temp_dict = resp.body["aggregations"][key]["buckets"]
        # print("--------------",temp_dict)
        # print (temp_dict[0])
        categorical[key] = []
        for val in temp_dict:
            categorical[key].append(val["key"])
    # print (categorical)

    for key in continuous_list:
        resp = es.search(index=INDEX, body=query.filterContinuous(key))
        # print(resp.body["aggregations"][key]["buckets"])
        continuous[key] = {}
        continuous[key]["min"] = resp.body["aggregations"]["min" + "_" + key]["value"]
        continuous[key]["max"] = resp.body["aggregations"]["max" + "_" + key]["value"]

    # print (continuous)

    data["continuous"] = continuous
    data["categorical"] = categorical
    # print("data",data)
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response 

@app.route("/api/groupBy")
def get_groupBy():
    # gourp_by_list = list(es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys())
    gourp_by_list = dataset.group_by
    response = jsonify(gourp_by_list)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

query = Query.Query()



@app.route("/api/aggregation")
def get_aggregate():
    """
    response format:
    {"data": ["count of distinct", "count of all", "total sum", "average", "min", "max"]}
    """
    # data = {
    #     "data": [
    #         "avg",
    #         "min",
    #         "max",
    #         "sum",
    #         "value_count",
    #         "cardinality"
    #         # "boxplot",
    #         # "percentiles"
    #     ]
    # }
    data = {"data":dataset.aggregate}
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/query", methods=["POST"])
def query_data_source2():
    
    json_data = request.json
    # data = query.formQuery(
    #     json_data["field"],
    #     json_data["filter"],
    #     json_data["group_by"],
    #     json_data["aggregate"],
    # )
    # print(jsonify(data))
    # response = jsonify(data)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # return response
    print ("before: "+ time.asctime(time.localtime(time.time())))
    
    
    resp = es.search(
        index=INDEX,
        body=query.formQuery(
            json_data["field"],
            json_data["filter"],
            json_data["group_by"],
            json_data["aggregate"],
        ),
    )
    # print(resp.body)
    print ("after: " + time.asctime(time.localtime(time.time())))
    response  = resp.body['aggregations']['categories']['buckets']
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
