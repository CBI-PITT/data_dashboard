from elasticsearch import Elasticsearch, helpers
import csv
import uuid
import glob
import os
import json
import pandas as pd

# file_cell = '/home/kelin/Documents/dashboard_data/klimstra/03CL13/data_for_dashboard/job_01132_binary_df_with_metadata.csv'
file_metadata = '/home/kelin/Documents/dashboard_data/klimstra/03CL02/data_for_dashboard/metadata.csv'
data = pd.read_csv(file_metadata)
print(data.columns)
print(data['voxel_spacing'])
# data = pd.read_csv(file_cell,sep='\t')
# print(data.columns)
# print(data['atlas_structure_acronym'].unique())
# data.fillna('null',inplace=True)
# print('-----------------')
# print(data['atlas_structure_acronym'].unique())
#

# print('-----------------')

# print(data_cell['atlas_structure_number'].unique())

# data = {
#     'Name': ['Alice', 'Bob', 'Charlie', 'David'],
#     'Age': [25, 30, 35.2, 28],
#     'City': ['New York', 'San Francisco', 'Chicago'],
#     'Salary': [60000.0, 75000.5, 80000.25, 55000.75]
# }

# df = pd.DataFrame(data)
# df.fillna('null',inplace=True)

# # Print the DataFrame
# print(df)
# print(df['Age'].dtypes)