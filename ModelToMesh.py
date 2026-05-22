import MeshToModel, struct

def colourCorrect(channel):
    return round((((channel)/255)**2.2)*255)


class MeshWriter:
    def __init__(self, model, file_path, root_file_path):
        self.vertex_size = 36 # each vertex is 36 bytes
        self.triangle_size = 12 # each triagles is make of 3 32 bit ints

        self.model_name = "torque_surface"

        self.model = model
        self.base_model = MeshToModel.MeshReader(root_file_path)
        self.mesh_file = open(file_path, 'wb')
        self.bytes_out = b""
        
        self.write_header()
        self.write_vertices()
        self.write_triangles()
        

        self.write_4_bytes(0)
        self.write_4_bytes(0) # not sure why by there's usually 8 empty bytes at the end

        self.mesh_file.write(self.bytes_out)
        self.mesh_file.close()


    def write_header(self):
        self.write_string("mesh")
        self.write_4_bytes(self.base_model.header["header4"])
        self.write_4_bytes(1) # mesh count
        self.write_4_bytes(len(self.model_name))
        self.write_string(self.model_name)

        for i in range(16,152,4):
            self.write_4_bytes(self.base_model.header["header"+str(i)])

    def write_vertices(self):
        self.write_4_bytes(self.vertex_size*len(self.model.vertices))
        
        for i in self.model.vertices:
            self.write_float(i["pos"][0])
            self.write_float(i["pos"][1])
            self.write_float(i["pos"][2])
            self.write_1_byte(colourCorrect(i["colour"]["r"]))
            self.write_1_byte(colourCorrect(i["colour"]["g"]))
            self.write_1_byte(colourCorrect(i["colour"]["b"]))
            self.write_1_byte(colourCorrect(i["colour"]["a"]))
            self.write_4_bytes(0) # bytes 16-23 are basically always empty
            self.write_4_bytes(0) # not sure what they do
            self.write_float(-i["normal"][0])
            self.write_float(-i["normal"][1])
            self.write_float(-i["normal"][2])

    def write_triangles(self):
        self.write_4_bytes(self.triangle_size*len(self.model.triangles))

        for i in self.model.triangles:
            self.write_4_bytes(i["index0"])
            self.write_4_bytes(i["index2"])
            self.write_4_bytes(i["index1"])

    def write_string(self, string):
        for i in string:
            self.write_1_byte(ord(i)) #it works

    def write_1_byte(self, value, byte_format="B"):
        self.write_bytes(byte_format, value)

    def write_4_bytes(self, value, byte_format="i"):
        self.write_bytes(byte_format, value)

    def write_float(self, value, byte_format="f"):
        self.write_bytes(byte_format, value)
            

    def write_bytes(self, byte_format, value):

        buffer = struct.pack(byte_format, value)

        self.bytes_out += buffer

    


if __name__ == "__main__":
    base = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/box1x1.mesh"
    
    model = MeshToModel.MeshReader(base)

    model.vertices = []
    model.triangles = []

    MeshWriter(model, "./output/empty.mesh", base)
        
