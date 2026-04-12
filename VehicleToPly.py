from PartModelLoader import PartModelLoader
from ModelManipulation import *
from ModelToPly import PlyWriter
import json

grid_size = 0.08

#name = "modularengine1_1 - Copy"
name = "Pinzgauer"
#name = "jeep2"

vehicle = json.load(open("C:/Users/Waity5/AppData/Roaming/Anymaker/creations/"+name+".data"))
anymaker_root_path = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo"

component_list = vehicle["definitions"]["components"]
component_models = [PartModelLoader(anymaker_root_path, i) for i in component_list]

model = ModelCreate()

for subgrid in vehicle["vehicles"]["vehicles"]:
    submodel = ModelCreate()
    components = subgrid["grids"][0]["components"]

    component_count = len(components)
    for component_index in range(component_count):
        component = components[component_index]
        print("Component {0:d}/{1:d}".format(component_index+1,component_count))

        if "ext" in component:
            cur_model = PartModelLoader(anymaker_root_path, component_list[component["def"]], extension = component["ext"])
        else:
            cur_model = component_models[component["def"]]

        if "rot" in component:
            cur_model = ModelRotate(cur_model, component["rot"])

        if "pos" in component:
            cur_model = ModelMove(cur_model, mul3(component["pos"],grid_size))

        #if component_list[component["def"]].find("light") == -1:
        submodel = ModelCombine(submodel, cur_model)

    submodel = ModelRotate(submodel, subgrid["transform"]["m"])

    submodel = ModelMove(submodel, subgrid["transform"]["t"])
    
    model = ModelCombine(model, submodel)

PlyWriter(model, "./output/"+name+".ply")
