import struct

class MeshReader:
    def __init__(self, file_path, offset=12):
        self.vertex_element_size = {
            (3,1): 12, # position
            (5,2): 4, # colour
            (2,3): 8, # U V texture co-ords I think
            (3,4): 12, # normal vector I think
            (3,5): 12, # no idea
            }
        self.triangle_size = 12 # each triagles is make of 3 32 bit ints

        self.file_path = file_path
        self.mesh_file = open(file_path, 'rb')
        self.read_master_header()

        if self.header["mesh_count"] == 0:
            self.close()
            return
        
        self.read_header(offset)
        self.read_triangles()
        self.estimated_vertex_size = self.vertices_size/(self.max_index+1) # this gives either 48, 36, 28, or 16
        assert self.estimated_vertex_size == self.vertex_size or self.estimated_vertex_size == 0
        self.read_vertices()

        self.close()
    

    def read_master_header(self):
        self.header = {
            'file_type': self.read_string(offset=0, num_bytes=4),
            'header4': self.read_4_bytes(offset=4),
            'mesh_count': self.read_4_bytes(offset=8), 
        }
        assert self.header["header4"] == 5 # version number?

    

    def read_header(self,offset):
        
        self.header['mesh_name_length'] = self.read_4_bytes(offset=offset)

        self.header["mesh_name"] = self.read_string(offset=offset+4, num_bytes=self.header["mesh_name_length"])

        offset += self.header["mesh_name_length"]

        i = 4
        self.header["vertex_format"] = []
        while self.read_4_bytes(offset=offset+i) != 0:
            self.header["vertex_format"].append((
                self.read_4_bytes(offset=offset+i),
                self.read_4_bytes(offset=offset+i+4)
                ))
            i += 8

        self.vertex_size = 0
        for i in self.header["vertex_format"]:
            self.vertex_size += self.vertex_element_size[i]
            
            
        #print(self.header["vertex_format"],self.vertex_size)


        self.header["texture1_name_length"] = self.read_4_bytes(offset=72+offset)
        self.header["texture1_name"] = self.read_string(offset=76+offset, num_bytes=self.header["texture1_name_length"])
        offset += self.header["texture1_name_length"]

        self.header["texture2_name_length"] = self.read_4_bytes(offset=76+offset)
        self.header["texture2_name"] = self.read_string(offset=80+offset, num_bytes=self.header["texture2_name_length"])
        offset += self.header["texture2_name_length"]

        self.header["texture3_name_length"] = self.read_4_bytes(offset=80+offset)
        self.header["texture3_name"] = self.read_string(offset=84+offset, num_bytes=self.header["texture3_name_length"])
        offset += self.header["texture3_name_length"]

        self.header["texture4_name_length"] = self.read_4_bytes(offset=84+offset)
        self.header["texture4_name"] = self.read_string(offset=88+offset, num_bytes=self.header["texture4_name_length"])
        offset += self.header["texture4_name_length"]

        self.header["texture5_name_length"] = self.read_4_bytes(offset=88+offset)
        self.header["texture5_name"] = self.read_string(offset=92+offset, num_bytes=self.header["texture5_name_length"])
        offset += self.header["texture5_name_length"]

        # why are there so many possible textures???
        # also, what does it even mean to have multiple textures for a single mesh
        

        self.vertices_start = 144+offset
        self.vertices_size = self.read_4_bytes(offset=140+offset)
        offset += self.vertices_size
        
        self.triangles_start = 148+offset
        self.triangles_size = self.read_4_bytes(offset=offset+144)
        offset += self.triangles_size

        self.end_of_mesh = 148+offset

        

    def read_vertices(self):
        self.vertices = []
        vertex_format = self.header["vertex_format"]

        for i in range(self.vertices_start,self.vertices_start+self.vertices_size,self.vertex_size):
            offset = i
            vertex = {}
            for j in vertex_format:
                if j == (3,1): # pos
                    vertex["pos"] = [ # y is up, z is forwards
                        self.read_float(offset = offset+0),
                        self.read_float(offset = offset+4),
                        self.read_float(offset = offset+8),
                        ]
                
                elif j == (5,2): # colour
                    vertex["colour"] = {
                        "r":self.read_1_byte(offset = offset+0),
                        "g":self.read_1_byte(offset = offset+1),
                        "b":self.read_1_byte(offset = offset+2),
                        "a":self.read_1_byte(offset = offset+3),
                        }

                elif j == (2,3): # probably U V co-ords
                    vertex["U"] = self.read_float(offset = offset+0),
                    vertex["V"] = self.read_float(offset = offset+0),

                elif j == (3,4): # normal vector
                    vertex["normal"] = [
                        self.read_float(offset = offset+0),
                        self.read_float(offset = offset+4),
                        self.read_float(offset = offset+8),
                        ]

                elif j == (3,5): # no clue
                    None

                else:
                    print(j,vertex_format,self.file_path)
                    assert 1!=1, "Unknown vertex element"

                offset += self.vertex_element_size[j]
            self.vertices.append(vertex)

        
        
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



def MultipleMeshReader(file_path):
    mesh = MeshReader(file_path)

    if mesh.header["mesh_count"] == 0:
        return []

    meshes = [mesh]
    for i in range(1,mesh.header["mesh_count"]):
        meshes.append(MeshReader(file_path,offset=meshes[-1].end_of_mesh))

    return meshes






if __name__ == "__main__":
    from glob import glob as glob # glob

    root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/"
    
    #search = [root+"brake_a_b.mesh"]
    #search = [root+"square_headlight_a.mesh"]
    #search = [root+"radiator_a_0_0_0.mesh"]
    #search = [root+"engine_block_a_0_0_0.mesh"]
    #search = [root+"natural_environment/foliage/big_leaf_maples_a.mesh"]
    #search = [root+"natural_environment/lightning_bolt.mesh"]
    #search = [root+"animals/animal_alaska_mountain_goat/alaska_mountain_goat.mesh"]
    search = glob(root+"/**/*.mesh",recursive=True)
    
    search_num = len(search)

    meshes_max = 0
    for i in range(search_num):
        foundZeros = False

        cur_path = search[i]
        #print(cur_path)

        try:
            models = MultipleMeshReader(cur_path)
        except:
            print(cur_path)
            assert 1!=1, "Load failed"
            
        for model in models:
            if True:
                has_texture = False
                for i in range(5):
                    has_texture = has_texture or model.header["texture"+str(i+1)+"_name"]!=""
                if has_texture:
                    for i in range(5):
                        print(i+1,model.header["texture"+str(i+1)+"_name"])
                    print()
                
                if model.estimated_vertex_size != model.vertex_size:
                    None
                    #print(model.estimated_vertex_size)
                    #print(cur_path)

                if model.estimated_vertex_size == 28:
                    None
                    #print(model.estimated_vertex_size)
                    #print(cur_path)

                if model.header["mesh_name_length"] == 16:
                    None
                    #print(cur_path)

                #if model.header["mesh_count"]==2:
                #    print(cur_path)

                #if model.header["texture1_name_length"] > 0 or model.header["texture2_name_length"] > 0:
                #    print(cur_path)

                if model.estimated_vertex_size == model.vertex_size:
                    #for j in model.vertices:
                    #    if j["what1"] != 0:
                    #        foundZeros = True
                    #    if j["what2"] != 0:
                    #        foundZeros = True
                    None
                    
                    #print(i["colour"])
                #if foundZeros:
                #    print(cur_path)
