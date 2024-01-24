from flask import Blueprint
from flask import jsonify
from elasticsearch import Elasticsearch
from config.es_config import es_server

from db_models.models import parameters
from flask import request
import query_dsl.query_dsl as Query
import time

import pandas as pd

dahsboard_bp = Blueprint("dashboard", __name__)

es = Elasticsearch(es_server, request_timeout=180)

INDEX = ""


def filter_indices(indices_list, substring):
    return [index for index in indices_list if substring not in index]


@dahsboard_bp.route("/api/indices")
def get_index():
    indices = es.cat.indices(format="json")
    # print(indices)
    index_names = [entry["index"] for entry in indices]
    filtered_indices = filter_indices(index_names, "klimstra6.0")
    # print(index_names)
    return jsonify(index_names)


@dahsboard_bp.route("/api/index_choosen/<index_name>")
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
        "aggregate": ["min", "max", "avg", "sum", "value_count", "cardinality"],
    }

    return formFrame


def volume_reader(um):
    csv_file_path = "atlasapi_output/atlas_mouse_acronym&volume.csv"
    df = pd.read_csv(csv_file_path)
    acronym_volume_dict = df.set_index("acronym")[f"volume_mm_{um}"].to_dict()
    return acronym_volume_dict


acronym_volume_10 = volume_reader(10)
acronym_volume_25 = volume_reader(25)
# indexDensityRegistrationMap = (
#     index_registration.Registration().index_density_registration_map
# )


@dahsboard_bp.route("/api/index_choosen/meta/<index_name>")
def meta(index_name):
    # if indexDensityRegistrationMap.get(index_name):
    # obj = indexDensityRegistrationMap.get(index_name)
    # response = {
    #     "meta": {
    #         "aggregation_condition": obj.aggregation_condition,
    #         "atlas_structure_acronym_column_name": obj.atlas_structure_acronym_column_name,
    #         "metadata_calculation_name": obj.metadata_calculation_name,
    #     },
    #     "acronym_volumn": {},
    # }
    # if obj.atlas_resolution == "25um":
    #     response["acronym_volumn"] = acronym_volume_25
    #     return jsonify(response)
    # elif obj.atlas_resolution == "10um":
    #     response["acronym_volumn"] = acronym_volume_10
    #     return jsonify(response)
    # else:
    #     return jsonify(response)
    parameters_info = parameters.query.filter_by(es_index=index_name).all()
    serialized_parameters = {
        "meta": {
            "aggregation_condition": parameters_info[0].density_agg,
            "atlas_structure_acronym_column_name": parameters_info[
                0
            ].density_atlas_col_name,
            "metadata_calculation_name": parameters_info[0].n_value_col_name,
        },
        "acronym_volumn": {},
    }
    if parameters_info[0].resolution_micrometer == 25:
        serialized_parameters["acronym_volumn"] = acronym_volume_25
        return serialized_parameters
    elif parameters_info[0].resolution_micrometer == 10:
        serialized_parameters["acronym_volumn"] = acronym_volume_10
        return serialized_parameters
    else:
        return serialized_parameters


@dahsboard_bp.route("/api/index_choosen/current_status/<index_name>")
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


query = Query.Query()


def custom_sort(item):
    # print(item.get('key_as_string'))
    # print(type(item.get('key_as_string')))
    return item.get("key_as_string", item.get("key"))


# def query_without_field(groupBy):
#     s = Search(using=es, index=INDEX)


# # Create a Composite aggregation for combined group by
#     composite_aggregation = aggs.Composite(sources=[
#         {term: {'terms': {'field': term}}} for term in groupBy
#     ], size=10000)

#     # Add the Composite aggregation to the search
#     s.aggs.bucket('combined_group', composite_aggregation)

#     # Set the size to 0 to only get aggregation results
#     s = s.extra(size=0)

#     # Execute the search
#     result = s.execute()

#     # Access the combined aggregation results
#     combined_buckets = result.aggregations.combined_group.buckets
#     json_result = []
#     # Process the aggregation results and print doc_count for each combination
#     for combined_bucket in combined_buckets:
#         # key = combined_bucket.key
#         # doc_count = combined_bucket.doc_count
#         # print(f"Combined group: {key}, Doc Count: {doc_count}")

#         for combined_bucket in combined_buckets:
#             key_values = [combined_bucket['key'][term] for term in groupBy]
#             key_as_string = '|'.join(map(str, key_values))
#             value_count = combined_bucket.doc_count

#             json_result.append({
#                 'key': key_values,
#                 'key_as_string': key_as_string,
#                 'value_count': value_count
#             })
#             print(json_result)
#     return json_result


@dahsboard_bp.route("/api/query", methods=["POST"])
def query_data_source2():
    json_data = request.json

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

    # return response
    response_sorted = sorted(response, key=custom_sort)
    return jsonify(response_sorted)

    # return jsonify(response)
