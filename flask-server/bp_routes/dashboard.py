from dataclasses import field

from flask import Blueprint
from flask import jsonify
from elasticsearch import Elasticsearch
from sqlalchemy import true
from config.es_config import es_server
from db_models.models import parameters
from flask import request
import query_dsl.query_dsl as Query
import time
import numpy as np
import pandas as pd
import re

dahsboard_bp = Blueprint("dashboard", __name__)

es = Elasticsearch(es_server, request_timeout=180)

INDEX = ""
DENSITY = False


def filter_indices(indices_list, substring):
    return [index for index in indices_list if substring not in index]


@dahsboard_bp.route("/api/indices")
def get_index():
    indices = es.cat.indices(format="json")
    # print(indices)
    index_names = [entry["index"] for entry in indices]
    # filtered_indices = filter_indices(index_names, "klimstra6.0")
    # print(index_names)
    return jsonify(index_names)


@dahsboard_bp.route("/api/index_choosen/<index_name>")
def choosen_index(index_name):
    global INDEX
    INDEX = index_name
    # global serialized_parameters
    # serialized_parameters = {}
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


acronym_volume_dict = {
    "acronym_volume_10": volume_reader(10),
    "acronym_volume_25": volume_reader(25),
}
# acronym_volume_10 = volume_reader(10)
# acronym_volume_25 = volume_reader(25)


@dahsboard_bp.route("/api/index_choosen/meta/<index_name>")
def meta(index_name):

    parameters_info = parameters.query.filter_by(es_index=index_name).all()

    serialized_parameters = {}
    if parameters_info:
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
            serialized_parameters["acronym_volumn"] = "acronym_volume_25"
            return serialized_parameters
        elif parameters_info[0].resolution_micrometer == 10:
            serialized_parameters["acronym_volumn"] = "acronym_volume_10"
            return serialized_parameters
        else:
            return serialized_parameters
    else:
        serialized_parameters = {
            "meta": {
                "aggregation_condition": None,
                "atlas_structure_acronym_column_name": None,
                "metadata_calculation_name": None,
            },
            "acronym_volumn": None,
        }
        return jsonify(serialized_parameters)


@dahsboard_bp.route("/api/index_choosen/current_status/<index_name>")
def choosen_index_current_status(index_name):

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
    return item.get("key_as_string", item.get("key"))


@dahsboard_bp.route("/api/query", methods=["POST"])
def query_data_source():
    json_data = request.json
    print(json_data)
    print(type(json_data["serialized_parameters"]))
    response = es_query_search(
        json_data["INDEX"],
        json_data["field"],
        json_data["filter"],
        json_data["group_by"],
        json_data["aggregate"],
    )
    agg_list = json_data["aggregate"]
    density_result = density(json_data, response, agg_list)
    response_density_check = density_result["response"]
    agg_list_density_check = density_result["agg_list"]
    agg_final = boxplot_filterOut(agg_list_density_check)
    response_final = {"agg_list": agg_final, "data": response_density_check}
    return jsonify(response_final)


@dahsboard_bp.route("/api/query_paras", methods=["POST"])
def query_paras():
    print(INDEX)
    json_data = request.json

    response = es_query_search(
        json_data["INDEX"],
        json_data["field"],
        json_data["filter"],
        json_data["group_by"],
        json_data["aggregate"],
        json_data["serialized_parameters"]["meta"]["metadata_calculation_name"],
    )

    agg_list = list(json_data["aggregate"])

    density_result = density(json_data, response, agg_list)
    response_density_check = density_result["response"]
    agg_list_density_check = density_result["agg_list"]
    total_n = None
    agg_list_boxplot_filterOut = boxplot_filterOut(agg_list_density_check)
    agg_list_boxplot_filterOut_copy = list(agg_list_boxplot_filterOut)

    if (
        json_data["serialized_parameters"]["meta"]["metadata_calculation_name"]
        in json_data["group_by"]
    ):
        for item in response_density_check:
            for agg in agg_list:
                item["avg" + "_" + agg + "_" + json_data["field"]] = {
                    "value": item[agg + "_" + json_data["field"]]["value"]
                    / item["N"]["value"],
                    "std": 0,
                }
        total_n = totalN(response_density_check, json_data["serialized_parameters"])
        response_final = {
            "agg_list": agg_list_boxplot_filterOut,
            "data": response_density_check,
            "total_n": total_n,
        }
        return jsonify(response_final)
    else:
        groupby_original = list(json_data["group_by"])
        group_by_added = list(json_data["group_by"])
        group_by_added.append(
            json_data["serialized_parameters"]["meta"]["metadata_calculation_name"]
        )
        response_groupby_added = es_query_search(
            json_data["INDEX"],
            json_data["field"],
            json_data["filter"],
            group_by_added,
            json_data["aggregate"],
        )

        density_result = density(json_data, response_groupby_added)
        response_groupby_added_density_check = density_result["response"]
        result_std = totalN_and_std(
            response_groupby_added_density_check,
            response_density_check,
            agg_list_boxplot_filterOut_copy,
            groupby_original,
            json_data["field"],
            json_data["serialized_parameters"],
        )
        response_std = result_std["response"]
        total_n = result_std["total_n"]
        for agg in agg_list_boxplot_filterOut_copy:
            agg_list_boxplot_filterOut.append("avg" + "_" + agg)
        response_final = {
            "agg_list": agg_list_boxplot_filterOut,
            "data": response_std,
            "total_n": total_n,
        }
        return jsonify(response_final)


