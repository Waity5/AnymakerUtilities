from PIL import Image as image
import json, numpy as np, struct


class TxtrReader:
    def __init__(self,file_path):

        self.file_path = file_path
        self.mesh_file = open(file_path, 'rb')

        self.read_header()
        self.read_image()

    def read_header(self):
        self.header = {
            'file_type': self.read_string(offset=0, num_bytes=4),
            'header4': self.read_4_bytes(offset=4),
            'header8': self.read_4_bytes(offset=4),
            'width': self.read_2_bytes(offset=12),
            'height': self.read_2_bytes(offset=14),
            'header16': self.read_4_bytes(offset=16),
            'length': self.read_4_bytes(offset=20),
        }

    def read_image(self):
        sx, sy = self.header["width"], self.header["height"]
        self.img = image.new(mode="RGBA",size=[sx,sy])
        pixels = self.img.load()
        offset = 24
        
        for y in range(sy):
            for x in range(sx):
                pixels[x, sy-y-1] = (
                    self.read_1_byte(offset = offset+0),
                    self.read_1_byte(offset = offset+1),
                    self.read_1_byte(offset = offset+2),
                    self.read_1_byte(offset = offset+3)
                    )
                offset += 4

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



if __name__ == "__main__":
    from glob import glob as glob # glob
    #root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/animals/"
    #root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/meshes/natural_environment/"
    root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/textures/"
    root = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/textures/weather/"

    #name = "spruce_large"
    
    #img = TxtrReader(root+name+".txtr").img

    #img.save("./output/"+name+".png")

    names = [i.replace("\\","/") for i in glob(root+"*.txtr")]
    

    for i in names:
        img = TxtrReader(i).img

        img.save("./output/"+i.split("/")[-1].split(".")[0]+".png")
