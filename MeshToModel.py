import struct

class MeshReader:
    def __init__(self, file_path):
        self.vertex_size = 36 # each vertex is 36 bytes
        self.triangle_size = 12 # each triagles is make of 3 32 bit ints
        # todo: add support for meshes with 16 and 28-size vertices

        self.file_path = file_path
        self.mesh_file = open(file_path, 'rb')
        self.read_header()
        self.read_triangles()
        self.estimated_vertex_size = self.vertices_size/(self.max_index+1) # this gives either 36, 28, or 16
        self.read_vertices()

        self.close()

    def read_header(self):
        self.header = {
            'file_type': self.read_string(offset=0, num_bytes=4),
            'header4': self.read_4_bytes(offset=4),
            'mesh_count': self.read_4_bytes(offset=8), 
        }
        # todo: read from multiple meshes in the same file
        # this is easy programming-wise but I'm not sure how to structure it with the whole return-class-as-model thing
        
        
        self.header['mesh_name_length'] = self.read_4_bytes(offset=12)


        assert self.header["header4"] == 5 # version number?

        name_len = self.header["mesh_name_length"]

        self.header["mesh_name"] = self.read_string(offset=16, num_bytes=name_len)

        offset = name_len

        
        #self.header["header6"] = self.read_4_bytes(offset=16+name_len)
        #self.header["header7"] = self.read_4_bytes(offset=20+name_len)
        #self.header["header8"] = self.read_4_bytes(offset=24+name_len)
        #self.header["header9"] = self.read_4_bytes(offset=28+name_len)

        for i in range(16,84,4):
            self.header["header"+str(i)] = self.read_4_bytes(offset=i+offset)

        self.header["texture1_name_length"] = self.read_4_bytes(offset=84+offset)
        self.header["texture1_name"] = self.read_string(offset=88+offset, num_bytes=self.header["texture1_name_length"])
        offset += self.header["texture1_name_length"]

        self.header["texture2_name_length"] = self.read_4_bytes(offset=88+offset)
        self.header["texture2_name"] = self.read_string(offset=92+offset, num_bytes=self.header["texture2_name_length"])
        offset += self.header["texture2_name_length"]

        
        

        self.vertices_start = 156+offset
        self.vertices_size = self.read_4_bytes(offset=152+offset)


        offset += self.vertices_size
        self.triangles_start = 160+offset
        self.triangles_size = self.read_4_bytes(offset=offset+156)

        

    def read_vertices(self):
        self.vertices = []

        if self.estimated_vertex_size == self.vertex_size:
            for i in range(self.vertices_start,self.vertices_start+self.vertices_size,self.vertex_size):
                self.vertices.append({
                    "pos":[ # y is up, z is forwards
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
                        ],
                    "what1":self.read_4_bytes(offset = i+16),
                    "what2":self.read_4_bytes(offset = i+20),
                    }) # bytes 16-23 seem to mostly be zero (other than inventory meshs), not sure what they're for (maybe glow effects?)

        elif self.estimated_vertex_size == 28:
            for i in range(self.vertices_start,self.vertices_start+self.vertices_size,28):
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
                        self.read_float(offset = i+16),
                        self.read_float(offset = i+20),
                        self.read_float(offset = i+24),
                        ],
                    })
        
        elif self.estimated_vertex_size == 16:
            for i in range(self.vertices_start,self.vertices_start+self.vertices_size,16):
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
                    })

        elif self.estimated_vertex_size != 0:
            print(self.file_path)
            assert 1!=1, "estimated vertex size is not accounted for"
        
        
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
    from glob import glob as glob # glob

    root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/"
    
    #search = [root+"brake_a_b.mesh"]
    #search = [root+"square_headlight_a.mesh"]
    #search = [root+"radiator_a_0_0_0.mesh"]
    #search = [root+"engine_block_a_0_0_0.mesh"]
    search = glob(root+"/**/*.mesh",recursive=True)
    
    search_num = len(search)

    meshes_max = 0
    for i in range(search_num):
        foundZeros = False

        cur_path = search[i]
        #print(cur_path)

        try:
            model = MeshReader(cur_path)
        except:
            print(cur_path)
            assert 1!=1, "Load failed"
        
        meshes_max = max(meshes_max,model.header["mesh_count"])
        if i%10 == 0:
            None
            #print("{0:d}/{1:d}".format(i+1,search_num))

        #print(model.vertices_size)
        if model.estimated_vertex_size != model.vertex_size:
            None
            #print(model.estimated_vertex_size)
            #print(cur_path)

        if model.header["mesh_name_length"] == 16:
            None
            #print(cur_path)

        #if model.header["mesh_count"]==2:
        #    print(cur_path)

        if model.header["texture1_name_length"] > 0 or model.header["texture2_name_length"] > 0:
            print(cur_path)

        if model.estimated_vertex_size == model.vertex_size:
            #for j in model.vertices:
            #    if j["what1"] != 0:
            #        foundZeros = True
            #    if j["what2"] != 0:
            #        foundZeros = True
            None
            
            #print(i["colour"])
        if foundZeros:
            print(cur_path)
