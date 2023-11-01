from elasticsearch import Elasticsearch, helpers
import csv
import uuid
import glob
import os
import json
import pandas as pd

server = "http://localhost:9200"
es = Elasticsearch(request_timeout=600, hosts=server)

INDEX = "cebra2.0"
SHARDS = 12
# REPLICAS = 2
# Create Index
mappings = {
    "properties": {
        "atlas_name": {"type": "keyword"},
        "atlas_resolution": {"type": "short"},
        "atlas_structure_number": {"type": "long"},
        "atlas_structure_acronym": {"type": "keyword"},
        # "channel": {
        #   "type": "short"
        # },
        "file_path": {"type": "keyword"},
        #   "id": {
        #     "type": "short"
        #   },
        # "is_cell": {
        #   "type": "short"
        # },
        "metadata": {"type": "keyword"},
        # "n_channels": {
        #   "type": "short"
        # },
        # "raw_coord_units": {
        #   "type": "keyword"
        # },
        # "route": {
        #   "type": "keyword"
        # },
        "time_point": {"type": "keyword"},
        # "transformed_coord_units": {
        #   "type": "keyword"
        # },
        "treatment": {"type": "keyword"},
        "sex": {"type": "keyword"},
        "uuid_brain": {"type": "keyword"},
        "uuid_cell": {
            "type": "keyword",
        },
        # "voxel_spacing": {
        #   "type": "keyword"
        # },
        # "voxel_spacing_units": {
        #   "type": "keyword",
        # },
        "x_downsampled": {"type": "short"},
        "x_raw": {"type": "float"},
        "x_raw_px": {"type": "integer"},
        "x_transformed": {"type": "short"},
        "x_transformed_px": {"type": "short"},
        "y_downsampled": {"type": "short"},
        "y_raw": {"type": "float"},
        "y_raw_px": {"type": "integer"},
        "y_transformed": {"type": "short"},
        "y_transformed_px": {"type": "short"},
        "z_downsampled": {"type": "short"},
        "z_raw": {"type": "float"},
        "z_raw_px": {"type": "short"},
        "z_transformed": {"type": "short"},
        "z_transformed_px": {"type": "short"},
    }
}


if not es.indices.exists(index=INDEX):
    es.indices.create(
        index=INDEX,
        body={
            "settings": {
                "index": {
                    "number_of_shards": SHARDS,
                    # 'number_of_replicas': REPLICAS
                }
            },
            "mappings": mappings,
        },
    )


def csv_to_pandas(csv_file):
    data = pd.read_csv(csv_file, sep="\t")
    # print(data['treatment'].head(n=100))
    # data.replace('\\N','null',inplace=True)
    data.fillna("null", inplace=True)

    # data['time_point'].replace('null',-1, inplace=True)
    # data = pd.read_csv(csv_file, sep='\t')
    # data.drop(data.columns[0], axis=1, inplace=True)
    # print(data.columns)
    # data = data.fillna("null")
    # print(data.dtypes)
    # print(data['treatment'].head(n=100))
    # print(data['time_point'].head(n=100))
    # print(data['route'].head(n=100))
    return data


def csv_to_records(csv_file):
    data = csv_to_pandas(csv_file)
    # data = data['time_point'].fillna(-1)
    # print(data.dtypes)
    # print(data['treatment'].head(n=100))
    # print(data['time_point'].head(n=100))
    # print(data['route'].head(n=100))

    records = data.to_dict("records")
    # print(records)
    for record in records:
        yield record


def bulk_records_data(records, _index):
    for doc in records:
        # use a `yield` generator so that the data
        # isn't loaded into memory
        # print(doc)
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                # "_type": 'keyword',
                "_id": uuid.uuid1(),
                "_source": doc,
            }
    # for doc in records:
    #     print(doc)


def join_with_metadata(cells, metadata, metadata_shift=0):
    df_cells = pd.read_csv(
        cells,
        usecols=[
            "uuid",
            "z_raw",
            "y_raw",
            "x_raw",
            "z_raw_px",
            "y_raw_px",
            "x_raw_px",
            "atlas_name",
            "atlas_resolution",
            "z_downsampled",
            "y_downsampled",
            "x_downsampled",
            "z_transformed",
            "y_transformed",
            "x_transformed",
            "z_transformed_px",
            "y_transformed_px",
            "x_transformed_px",
            # 'atlas_structure_number', 'atlas_structure_acronym', 'metadata'
            "atlas_structure_acronym",
            "atlas_structure_number",
            "metadata",
        ],
    )
    df_cells = df_cells.rename(columns={"uuid": "uuid_cell"})
    dtype_dict = {"time_point": float}
    df_metadata = pd.read_csv(
        metadata,
        usecols=["id", "uuid", "file_path", "treatment", "time_point", "sex"],
        dtype=dtype_dict,
    )
    df_metadata = df_metadata.rename(columns={"uuid": "uuid_brain"})
    df_merged = pd.merge(
        left=df_metadata, right=df_cells, how="inner", left_on="id", right_on="metadata"
    ).drop(["id"], axis=1)
    joint_file = cells.replace(".csv", "_with_metadata.csv")
    df_merged["metadata"] += metadata_shift
    df_merged.to_csv(joint_file, sep="\t", index=False)
    return joint_file


# 02CL89
metadata = (
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/metadata.csv"
)
files = [
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00836_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00834_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00833_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00835_df_for_dashboard.csv",
]

for file in files:
    joint_file = join_with_metadata(file, metadata)
    records = csv_to_records(joint_file)
    # print(records)
    print("Indexing")
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)


# 03CL12
metadata = (
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/metadata.csv"
)
files = [
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01179_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01181_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01202_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01103_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01174_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01178_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01109_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01151_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01115_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01175_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01159_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01161_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01116_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01111_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01182_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01106_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01093_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01117_df_for_dashboard.csv",
]

for file in files:
    print("Working on", file)
    joint_file = join_with_metadata(file, metadata, metadata_shift=9)
    records = csv_to_records(joint_file)
    print(records)
    print("Indexing")
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)


# 03CL47
metadata = (
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/metadata.csv"
)
files = [
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01251_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01250_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01255_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01249_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01253_df_for_dashboard.csv",
]

for file in files:
    print("Working on", file)
    joint_file = join_with_metadata(file, metadata, metadata_shift=37)
    records = csv_to_records(joint_file)
    print(records)
    print("Indexing")
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)
