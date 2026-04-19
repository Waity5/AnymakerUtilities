import plyfile, numpy, ModelToMesh
from ModelManipulation import cross3, norm3


class PlyReader:
    def __init__(self, path):
        file = open(path,"rb")
        ply_mesh = plyfile.PlyData.read(file)
        file.close()

        header = []


        for i in ply_mesh.header.split("\n"):
            if "property" in i:
                cur = i[i.find(" ",9)+1:]
                header.append(cur)

        #print(header)
        
        raw_points = ply_mesh.elements[0].data
        raw_tris = ply_mesh.elements[1].data

        self.vertices = []

        for i in raw_points:
            self.vertices.append({
                "pos":[
                    float(i[header.index("x")]),
                    float(i[header.index("y")]),
                    float(i[header.index("z")])
                    ],
                "colour":{
                    "r":int(i[header.index("red")]),
                    "g":int(i[header.index("green")]),
                    "b":int(i[header.index("blue")]),
                    "a":int(i[header.index("alpha")]),
                    },
                "normal":[
                    [],
                    [],
                    [],
                    ]
                })

        


        self.triangles = []

        for i in raw_tris:
            self.triangles.append({
                "index0":int(i[0][0]),
                "index1":int(i[0][1]),
                "index2":int(i[0][2]),
                })
            points = [self.vertices[int(i[0][j])] for j in range(3)]
            normal = cross3(points[0]["pos"],points[1]["pos"],points[2]["pos"])
            if max(normal) != min(normal) != 0:
                normal = norm3(normal)
                for j in points:
                    for k in range(3):
                        j["normal"][k].append(normal[k])

        for i in self.vertices:
            if len(i["normal"][0]) > 0:
                for j in range(3):
                    i["normal"][j] = sum(i["normal"][j])/len(i["normal"][j])
            else:
                i["normal"] = [0,0,0]
            
            


if __name__ == "__main__":
    model = PlyReader("C:/Users/Waity5/AppData/Local/GitHubDesktop/stuff/AnymakerUtilities/output/shrek_small.ply")

    output = ModelToMesh.MeshWriter(model,"C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/electric_relay.mesh","C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/electric_relay original.mesh")
    
