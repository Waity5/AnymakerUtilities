from copy import deepcopy as dcopy
from math import dist

# surely this is the propper way to use classes

def dot3(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def add3(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def sub3(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def mul3(a,b):
    return (a[0]*b, a[1]*b, a[2]*b)

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

def cross3(a, b, c):
    return cross(sub3(b,a), sub3(c,a))

def norm3(a):
    return mul3(a,1/dist(a,(0,0,0)))



class ModelCombine:
    def __init__(self, mesh1, mesh2):
        self.vertices = mesh1.vertices + dcopy(mesh2.vertices)
        vertices_count = len(mesh1.vertices)
        triangles2 = dcopy(mesh2.triangles)
        for i in triangles2:
            for j in i:
                i[j]+=vertices_count
        self.triangles = mesh1.triangles + triangles2

class ModelMove:
    def __init__(self, mesh, offset):
        self.vertices = dcopy(mesh.vertices)
        self.triangles = dcopy(mesh.triangles)

        for i in self.vertices:
            i["pos"] = add3(i["pos"], offset)

class ModelStretch:
    def __init__(self, mesh, offset, center_stretch):
        self.vertices = dcopy(mesh.vertices)
        self.triangles = dcopy(mesh.triangles)

        for i in self.vertices:
            if dot3(sub3(i["pos"],center_stretch),offset) > 0:            
                i["pos"] = add3(i["pos"], offset)
            
class ModelRotate:
    def __init__(self, mesh, matrix):
        self.vertices = dcopy(mesh.vertices)
        self.triangles = dcopy(mesh.triangles)

        for i in self.vertices:
            i["pos"] = (
                i["pos"][0] * matrix[0] + i["pos"][1] * matrix[3] + i["pos"][2] * matrix[6],
                i["pos"][0] * matrix[1] + i["pos"][1] * matrix[4] + i["pos"][2] * matrix[7],
                i["pos"][0] * matrix[2] + i["pos"][1] * matrix[5] + i["pos"][2] * matrix[8],
                )

class ModelExtend: # unfinished, meant to be used to make beams and wires
    def __init__(self, mesh, pos1, pos2):
        diff = sub3(pos2,pos1)

        self.triangles = dcopy(mesh.triangles)

        verts = set(range(len(mesh.vertices)))
        mesh1_verts = dcopy(verts)
        for i in range(len(mesh.triangles)-1,-1,-1):
            cur = mesh.triangles[i]
            normal = cross3(mesh.vertices[cur["index0"]]["pos"],mesh.vertices[cur["index1"]]["pos"],mesh.vertices[cur["index2"]]["pos"])

            if dot3(diff,normal)>0:
                for j in cur:
                    mesh1_verts.discard(cur[j])
                mesh.triangles.pop(i)
        

class ModelCreate:
    def __init__(self):
        self.vertices = []
        self.triangles = []


if __name__ == "__main__":
    import PlyToModel, ModelToPly

    model = PlyToModel.PlyReader("./data/beam.ply")

    model = ModelExtend(model,(0,0,0),(5,5,0))

    ModelToPly.PlyWriter(model,"./output/beam.ply")
