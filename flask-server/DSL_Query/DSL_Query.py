class Query:
    def filterContinuous(self, continuous_name):
        continuousName = continuous_name
        filterRetreive_query_body = {
            "size": 0,
            "aggs": {
                "max" + "_" + continuousName: {"max": {"field": continuousName}},
                "min" + "_" + continuousName: {"min": {"field": continuousName}}
            }
        }
        return filterRetreive_query_body

    def filterCategorical(self, category_name):
        categoryName = category_name
        sizeValue = 10000
        filterRetreive_query_body = {
            "size": 0,
            "aggs": {categoryName: {"terms": {"field": categoryName, "size": sizeValue}}},
        }
        return filterRetreive_query_body

    def formQuery():
        return ""
