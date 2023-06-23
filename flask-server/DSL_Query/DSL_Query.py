class Query:
    def filterContinuous(self, continuous_name):
        continuousName = continuous_name
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
            "aggs": {
                "categories": {
                    # terms or multiterms section
                    "aggs": {}
                }
            },
        }
        if len(groupBy) == 1:
            form_query_body["aggs"]["categories"]["terms"] = {"field": groupBy[0]}
        else:
            form_query_body["aggs"]["categories"]["multi_terms"] = {"terms": []}
            for item in groupBy:
                form_query_body["aggs"]["categories"]["multi_terms"]["terms"].append(
                    {"field": item}
                )

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

        aggs = {}
        for item in aggregation:
            aggs[item + "_" + field] = {item: {"field": field}}
        form_query_body["aggs"]["categories"]["aggs"] = aggs
        return form_query_body
        
