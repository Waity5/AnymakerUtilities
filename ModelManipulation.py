from copy import deepcopy as dcopy

# surely this is the propper way to use classes

def dot3(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def add3(a,b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def sub3(a,b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def mul3(a,b):
    return (a[0]*b, a[1]*b, a[2]*b)



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

class ModelCreate:
    def __init__(self):
        self.vertices = []
        self.triangles = []
