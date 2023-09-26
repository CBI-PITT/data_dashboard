import datasets.filter_template as filter_template
class datasets_collection:
    def __init__(self):
        klimstra_index_4 = "klimstra4.0"
        klimstra_filter_4 = filter_template.filter_template()
        klimstra_filter_4.field = {
            "atlas_structure_number": "long",
            "metadata": "short",
            "route": "keyword",
            "time_point": "keyword",
            "treatment": "keyword",
            "uuid_cell": "keyword",
            "z_raw_px":"long"
        }
        klimstra_filter_4.filter = {
            "continuous": ['x_raw_px','y_raw_px', 'z_raw_px'],
            "categorical": [
                # "atlas_structure_number",
                "metadata",
                "route",
                "time_point",
                "treatment",
            ],
        }
        klimstra_filter_4.group_by = [
            "atlas_structure_number",
            "metadata",
            "route",
            "time_point",
            "treatment",
        ]
        klimstra_filter_4.aggregate = [
            "min",
            "max",
            "avg",
            "sum",
            "value_count",
            "cardinality",
        ]

        klimstra_index_3 = "klimstra3.0"
        klimstra_filter_3 = filter_template.filter_template()
        klimstra_filter_3.field = {
            "atlas_structure_number": "long",
            "metadata": "short",
            "route": "keyword",
            "time_point": "keyword",
            "treatment": "keyword",
            "uuid_cell": "keyword",
        }
        klimstra_filter_3.filter = {
            "continuous": ['z_raw','y_raw'],
            "categorical": [
                # "atlas_structure_number",
                # "metadata",
                "route",
                "time_point",
                "treatment",
            ],
        }
        klimstra_filter_3.group_by = [
            "atlas_structure_number",
            "metadata",
            "route",
            "time_point",
            "treatment",
        ]
        klimstra_filter_3.aggregate = [
            "min",
            "max",
            "avg",
            "sum",
            "value_count",
            "cardinality",
        ]

        metadata_index = "metadata_cell_count"
        metadata_filter = filter_template.filter_template()
        metadata_filter.field = {
            
            "id": "long",
            "cell_count":"short"
        }
        metadata_filter.filter = {
            "continuous": ['id'],
            "categorical": [
                # "atlas_structure_number",
                # "metadata",
                # "voxel_spacing",
                "time_point",
                "treatment",
            ],
        }
        metadata_filter.group_by = [
            # "voxel_spacing",
            "route",
            
            "time_point",
            "treatment",
        ]
        metadata_filter.aggregate = [
            "min",
            "max",
            "avg",
            "sum",
            "value_count",
            "cardinality",
        ]



        self.indexMap = {klimstra_index_4: klimstra_filter_4,
                         klimstra_index_3:klimstra_filter_3,
                         metadata_index:metadata_filter}
