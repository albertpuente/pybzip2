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
from methods.HuffmanT import *
from methods.other import *

class pybzip2compressor:
    def __init__(self, msg = None, lvl=1):
        self.msg = msg
        self.content = None

    def compress(self):
        # Run-length encoding (RLE) of initial data
        res = rle_encode(self.msg)
        # Burrows–Wheeler transform (BWT) or block sorting
        res, bwt_column = bwt_encode(res)
        self.bwt_column = bwt_column
        # Move to front (MTF) transform
        res, _ = mtf_encode(res)
        # self.mtf_stack = mtf_stack
        
        # Run-length encoding (RLE) of MTF result
        res = rle2_encode(res)
        
        # Huffman coding
        coded_data, huffman_lengths, table_order = huffman_encode(res)
        self.content = bitChain(''.join(coded_data))
        self.huffman_groups = len(huffman_lengths)
        
        # Selection between multiple Huffman tables
        self.selectors_used = bitChain(len(table_order), 15)
        
        # store this to apply the mtf+unary encoding in packaging.py
        self.table_order = table_order

        # Delta encoding (Δ) of Huffman code bit-lengths
        self.delta_bit_length = []
        for lengths in huffman_lengths:
            self.delta_bit_length += [delta_encode(lengths)]
        
        # Sparse bit array showing which symbols are used
        # res is the source before huffman
        self.bit_maps = sparse(set(res))

    def decompress(self):
        if self.content is None:
            raise Exception("Trying to decompress without having compressed")

        # Sparse bit array showing which symbols are used
        symbols = unsparse(self.bit_maps)
        # Delta encoding (Δ) of Huffman code bit-lengths
        huffman_lengths = []
        for deltas in self.delta_bit_length:
            huffman_lengths += [delta_decode(deltas)]

        # Unary base 1 encoding of Huffman table selection
        # Selection between multiple Huffman tables
        # Huffman coding
        res = self.content

        res = huffman_decode(res, huffman_lengths,self.selectors_used, symbols)
        
        # Run-length encoding (RLE) of MTF result
        res = rle2_decode(res)

        # Move to front (MTF) transform
        res = mtf_decode2(res, symbols)
        
        # Burrows–Wheeler transform (BWT) or block sorting
        res = bwt_decode((res, self.bwt_column))

        # Run-length encoding (RLE) of initial data
        res = rle_decode(res)
        
        self.decompressed = res
'''
file_name = "Physics.cu"
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

print("Compression ratio:", (1 - (len(C.content) / file_size)) * 100, "%")
'''