def density(json_data, response, agg_list=None):
    if (
        json_data["field"]
        == json_data["serialized_parameters"]["meta"][
            "atlas_structure_acronym_column_name"
        ]
        and json_data["serialized_parameters"]["meta"][
            "atlas_structure_acronym_column_name"
        ]
        in json_data["group_by"]
        and json_data["serialized_parameters"]["meta"]["aggregation_condition"]
        in json_data["aggregate"]
        and json_data["serialized_parameters"]["acronym_volumn"]
    ):

        field = json_data["serialized_parameters"]["meta"][
            "atlas_structure_acronym_column_name"
        ]
        agg = json_data["serialized_parameters"]["meta"]["aggregation_condition"]
        resolution = acronym_volume_dict[
            json_data["serialized_parameters"]["acronym_volumn"]
        ]

        for item in response:

            acronym = item["key"][
                json_data["serialized_parameters"]["meta"][
                    "atlas_structure_acronym_column_name"
                ]
            ]
            item["density" + "_" + field] = {"value": ""}
            if resolution.get(acronym):

                item["density" + "_" + field]["value"] = (
                    item[agg + "_" + field]["value"] / resolution[acronym]
                )
            else:
                item["density" + "_" + field]["value"] = 0
        if agg_list:
            agg_list.append("density")
    else:

        print("density calculation not satisfied")
    return {"response": response, "agg_list": agg_list}


def totalN(buckets, serialized_parameters):
    totalN_set = set()
    for bucket in buckets:
        totalN_set.add(
            bucket["key"][serialized_parameters["meta"]["metadata_calculation_name"]]
        )
    return len(totalN_set)


def totalN_and_std(
    buckets_add, buckets, agg_original, groupby_original, field, serialized_parameters
):
    dict_std = {}
    for bucket in buckets_add:
        string_groupby = "|".join(
            str(bucket["key"].get(gb, "")) for gb in groupby_original
        )
        if string_groupby not in dict_std:
            dict_std[string_groupby] = {agg + "_" + field: [] for agg in agg_original}
        for agg in agg_original:
            dict_std[string_groupby][agg + "_" + field].append(
                bucket[agg + "_" + field]["value"]
            )

    totalN_set = {
        bucket["key"][serialized_parameters["meta"]["metadata_calculation_name"]]
        for bucket in buckets_add
    }
    total_n = len(totalN_set)

    for bucket in buckets:
        string_groupby = "|".join(
            str(bucket["key"].get(gb, "")) for gb in groupby_original
        )
        for agg in agg_original:
            std_values = dict_std.get(string_groupby, {}).get(agg + "_" + field)
            bucket["avg_" + agg + "_" + field] = {
                "value": bucket[agg + "_" + field]["value"] / bucket["N"]["value"],
                # standerd deviation
                # "std": np.std(std_values) if std_values else None
                # standerd error
                "std": (
                    np.std(std_values) / np.sqrt(len(std_values))
                    if std_values
                    else None
                ),
            }

    return {"response": buckets, "total_n": total_n}


def es_query_search(
    INDEX, field, filter, groupBy, aggregation, metadata_calculation_name=None
):
    print("before: " + time.asctime(time.localtime(time.time())))
    resp = es.search(
        index=INDEX,
        body=query.formCompositeQuery(
            field=field,
            filters=filter,
            groupBy=groupBy,
            aggregation=aggregation,
            cadinality_field=metadata_calculation_name,
        ),
    )
    print("after: " + time.asctime(time.localtime(time.time())))
    return resp.body["aggregations"]["categories"]["buckets"]


def boxplot_filterOut(agg_list):
    filtered_list = [s for s in agg_list if not re.match(r"^boxplot", s, re.IGNORECASE)]
    return filtered_list
