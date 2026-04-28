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
    name = "radiator_a_0_0_0"

    newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/animals/lizard_creature_c/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/inventory/"+name+".mesh")
    #newMesh = MeshReader("C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/"+name+".mesh")

    #newMesh = MeshCombiner(newMesh,newMesh)

    PlyWriter(newMesh, "./output/"+name+".ply")

