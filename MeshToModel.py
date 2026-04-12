import struct

class MeshReader:
    def __init__(self, file_path):
        self.vertex_size = 36 # each vertex is 36 bytes
        self.triangle_size = 12 # each triagles is make of 3 32 bit ints
        
        self.mesh_file = open(file_path, 'rb')
        self.read_header()
        self.read_vertices()
        self.read_triangles()

        self.close()

    def read_header(self):
        self.header = {
            'file_type': self.read_string(offset=0, num_bytes=4),
            'header0': self.read_2_bytes(offset=4),
            'header1': self.read_2_bytes(offset=6),
            'header2': self.read_2_bytes(offset=8),
            'header3': self.read_2_bytes(offset=10),
            'mesh_name_length': self.read_2_bytes(offset=12),
            'header5': self.read_2_bytes(offset=14),
        }

        name_len = self.header["mesh_name_length"]

        self.header["mesh_name"] = self.read_string(offset=16, num_bytes=name_len)

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
        
    def read_triangles(self):
        self.triangles = []
        for i in range(self.triangles_start,self.triangles_start+self.triangles_size,self.triangle_size):
            self.triangles.append({
                "index0":self.read_4_bytes(offset=i+0),
                "index1":self.read_4_bytes(offset=i+4),
                "index2":self.read_4_bytes(offset=i+8),
                })

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
        
        if self.read_1_byte(offset, byte_format='c').decode('ascii') == "-": #needed for some WADs like CATWALK.WAD, not sure why
            return "-"
        return ''.join(b.decode('ascii') for b in
                       self.read_bytes(offset, num_bytes, byte_format='c' * num_bytes)
                       if ord(b) != 0)


    def read_bytes(self, offset, num_bytes, byte_format):
        self.mesh_file.seek(offset)
        buffer = self.mesh_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)

    def close(self):
        self.mesh_file.close()
