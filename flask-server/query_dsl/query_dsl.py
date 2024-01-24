import json
from config.es_config import es_server
from elasticsearch_dsl import Search, Q, connections
connections.create_connection(hosts=[es_server])

def create_aggs(fields):
    if not fields:
        return {}

    field = fields.pop(0)
    aggs = {field: {"terms": {"field": field}, "aggs": create_aggs(fields.copy())}}

    return aggs


class Query:
    def filterContinuous(self, continuous_name):
        continuousName = continuous_name
        sizeValue = 10000
        filterRetrieve_query_body = {
            "size": 0,
            "aggs": {
                "max" + "_" + continuousName: {"max": {"field": continuousName}},
                "min" + "_" + continuousName: {"min": {"field": continuousName}},
            },
        }
        return filterRetrieve_query_body

    def filterCategorical(self, category_name):
        categoryName = category_name
        sizeValue = 10000
        filterRetrieve_query_body = {
            "size": 0,
            "aggs": {
                categoryName: {"terms": {"field": categoryName, "size": sizeValue}}
            },
        }
        return filterRetrieve_query_body

    def formQuery(self, field: str, filters: dict, groupBy: list, aggregation: list):
        form_query_body = {
            "size": 0,
            "query": {"bool": {"filter": {"bool": {"must": []}}}},
        }
        sizeValue = 10000
        categorical = filters["categorical"]
        continuous = filters["continuous"]
        for item in categorical:
            should = []
            # form_query_body['query']['bool']['filter']['bool']['must'].append({'bool' : {'should' : []}})
            for val in categorical[item]:
                should.append({"term": {item: val}})
            bool = {"bool": {"should": should}}
            form_query_body["query"]["bool"]["filter"]["bool"]["must"].append(bool)
        # print(form_query_body)
        for item in continuous:
            # print(continuous[item],continuous[item][0],continuous[item][1])
            range = {
                "range": {
                    item: {"gte": continuous[item][0], "lte": continuous[item][1]}
                }
            }
            form_query_body["query"]["bool"]["filter"]["bool"]["must"].append(range)

        form_query_body["aggs"] = {"categories": {"aggs": {}}}
        if len(groupBy) == 1:
            form_query_body["aggs"]["categories"]["terms"] = {
                "field": groupBy[0],
                "size": sizeValue,
            }
        else:
            form_query_body["aggs"]["categories"]["multi_terms"] = {
                "terms": [],
                "size": sizeValue,
            }
            for item in groupBy:
                form_query_body["aggs"]["categories"]["multi_terms"]["terms"].append(
                    {"field": item}
                )

        aggs = {}
        for item in aggregation:
            aggs[item + "_" + field] = {item: {"field": field}}
        form_query_body["aggs"]["categories"]["aggs"] = aggs

        # print(json.dumps(form_query_body,indent=2))

        return form_query_body

    
