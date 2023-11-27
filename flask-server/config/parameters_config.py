class parameters_config:
    def __init__(
        self,
        index,
        atlas_resolution,
        atlas_structure_acronym_column_name,
        aggregation_condition,
        metadata_calculation_name,
    ) -> None:
        self.index = index
        self.atlas_resolution = atlas_resolution
        self.atlas_structure_acronym_column_name = atlas_structure_acronym_column_name
        self.aggregation_condition = aggregation_condition
        self.metadata_calculation_name = metadata_calculation_name
