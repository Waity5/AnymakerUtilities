import struct

class MeshReader:
    def __init__(self, file_path):
        self.vertex_size = 36 # each vertex is 36 bytes
        self.triangle_size = 12 # each triagles is make of 3 32 bit ints

        self.file_path = file_path
        self.mesh_file = open(file_path, 'rb')
        self.read_header()
        self.read_triangles()
        self.estimated_vertex_size = self.vertices_size/(self.max_index+1)
        self.read_vertices()

        self.close()

    def read_header(self):
        self.header = {
            'file_type': self.read_string(offset=0, num_bytes=4),
            'header4': self.read_4_bytes(offset=4),
            'mesh_count': self.read_4_bytes(offset=8),
        }
        
        
        self.header['mesh_name_length'] = self.read_4_bytes(offset=12)


        assert self.header["header4"] == 5 # version number?

        name_len = self.header["mesh_name_length"]

        self.header["mesh_name"] = self.read_string(offset=16, num_bytes=name_len)

        
        #self.header["header6"] = self.read_4_bytes(offset=16+name_len)
        #self.header["header7"] = self.read_4_bytes(offset=20+name_len)
        #self.header["header8"] = self.read_4_bytes(offset=24+name_len)
        #self.header["header9"] = self.read_4_bytes(offset=28+name_len)

        for i in range(16,152,4):
            self.header["header"+str(i)] = self.read_4_bytes(offset=i+name_len)

        self.vertices_start = 156+name_len
        self.vertices_size = self.read_4_bytes(offset=152+name_len)
        # each vertex appears to be 36 bytes long


        self.triangles_start = 160+name_len+self.vertices_size
        self.triangles_size = self.read_4_bytes(offset=self.triangles_start-4)

        # the header seems mostly empty, and consistent from file to file
        

    def read_vertices(self):
        self.vertices = []
        for i in range(self.vertices_start,self.vertices_start+self.vertices_size,self.vertex_size):
            self.vertices.append({
                "pos":[
                    self.read_float(offset = i+0),
                    self.read_float(offset = i+4),
                    self.read_float(offset = i+8),
                    ],
                "colour":{
                    "r":self.read_1_byte(offset = i+12),
                    "g":self.read_1_byte(offset = i+13),
                    "b":self.read_1_byte(offset = i+14),
                    "a":self.read_1_byte(offset = i+15),
                    },
                "normal":[
                    self.read_float(offset = i+24),
                    self.read_float(offset = i+28),
                    self.read_float(offset = i+32),
                    ]
                }) # bytes 16-23 seem to always be zero, not sure what they're for
            #if self.read_4_bytes(offset = i+16) != 0:
            #    print(self.file_path)
            #if self.read_4_bytes(offset = i+16) != 0:
            #    self.vertices[-1]["colour"] = {"r":0,"g":255,"b":0,"a":255}
        
    def read_triangles(self):
        self.max_index = 0
        self.triangles = []
        for i in range(self.triangles_start,self.triangles_start+self.triangles_size,self.triangle_size):
            self.triangles.append({
                "index0":self.read_4_bytes(offset=i+0),
                "index1":self.read_4_bytes(offset=i+4),
                "index2":self.read_4_bytes(offset=i+8),
                })

        for i in self.triangles:
            self.max_index = max(self.max_index, i["index0"], i["index1"], i["index2"])

    def read_1_byte(self, offset, byte_format='B'):
        # B - unsigned char, b - signed char
        return self.read_bytes(offset=offset, num_bytes=1, byte_format=byte_format)[0]

    def read_2_bytes(self, offset, byte_format="h"):
        # H - uint16, h - int16
        return self.read_bytes(offset=offset, num_bytes=2, byte_format=byte_format)[0]

    def read_4_bytes(self, offset, byte_format='i'):
        # I - uint32, i - int32
        return self.read_bytes(offset=offset, num_bytes=4, byte_format=byte_format)[0]

    def read_float(self, offset):

        return self.read_4_bytes(offset, byte_format="f")

    def read_string(self, offset, num_bytes=8):
        
        # c - char
        
        #if self.read_1_byte(offset, byte_format='c').decode('ascii') == "-": #needed for some WADs like CATWALK.WAD, not sure why
        #    return "-"
        return ''.join(b.decode('ascii') for b in
                       self.read_bytes(offset, num_bytes, byte_format='c' * num_bytes)
                       if ord(b) != 0)


    def read_bytes(self, offset, num_bytes, byte_format):
        self.mesh_file.seek(offset)
        buffer = self.mesh_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)

    def close(self):
        self.mesh_file.close()


if __name__ == "__main__":
    from glob import glob as glob

    root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/components/"
    
    #search = [root+"brake_a_b.mesh"]
    #search = [root+"square_headlight_a.mesh"]
    search = glob(root+"*.mesh")
    search_num = len(search)

    meshes_max = 0
    for i in range(search_num):
        model = MeshReader(search[i])
        meshes_max = max(meshes_max,model.header["mesh_count"])
        if i%10 == 0:
            None
            #print("{0:d}/{1:d}".format(i+1,search_num))

        #print(model.vertices_size)
        if model.estimated_vertex_size != model.vertex_size:
            print(model.estimated_vertex_size)
            #print(search[i])

        #if model.header["mesh_count"]==2:
        #    print(search[i])
        
    
