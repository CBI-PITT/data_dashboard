
from elasticsearch import Elasticsearch, helpers
import uuid
import pandas as pd
import os
import requests
from config.es_config import es_server
from config.host import HOST, UPLOAD_FOLDER_PATH

server = es_server
es = Elasticsearch(request_timeout=600, hosts=server)


def creat_index(index_name, shard_number, mapping):
    INDEX = index_name
    mappings = mapping
    SHARDS = shard_number
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


# check here data read


def csv_to_pandas(csv_file, separator, delimiter):
    separator_mark = {
        "comma": ",",
        "tab": "\t",
        "semicolon": ";",
        "space": " ",
    }.get(separator, ",")

    delimiter_mark = {
        "double_quote": '"',
        "single_quote": "'",
    }.get(delimiter, '"')
    data = pd.read_csv(csv_file, sep=separator_mark, quotechar=delimiter_mark)
    data.fillna("null", inplace=True)
    return data


def csv_to_records(csv_file, separator, delimiter):
    data = csv_to_pandas(csv_file, separator, delimiter)

    records = data.to_dict("records")

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


def indexing_new(file_name, separator, delimiter, index_name, shard_number, mapping):
    creat_index(index_name, shard_number, mapping)
    records = csv_to_records(UPLOAD_FOLDER_PATH + "/" + file_name, separator, delimiter)
    print(records)
    print("Indexing")
    response = helpers.bulk(es, bulk_records_data(records, index_name))
    print("\nbulk_json_data() RESPONSE:", response)
    os.remove(UPLOAD_FOLDER_PATH + "/" + file_name)
    url = HOST + '/indexing/mapping_store'

    # Example payload for the POST request (can be a dictionary or any other data)
    payload = {'index': index_name, 'mapping': mapping["properties"]}
    
    # Send POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response # Convert response to JSON format
        print(data)
    else:
        print('POST request failed')

def indexing_existed(file_name, separator, delimiter, index_name):
    records = csv_to_records(UPLOAD_FOLDER_PATH + "/" + file_name, separator, delimiter)
    print(records)
    print("Indexing")
    response = helpers.bulk(es, bulk_records_data(records, index_name))
    print("\nbulk_json_data() RESPONSE:", response)
    os.remove(UPLOAD_FOLDER_PATH + "/" + file_name)
