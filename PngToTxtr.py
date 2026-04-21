from PIL import Image as image
import json, numpy as np
from math import log2


import MeshToModel, struct

def colourCorrect(channel):
    return round((((channel)/255)**2.2)*255)


class TxtrWriter:
    def __init__(self, img, file_path):
        self.mesh_file = open(file_path, 'wb')
        self.bytes_out = b""
        self.bytes_out_sub = b""

        pixels = img.load()
        (sx,sy) = img.size

        assert log2(sx)%1==0, "width must be a power of 2"
        assert log2(sy)%1==0, "height must be a power of 2"
            
        

        
        self.write_string("TXTR")


        self.write_4_bytes(2)
        self.write_4_bytes(2)
        self.write_2_bytes(sx) # width
        self.write_2_bytes(sy) # height
        self.write_4_bytes(1)
        self.write_4_bytes(sx*sy*4) # length in bytes
        
        for y in range(sy):
            for x in range(sx):
                pixel = pixels[x,sy-y-1]
                self.write_1_byte(pixel[0])
                self.write_1_byte(pixel[1])
                self.write_1_byte(pixel[2])
                self.write_1_byte(pixel[3])

            if y%10 == 0:
                print(y/sy)
            
            self.bytes_out += self.bytes_out_sub
            self.bytes_out_sub = b""

        self.mesh_file.write(self.bytes_out)
        self.mesh_file.close()

    def write_string(self, string):
        for i in string:
            self.write_1_byte(ord(i)) #it works

    def write_1_byte(self, value, byte_format="B"):
        self.write_bytes(byte_format, value)

    def write_2_bytes(self, value, byte_format="h"):
        self.write_bytes(byte_format, value)

    def write_4_bytes(self, value, byte_format="i"):
        self.write_bytes(byte_format, value)

    def write_float(self, value, byte_format="f"):
        self.write_bytes(byte_format, value)
            

    def write_bytes(self, byte_format, value):

        buffer = struct.pack(byte_format, value)

        self.bytes_out_sub += buffer

    

        



if __name__ == "__main__":
    img = image.open("./input/shrek.png").convert("RGBA")


    root_path = "C:/Program Files (x86)/Steam/steamapps/common/Anymaker Demo/rom/textures/"

    TxtrWriter(img, root_path+"logo.txtr")

