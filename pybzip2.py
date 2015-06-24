'''
bzip2 python implementation

CDI-FIB
Joan Ginés, Albert Puente, Andrés Mingorance
'''

import os
import utils.convert as uc
from methods.MTF import *
from methods.RLE import *
from methods.BWT import *
from methods.delta import *

class pybzip2compressor:
    def __init__(self, msg, lvl=1):
        self.msg = msg
        self.compressed = None

    def compress(self):
        # Run-length encoding (RLE) of initial data
        res = rle_encode(self.msg)
        # Burrows–Wheeler transform (BWT) or block sorting
        res, bwt_column = bwt_encode(res)
        self.bwt_column = bwt_column
        # Move to front (MTF) transform
        res, mtf_stack = mtf_encode(res)
        self.mtf_stack = mtf_stack
        # Run-length encoding (RLE) of MTF result
        res = rle_encode(res)
        # Huffman coding
        # Selection between multiple Huffman tables
        # Unary base 1 encoding of Huffman table selection
        # Delta encoding (Δ) of Huffman code bit-lengths
        # Sparse bit array showing which symbols are used
        self.compressed = res

    def decompress(self):
        if self.compressed is None:
            raise Exception("Trying to decompress without having compressed")

        # Sparse bit array showing which symbols are used
        # Delta encoding (Δ) of Huffman code bit-lengths
        # Unary base 1 encoding of Huffman table selection
        # Selection between multiple Huffman tables
        # Huffman coding
        res = self.compressed
        # Run-length encoding (RLE) of MTF result
        res = rle_decode(res)
        # Move to front (MTF) transform
        res = mtf_decode((res, self.mtf_stack))
        # Burrows–Wheeler transform (BWT) or block sorting
        res = bwt_decode((res, self.bwt_column))
        # Run-length encoding (RLE) of initial data
        res = rle_decode(res)
        self.decompressed = res

file_name = "input.txt"
file_path = "input/" + file_name
file_size = os.path.getsize(file_path)

with open(file_path, "rb") as file:
    bytes = file.read(file_size)

original = bytes

C = pybzip2compressor(list(bytes))
C.compress()
C.decompress()

# print(list(original)[40:])
# print(C.compressed[40:])
# print(C.decompressed[40:])

if list(original) == C.decompressed:
    print("success")
else :
    print("Fail")
# print(original)
# print(uc.intlist2bytes(C.decompressed))

print("Compression ratio:", (1 - (len(C.compressed) / file_size)) * 100, "%")