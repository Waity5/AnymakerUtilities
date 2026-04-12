from MeshToModel import MeshReader
from ModelToPly import PlyWriter
import json
from ModelManipulation import *

grid_size = 0.08

def PartModelLoader (anymaker_root_path, part_id, extension=(0,0,0)):
    definitions = json.load(open(anymaker_root_path+"/rom/data/vehicle_component_definitions.json"))["definitions"]

    part_definition = None
    for i in definitions:
        if i["id"] == part_id:
            part_definition = i

    assert part_definition != None # Part ID not found

    modelBasePath = anymaker_root_path+"/rom/"
    modelName = part_definition["mesh_static"]["mesh_path"]
    model = MeshReader(modelBasePath + modelName)
    
    if not ("interval" in part_definition):
        return model
    interval = part_definition["interval"]


    tile_axes = [0,0,0]
    for i in range(3):
        mode_cur = "mode_" + "xyz"[i]
        if (mode_cur in part_definition) and (part_definition[mode_cur] == "tile"):
            tile_axes[i] = extension[i]//interval[i] + 1

    if max(tile_axes) > 0:
        for x in range(0,tile_axes[0]+1):
            for y in range(0,tile_axes[1]+1):
                for z in range(0,tile_axes[2]+1):
                    if x+y+z > 0:
                        modelNameX = 2 if (x==tile_axes[0] and tile_axes[0]>0) else min(x,1)
                        modelNameY = 2 if (y==tile_axes[1] and tile_axes[1]>0) else min(y,1)
                        modelNameZ = 2 if (z==tile_axes[2] and tile_axes[2]>0) else min(z,1)
                        
                        newModelName = modelName[:modelName.find(".mesh")-5]
                        newModelName += "{0:d}_{1:d}_{2:d}.mesh".format(modelNameX,modelNameY,modelNameZ)
                        
                        newModel = MeshReader(modelBasePath + newModelName)
                        newModel = ModelMove(newModel, mul3((
                                x*interval[0]-max(interval[0]-1,0),
                                y*interval[1]-max(interval[1]-1,0),
                                z*interval[2]-max(interval[2]-1,0)),
                            grid_size)) # this isn't great, but engines need offsets of 1,3,5, not 2,4,6, which is annoying
                        model = ModelCombine(model, newModel)
    

    if "center_stretch" in part_definition:
        center_stretch = part_definition["center_stretch"]
        
        for i in range(3):
            mode_cur = "mode_" + "xyz"[i]
            if (extension[i] > 0) and (mode_cur in part_definition) and (part_definition[mode_cur] == "stretch"):
                cur_extension = [0, 0, 0]
                cur_extension[i] = extension[i]*grid_size
                model = ModelStretch(model, cur_extension, mul3(center_stretch,grid_size))



    return model


if __name__ == "__main__":
    #name = "liquid_pump"
    #name = "drive_shaft"
    #name = "radiator"
    #name = "engine"
    #name = "liquid_tank"
    #name = "tool_wall"
    name = "drive_shaft_c"
    
    
    model = PartModelLoader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo", name, extension = (10,10,10))
    
    
    PlyWriter(model, "./output/"+name+".ply")
