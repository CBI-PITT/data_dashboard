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


es = Elasticsearch("http://localhost:9200", timeout=180)


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resource={
#     r"/*":{
#         "origins":"*"
#     }
# })

# collection = datasets_collection.datasets_collection()


INDEX = ""


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/details")
def get_details():
    indices = es.cat.indices(format="json")
    print(indices)

    # print(index_names)

    return []


# to be constructed
@app.route("/api/indices")
def get_index():
    indices = es.cat.indices(format="json")
    # print(indices)
    index_names = [entry["index"] for entry in indices]
    # print(index_names)

    return jsonify(index_names)


@app.route("/api/index_choosen/<index_name>")
def choosen_index(index_name):
    global INDEX
    INDEX = index_name
    time.sleep(1)
    # fileds = list(
    #     es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys()
    # )
    mappings = es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"]
    for key, value in mappings.items():
        mappings[key] = value["type"]
    categorical = {}
    continuous = {}
    for key, value in mappings.items():
        if mappings[key] == "keyword":
            categorical[key] = []
        else:
            continuous[key] = []

    for key in categorical:
        # print(key)
        resp = es.search(index=INDEX, body=query.filterCategorical(key))
        # print(resp.body["aggregations"][key]["buckets"])
        temp_dict = resp.body["aggregations"][key]["buckets"]
        # print("--------------",temp_dict)
        # print (temp_dict)

        for val in temp_dict:
            categorical[key].append(val["key"])
    # print (categorical)

    for key in continuous:
        resp = es.search(index=INDEX, body=query.filterContinuous(key))
        # print(resp.body["aggregations"][key]["buckets"])

        continuous[key].append(resp.body["aggregations"]["min" + "_" + key]["value"])
        continuous[key].append(resp.body["aggregations"]["max" + "_" + key]["value"])

    filters = {"categorical": categorical, "continuous": continuous}

    formFrame = {
        "filter_list": list(mappings.keys()),
        "field": mappings,
        "filter": filters,
        "group_by": list(mappings.keys()),
        "aggregate": ["min", "max", "avg", "value_count", "cardinality"],
        # "acronym_volume": acronym_volume,
    }

    return formFrame


def volume_reader(um):
    csv_file_path = "../atlasapi_output/atlas_mouse_acronym&volume.csv"
    df = pd.read_csv(csv_file_path)
    acronym_volume_dict = df.set_index("acronym")[f"volume_mm_{um}"].to_dict()
    return acronym_volume_dict


acronym_volume_10 = volume_reader(10)
acronym_volume_25 = volume_reader(25)


@app.route("/api/index_choosen/volume/<index_name>")
def acronym_volume(index_name):
    if index_name == "klimstra6.0":
        response = acronym_volume_25
        # print(acronym_volume_25)
        return jsonify(response)
    elif index_name == "cebra2.0":
        return jsonify(acronym_volume_10)


@app.route("/api/index_choosen/current_status/<index_name>")
def choosen_index_current_status(index_name):
    time.sleep(1)
    indices = es.cat.indices(format="json")
    current_status = {}
    # print(indices)
    for index_data in indices:
        if index_data["index"] == index_name:
            current_status["health"] = index_data["health"]
            current_status["status"] = index_data["status"]
            current_status["storage_size"] = index_data["store.size"]
            current_status["docs_count"] = index_data["docs.count"]
            break
    return jsonify(current_status)


# @app.route("/api/datasets")
# def get_dataset():
#     return list(collection.indexMap.keys())


# @app.route("/api/dataset_choosen/<dataset_name>")
# def choose_dataset(dataset_name):
#     global INDEX
#     INDEX = dataset_name

#     time.sleep(1)
#     formFrame = collection.indexMap.get(dataset_name).__dict__

#     categorical = {}
#     continuous = {}

#     # fileds = list(
#     #     es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys()
#     # )
#     # print(fileds)

#     continuous_list = formFrame["filter"]["continuous"]
#     categorical_list = formFrame["filter"]["categorical"]
#     # print('----------------',categorical_list)

#     for key in categorical_list:
#         print(key)
#         resp = es.search(index=INDEX, body=query.filterCategorical(key))
#         # print(resp.body["aggregations"][key]["buckets"])
#         temp_dict = resp.body["aggregations"][key]["buckets"]
#         # print("--------------",temp_dict)
#         # print (temp_dict[0])
#         categorical[key] = []
#         for val in temp_dict:
#             categorical[key].append(val["key"])
#     # print (categorical)

#     for key in continuous_list:
#         resp = es.search(index=INDEX, body=query.filterContinuous(key))
#         # print(resp.body["aggregations"][key]["buckets"])
#         continuous[key] = []
#         continuous[key].append(resp.body["aggregations"]["min" + "_" + key]["value"])
#         continuous[key].append(resp.body["aggregations"]["max" + "_" + key]["value"])

#     # print (continuous)

#     formFrame["filter"]["continuous"] = continuous
#     formFrame["filter"]["categorical"] = categorical
#     response = jsonify(formFrame)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return formFrame


# @app.route("/api/field")
# def get_field():
#     # fields = es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"]
#     # fields_dict = {}
#     # for field in fields:
#     #     fields_dict[field] = fields[field].get('type')
#     # response = jsonify(fields_dict)
#     # response.headers.add("Access-Control-Allow-Origin", "*")
#     # return response

#     field = dataset.field
#     response = jsonify(field)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


# @app.route("/api/filter")
# def get_filters2():
#     data = {}
#     categorical = {}
#     continuous = {}

#     # fileds = list(
#     #     es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys()
#     # )
#     # print(fileds)

#     # manually setting cate and conti list
#     # categorical_list = ["route", "time_point", "treatment"]
#     continuous_list = dataset.filter['continuous']
#     categorical_list = dataset.filter['categorical']


#     for key in categorical_list:
#         resp = es.search(index=INDEX, body=query.filterCategorical(key))
#         # print(resp.body["aggregations"][key]["buckets"])
#         temp_dict = resp.body["aggregations"][key]["buckets"]
#         # print("--------------",temp_dict)
#         # print (temp_dict[0])
#         categorical[key] = []
#         for val in temp_dict:
#             categorical[key].append(val["key"])
#     # print (categorical)

#     for key in continuous_list:
#         resp = es.search(index=INDEX, body=query.filterContinuous(key))
#         # print(resp.body["aggregations"][key]["buckets"])
#         continuous[key] = {}
#         continuous[key]["min"] = resp.body["aggregations"]["min" + "_" + key]["value"]
#         continuous[key]["max"] = resp.body["aggregations"]["max" + "_" + key]["value"]

#     # print (continuous)

#     data["continuous"] = continuous
#     data["categorical"] = categorical
#     # print("data",data)
#     response = jsonify(data)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

# @app.route("/api/groupBy")
# def get_groupBy():
#     # gourp_by_list = list(es.indices.get_mapping(index=INDEX)[INDEX]["mappings"]["properties"].keys())
#     gourp_by_list = dataset.group_by
#     response = jsonify(gourp_by_list)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


# @app.route("/api/aggregation")
# def get_aggregate():
#     """
#     response format:
#     {"data": ["count of distinct", "count of all", "total sum", "average", "min", "max"]}
#     """
#     # data = {
#     #     "data": [
#     #         "avg",
#     #         "min",
#     #         "max",
#     #         "sum",
#     #         "value_count",
#     #         "cardinality"
#     #         # "boxplot",
#     #         # "percentiles"
#     #     ]
#     # }
#     data = {"data": dataset.aggregate}
#     response = jsonify(data)
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response


query = Query.Query()


def custom_sort(item):
    # print(item.get('key_as_string'))
    # print(type(item.get('key_as_string')))
    return item.get("key_as_string", item.get("key"))


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
    print("before: " + time.asctime(time.localtime(time.time())))

    # resp = query.formQuery(
    #      json_data["field"],
    #         json_data["filter"],
    #         json_data["group_by"],
    #         json_data["aggregate"],
    # )
    # return resp

    resp = es.search(
        index=INDEX,
        body=query.formQuery(
            json_data["field"],
            json_data["filter"],
            json_data["group_by"],
            json_data["aggregate"],
        ),
    )

    print("after: " + time.asctime(time.localtime(time.time())))
    response = resp.body["aggregations"]["categories"]["buckets"]

    response_sorted = sorted(response, key=custom_sort)
    return jsonify(response_sorted)
    # return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
