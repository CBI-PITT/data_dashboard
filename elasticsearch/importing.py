from elasticsearch import Elasticsearch, helpers
import csv
import uuid
import glob
import os
import json
import pandas as pd

file = "/home/kelin/Desktop/merged_cell_metadata.csv"
file_metadata = "/home/kelin/Documents/GitHub/data_dashboard/flask-server/metadata.csv"

server = 'http://localhost:9200'
es = Elasticsearch(request_timeout=600, hosts=server)

INDEX = 'klimstra4.0'
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

records = csv_to_records(file)
print(records)
print('Indexing')
response = helpers.bulk(es, bulk_records_data(records, INDEX))
print("\nbulk_json_data() RESPONSE:", response)
