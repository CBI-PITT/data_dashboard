from elasticsearch import Elasticsearch, helpers
import csv
import uuid
import glob
import os
import json
import pandas as pd

# file = '/CBI_FastStore/Iana/BIL/merged_cell_metadata.csv'  # initial 03CL13 (with Imaris)

server = 'http://localhost:9200'
es = Elasticsearch(request_timeout=600, hosts=server)

INDEX = 'klimstra5.0'
SHARDS = 12
# REPLICAS = 2
# Create Index
mappings = {
    "properties": {
      "atlas_name": {
        "type": "keyword"
      },
      "atlas_resolution": {
        "type": "short"
      },
      "atlas_structure_number": {
        "type": "long"
      },
      "channel": {
        "type": "short"
      },
      "file_path": {
        "type": "keyword"
      },
      "id": {
        "type": "short"
      },
      "is_cell": {
        "type": "short"
      },
      "metadata": {
        "type": "short"
      },
      "n_channels": {
        "type": "short"
      },
      "raw_coord_units": {
        "type": "keyword"
      },
      "route": {
        "type": "keyword"
      },
      "time_point": {
        "type": "keyword"
      },
      "transformed_coord_units": {
        "type": "keyword"
      },
      "treatment": {
        "type": "keyword"
      },
      "uuid_brain": {
        "type": "keyword"
      },
      "uuid_cell": {
        "type": "keyword",
      },
      "voxel_spacing": {
        "type": "keyword"
      },
      "voxel_spacing_units": {
        "type": "keyword",
      },
      "x_downsampled": {
        "type": "short"
      },
      "x_raw": {
        "type": "float"
      },
      "x_raw_px": {
        "type": "integer"
      },
      "x_transformed": {
        "type": "short"
      },
      "x_transformed_px": {
        "type": "short"
      },
      "y_downsampled": {
        "type": "short"
      },
      "y_raw": {
        "type": "float"
      },
      "y_raw_px": {
        "type": "integer"
      },
      "y_transformed": {
        "type": "short"
      },
      "y_transformed_px": {
        "type": "short"
      },
      "z_downsampled": {
        "type": "short"
      },
      "z_raw": {
        "type": "float"
      },
      "z_raw_px": {
        "type": "short"
      },
      "z_transformed": {
        "type": "short"
      },
      "z_transformed_px": {
        "type": "short"
      }
    }
  }


if not es.indices.exists(index=INDEX):
    es.indices.create(index=INDEX, body={
        'settings': {
            'index': {
                'number_of_shards': SHARDS,
                # 'number_of_replicas': REPLICAS
            }
        },
        "mappings": mappings
    })

def csv_to_pandas(csv_file):
    
    data = pd.read_csv(csv_file, sep='\t')
    data.replace('\\N','null',inplace=True)
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

    records = data.to_dict('records')
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
                #"_type": 'keyword',
                "_id": uuid.uuid1(),
                "_source": doc
            }
    # for doc in records:
    #     print(doc)


def join_with_metadata(cells, metadata, metadata_shift=0):
    df_cells = pd.read_csv(cells, usecols=['uuid', 'channel', 'is_cell', 'atlas_name', 'atlas_resolution', 'z_downsampled', 'y_downsampled', 'x_downsampled', 'z_transformed', 'y_transformed', 'x_transformed', 'transformed_coord_units', 'z_transformed_px', 'y_transformed_px', 'x_transformed_px', 'atlas_structure_number', 'metadata'])
    df_cells = df_cells.rename(columns={'uuid': 'uuid_cell'})
    df_metadata = pd.read_csv(metadata, usecols=['id', 'uuid', 'file_path', 'n_channels', 'voxel_spacing', 'voxel_spacing_units', 'treatment', 'time_point', 'route'])
    df_metadata = df_metadata.rename(columns={'uuid': 'uuid_brain'})
    df_merged = pd.merge(left=df_metadata,
             right=df_cells,
             how='inner',
             left_on='id',
             right_on='metadata').drop(['id'], axis=1)
    joint_file = cells.replace('.csv', '_with_metadata.csv')
    df_merged['metadata'] += metadata_shift
    df_merged.to_csv(joint_file, sep="\t")
    return joint_file


# 03CL13
metadata = '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/metadata.csv'
files = [
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01081_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01083_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01084_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01087_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01107_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01132_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01133_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL13/data_for_dashboard/job_01198_binary_df.csv'
]


for file in files:
    joint_file = join_with_metadata(file, metadata)
    records = csv_to_records(joint_file)
    print(records)
    print('Indexing')
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)


# 03CL02
metadata = '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/metadata.csv'
files = [
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00914_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00917_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00922_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00931_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00960_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00963_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00968_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00970_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00973_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00978_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00983_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00991_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_00999_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01016_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01017_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01018_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01068_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01077_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01102_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01105_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01124_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/03CL02/data_for_dashboard/job_01128_binary_df.csv'
]

for file in files:
    print("Working on", file)
    joint_file = join_with_metadata(file, metadata, metadata_shift=29)
    records = csv_to_records(joint_file)
    print(records)
    print('Indexing')
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)


# 01CL73
metadata = '/CBI_Hive/CBI/Iana/projects/klimstra/01CL73/data_for_dashboard/metadata.csv'
files = [
    '/CBI_Hive/CBI/Iana/projects/klimstra/01CL73/data_for_dashboard/00076_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/01CL73/data_for_dashboard/00077_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/01CL73/data_for_dashboard/00078_binary_df.csv',
    '/CBI_Hive/CBI/Iana/projects/klimstra/01CL73/data_for_dashboard/00142_binary_df.csv'
]

for file in files:
    print("Working on", file)
    joint_file = join_with_metadata(file, metadata, metadata_shift=58)
    records = csv_to_records(joint_file)
    print(records)
    print('Indexing')
    response = helpers.bulk(es, bulk_records_data(records, INDEX))
    print("\nbulk_json_data() RESPONSE:", response)
