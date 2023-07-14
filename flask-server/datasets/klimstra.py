class klimstra:
    def __init__(self):
        self.index = "klimstra4.0"
        self.field = {
            "atlas_structure_number": "long",
            "metadata": "short",
            "route": "keyword",
            "time_point": "keyword",
            "treatment": "keyword",
            "uuid_cell": "keyword",
            'z_raw_px':'short'
        }
        self.filter = {
            "continuous": ['x_raw_px','y_raw_px'],
            "categorical": [
                # "atlas_structure_number",
                # "metadata",
                "route",
                "time_point",
                "treatment",
            ],
        }
        self.group_by = [
            "atlas_structure_number",
            "metadata",
            "route",
            "time_point",
            "treatment",
        ]
        self.aggregate = ["min", "max", "avg", "sum", "value_count", "cardinality"]

