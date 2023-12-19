from config.parameters_config import parameters_config

class Registration:
    def __init__(self) -> None:
        # (index, resolution, column name for calculating acronym density, aggregation condition triggered for density calculation, column name for calculating N value)
        klimstra_6 = parameters_config(
            "klimstra6.0", "25um", "atlas_structure_acronym", "value_count", "metadata"
        )
        cebra_2 = parameters_config(
            "cebra2.0", "10um", "atlas_structure_acronym", "value_count", "metadata"
        )
        bill_1 = parameters_config("bill1.0", None, None, None, None)

        check = parameters_config(
            "check", "25um", "atlas_structure_acronym", "value_count", "metadata"
        )
        self.index_density_registration_map = {
            klimstra_6.index: klimstra_6,
            cebra_2.index: cebra_2,
            bill_1.index: bill_1,
            check.index: check
        }
