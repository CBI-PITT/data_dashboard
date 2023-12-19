from bg_atlasapi import show_atlases
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
import csv

# atlas_mouse_25 = BrainGlobeAtlas("allen_mouse_25um")
# atlas_mouse_10 = BrainGlobeAtlas("allen_mouse_10um")

# # structure_acronyms_25 = [
# #     structure["acronym"] for structure in atlas_mouse_25.structures.values()
# # ]
# structure_acronyms_10 = [
#     structure["acronym"] for structure in atlas_mouse_10.structures.values()
# ]
# # Print the list of structure acronyms
# # map_25 = {}
# # print("Map_25 in process")
# # for acronym in structure_acronyms_25:
# #     temp = atlas_mouse_25.get_structure_mask(acronym)
# #     volume = temp[temp > 0].shape[0]
# #     map_25[acronym] = volume

# map_10 = {}
# print("Map_10 in process")
# for acronym in structure_acronyms_10:
#     temp = atlas_mouse_10.get_structure_mask(acronym)
#     volume = temp[temp > 0].shape[0]
#     map_10[acronym] = volume

#     # Specify the CSV file name
# # csvfile = "atlas_mouse_aconym&volume.csv"
# csv_file_10 = "atlas_mouse_10um_aconym&volume.csv"

# # Write the data to the CSV file
# with open(csv_file_10, "w", newline="") as csvfile:
#     fieldnames = [
#         "acronym",
#         "volume_um_10",
#         "volume_mm_10",
#     ]  # Define the header row
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Write the header row
#     writer.writeheader()

#     # Write the data
#     # for name, value in map_25.items():
        
#     #     writer.writerow(
#     #         {
#     #             "acronym": name,
#     #             "volume_um_10":map_10['name'],
#     #             "volume_mm_10":map_10['name'] * 0.01**3,
#     #             "volume_um_25": value,
#     #             "volume_mm_25": value * 0.025**3,
#     #         }
#     #     )
#     for name, value in map_10.items():
#         print(name,value)
#         writer.writerow(
#             {"acronym": name, "volume_um_10": value, "volume_mm_10": value * 0.01**3}
#         )

# print(f"Data has been written to {csv_file_10}.")


atlas_mouse_25 = BrainGlobeAtlas("allen_mouse_25um")
atlas_mouse_10 = BrainGlobeAtlas("allen_mouse_10um")

structure_acronyms_25 = [
    structure["acronym"] for structure in atlas_mouse_25.structures.values()
]
structure_acronyms_10 = [
    structure["acronym"] for structure in atlas_mouse_10.structures.values()
]
# Print the list of structure acronyms
map_25 = {}
print("Map_25 in process")
for acronym in structure_acronyms_25:
    temp = atlas_mouse_25.get_structure_mask(acronym)
    volume = temp[temp > 0].shape[0]
    map_25[acronym] = volume

map_10 = {}
print("Map_10 in process")
for acronym in structure_acronyms_10:
    temp = atlas_mouse_10.get_structure_mask(acronym)
    volume = temp[temp > 0].shape[0]
    map_10[acronym] = volume

    # Specify the CSV file name
csvfile = "atlas_mouse_aconym&volume.csv"


# Write the data to the CSV file
with open(csvfile, "w", newline="") as csvfile:
    fieldnames = [
        "acronym",
        "volume_um_10",
        "volume_mm_10",
        "volume_um_25",
        "volume_mm_25",
    ]  # Define the header row
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write the header row
    writer.writeheader()

    # Write the data
    for name, value in map_25.items():
        print(f'writing: {name}')
        writer.writerow(
            {
                "acronym": name,
                "volume_um_10":map_10[name],
                "volume_mm_10":map_10[name] * 0.01**3,
                "volume_um_25": value,
                "volume_mm_25": value * 0.025**3,
            }
        )
    

# print(f"Data has been written to {csvfile}.")
# atlas_mouse_25 = BrainGlobeAtlas("allen_mouse_25um")
# temp = atlas_mouse_25.get_structure_mask('CUL4, 5')
# volume = temp[temp > 0].shape[0]
# print(volume)