import pandas as pd
def join_with_metadata(cells, metadata, metadata_shift=0):
    dtype_dict = {"time_point": float}
    df_cells = pd.read_csv(
        cells,
        usecols=[
            "uuid",
            "z_downsampled",
            "y_downsampled",
            "x_downsampled",
            "z_transformed",
            "y_transformed",
            "x_transformed",
            "transformed_coord_units",
            "z_transformed_px",
            "y_transformed_px",
            "x_transformed_px",
            "atlas_structure_number",
            "atlas_structure_acronym",
            "metadata",
        ],
    )
    df_cells = df_cells.rename(columns={"uuid": "uuid_cell"})
    df_metadata = pd.read_csv(
        metadata,
        usecols=[
            "id",
            "uuid",
            "file_path",
            "n_channels",
            "voxel_spacing",
            "voxel_spacing_units",
            "treatment",
            "time_point",
            "route",
        ],
        dtype=dtype_dict,
    )
    # df_cells['atlas_structure_acronym'] = df_cells['atlas_structure_acronym'].astype(str)
    df_metadata = df_metadata.rename(columns={"uuid": "uuid_brain"})
    df_merged = pd.merge(
        left=df_metadata, right=df_cells, how="inner", left_on="id", right_on="metadata"
    ).drop(["id"], axis=1)
    joint_file = cells.replace(".csv", ".testfile.csv")
    df_merged["metadata"] += metadata_shift
    df_merged.to_csv(joint_file, index=False)
    return joint_file

metadata = (
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/metadata.csv"
)
files = [
    
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01018_binary_df.csv",
]

for file in files:
    joint_file = join_with_metadata(file, metadata)
    
    # print(records)
    print("jointing")
    