from MeshToData import MeshReader
from DataToPly import PlyWriter



#name = "liquid_fill"
#name = "liquid_pump_a"
#name = "motorcycle_wheel"
#name = "differential_gearbox_a"
#name = "lizard_creature_c_lod"
#name = "food_canned_bread"
#name = "test_playground"
#name = "brake_a"
#name = "brake_a_b"
#name = "engine_block_a_0_0_0"
#name = "engine_block_a_0_0_1"
name = "engine_block_a_0_0_2"

newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/"+name+".mesh")
#newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/animals/lizard_creature_c/"+name+".mesh")
#newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/inventory/"+name+".mesh")
#newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/"+name+".mesh")

PlyWriter(newMesh, "./output/"+name+".ply")
