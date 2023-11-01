import pandas as pd

files = [
    # "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00836_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00834_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00833_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/02CL89/data_for_dashboard/job_00835_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01179_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01181_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01202_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01103_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01174_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01178_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01109_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01151_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01115_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01175_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01159_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01161_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01116_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01111_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01182_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01106_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01093_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL12/data_for_dashboard/job_01117_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01251_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01250_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01255_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01249_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/cebra/03CL47/data_for_dashboard/job_01253_df_for_dashboard.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01081_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01083_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01084_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01087_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01107_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01132_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01133_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01198_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00914_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00917_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00922_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00931_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00960_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00963_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00968_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00970_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00973_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00978_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00983_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00991_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_00999_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01016_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01017_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01018_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01068_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01077_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01102_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01105_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01124_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/job_01128_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/01CL73/data_for_dashboard/00076_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/01CL73/data_for_dashboard/00077_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/01CL73/data_for_dashboard/00078_binary_df.csv",
    "/home/kelin/Documents/dashboard_data/klimstra/01CL73/data_for_dashboard/00142_binary_df.csv",
]

def process_csv_file(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check for columns without column names and remove them
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, index=False)
        print(f"Processed file: {file_path}")

    except Exception as e:
        print(f"Error processing file: {file_path}\nError: {e}")

# Process all CSV files in the list
for file_path in files:
    process_csv_file(file_path)