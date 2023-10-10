from bg_atlasapi import show_atlases
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
atlas_mouse_25 = BrainGlobeAtlas("allen_mouse_25um")
atlas_mouse_10 = BrainGlobeAtlas("allen_mouse_10um")
root_25 = atlas_mouse_25.get_structure_mask('root')
root_25_px = root_25[root_25 > 0].shape[0]
# print(root_25)
mob_25 = atlas_mouse_25.get_structure_mask('MOB')  # olfactory bulb
# print(mob_25[mob_25 > 0])
mob_25_px = mob_25[mob_25 > 0].shape[0]
mob_volumn = mob_25_px/root_25_px
print("mob_25_px" , mob_25_px)
print("root_25_px" , root_25_px)

mob_10 = atlas_mouse_10.get_structure_mask('MOB')
mob_10_px = mob_10[mob_10 > 0].shape[0]
print("mob_10_px" , mob_10_px)
# show_atlases()

# null_25 = atlas_mouse_25.get_structure_mask('null')
# print(null_25)