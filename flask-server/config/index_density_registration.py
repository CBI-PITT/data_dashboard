from .density_meta import DensityMeta
# import .density_meta  as d

class Registration:
    def __init__(self) -> None:
        klimstra_6 = DensityMeta(
            "klimstra6.0", "25um", "atlas_structure_acronym", "value_count"
        )
        cebra_2 = DensityMeta(
            "cebra2.0", "10um", "atlas_structure_acronym", "value_count"
        )
        bill_1 = DensityMeta(
            "bill1.0", "10um", "atlas_structure_acronym", "value_count"
        )
        self.index_density_registration_map = {
            klimstra_6.index: klimstra_6,
            cebra_2.index: cebra_2,
            bill_1.index:bill_1
        }
