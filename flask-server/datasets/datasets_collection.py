import datasets.filter_template as filter_template
class datasets_collection:
    def __init__(self):
        klimstra_index = "klimstra4.0"
        klimstra_filter = filter_template.filter_template()
        klimstra_filter.field = {
            "atlas_structure_number": "long",
            "metadata": "short",
            "route": "keyword",
            "time_point": "keyword",
            "treatment": "keyword",
            "uuid_cell": "keyword",
        }
        klimstra_filter.filter = {
            "continuous": [],
            "categorical": [
                # "atlas_structure_number",
                # "metadata",
                "route",
                "time_point",
                "treatment",
            ],
        }
        klimstra_filter.group_by = [
            "atlas_structure_number",
            "metadata",
            "route",
            "time_point",
            "treatment",
        ]
        klimstra_filter.aggregate = [
            "min",
            "max",
            "avg",
            "sum",
            "value_count",
            "cardinality",
        ]

        self.indexMap = {klimstra_index: klimstra_filter}
