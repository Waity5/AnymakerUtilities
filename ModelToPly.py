import plyfile, numpy

def PlyWriter(mesh, path):
    vertexes = numpy.array([tuple(i["pos"])+(i["colour"]["r"],i["colour"]["g"],i["colour"]["b"],i["colour"]["a"]) for i in mesh.vertices],
                dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4'),('red', 'u1'),('green', 'u1'),('blue', 'u1'),('alpha', 'u1')])

    faces = numpy.array([([i["index0"],i["index1"],i["index2"]],) for i in mesh.triangles],
                dtype=[('vertex_indices', 'i4', (3,))])

    el1 = plyfile.PlyElement.describe(vertexes, 'vertex')
    el2 = plyfile.PlyElement.describe(faces, 'face')

    plyfile.PlyData([el1,el2]).write(path)



if __name__ == "__main__":
    from MeshToModel import MeshReader


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
    #name = "engine_block_a_0_0_2"
    #name = "fuel_tank_a_0_0_0"
    #name = "radiator_a_0_0_0"
    #name = "lightning_bolt"
    #name = "muzzle_flash"
    #name = "elev45_a_b"
    name = "square_headlight_a"

    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/animals/lizard_creature_c/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/inventory/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/natural_environment/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/bunker_design/"+name+".mesh")
    newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/animals/animal_spotted_owl/spotted_owl.mesh")
    print("Vertex size:",newMesh.estimated_vertex_size)
    print("Text 1 name:",newMesh.header["texture1_name"])
    print("Text 2 name:",newMesh.header["texture2_name"])
    print("Mesh count:",newMesh.header["mesh_count"])
    #newMesh = MeshCombiner(newMesh,newMesh)

    PlyWriter(newMesh, "./output/"+name+".ply")

