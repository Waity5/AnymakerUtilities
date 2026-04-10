import plyfile, numpy

def PlyWriter(mesh, path):
    vertexes = numpy.array([tuple(i["pos"])+(i["colour"]["r"],i["colour"]["g"],i["colour"]["b"],i["colour"]["a"]) for i in mesh.vertices],
                dtype=[('x', 'f4'), ('z', 'f4'),('y', 'f4'),('red', 'u1'),('green', 'u1'),('blue', 'u1'),('alpha', 'u1')])

    faces = numpy.array([([i["index0"],i["index1"],i["index2"]],) for i in mesh.triangles],
                dtype=[('vertex_indices', 'i4', (3,))])

    el1 = plyfile.PlyElement.describe(vertexes, 'vertex')
    el2 = plyfile.PlyElement.describe(faces, 'face')

    plyfile.PlyData([el1,el2]).write(path)

