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
        print ("pyzbzip2 initialized")
        print ("msg = ", msg)
        self.msg = msg
        self.content = None

    def compress(self):
        print ("Start compress()")
        print ("MSG: ", self.msg)
        
        # Run-length encoding (RLE) of initial data
        res = rle_encode(self.msg)
        print ("RLE: ", res)
        
        # Burrows–Wheeler transform (BWT) or block sorting
        res, bwt_column = bwt_encode(res)
        self.bwt_column = bwt_column
        print ("BWT RES: ", res)
        print ("BWT COL: ", bwt_column)
        
        # Move to front (MTF) transform
        res, _ = mtf_encode(res)
        print ("MTF: ", res)
        # self.mtf_stack = mtf_stack
        
        # Run-length encoding (RLE) of MTF result
        res = rle2_encode(res)
        print ("RLE2: ", res)
        
        # Huffman coding
        coded_data, huffman_lengths, table_order = huffman_encode(res)
        self.content = bitChain(''.join(coded_data))
        self.huffman_groups = len(huffman_lengths)
        print ("HUFFMAN GROUPS:", self.huffman_groups)
        print ("Content: ", self.content)
        
        # Selection between multiple Huffman tables
        self.selectors_used = bitChain(len(table_order), 15)
        print ("Selectors used:", self.selectors_used)
        
        # store this to apply the mtf+unary encoding in packaging.py
        self.table_order = table_order
        print ("Table order:", self.table_order)

        # Delta encoding (Δ) of Huffman code bit-lengths
        # self.delta_bit_length = []
        # for lengths in huffman_lengths:
        #    self.delta_bit_length += [delta_encode(lengths)]
        self.delta_bit_length = huffman_lengths
        print ("Huf length:", self.delta_bit_length)
        
        # Sparse bit array showing which symbols are used
        # res is the source before huffman
        print ("Symbols to sparse:", set(res))
        self.bit_maps = sparse(set(res))
        print ("Sparse:", self.bit_maps)

    def decompress(self):
        if self.content is None:
            raise Exception("Trying to decompress without having compressed")
        print ("\nStart decompress()")
        print ("Sparsed bit map:", self.bit_maps)
        # Sparse bit array showing which symbols are used
        symbols = unsparse(self.bit_maps)
        print ("Sym (unsparse):", symbols)
        
        # Delta encoding (Δ) of Huffman code bit-lengths
        # huffman_lengths = []
        # for deltas in self.delta_bit_length:
        #    huffman_lengths += [delta_decode(deltas)]
        huffman_lengths  = self.delta_bit_length
        print ("Huf lengths", huffman_lengths)
        
        # Unary base 1 encoding of Huffman table selection
        # Selection between multiple Huffman tables
        # Huffman coding
        res = self.content

        res = huffman_decode(res, huffman_lengths,self.table_order, symbols)
        print ("HUF dec:", res)
        # Run-length encoding (RLE) of MTF result
        res = rle2_decode(res)
        print ("RLE2 dec:", res)
        # Move to front (MTF) transform
        res = mtf_decode2(res, list(range(256)))
        print ("MTF dec:", res)
        # Burrows–Wheeler transform (BWT) or block sorting
        res = bwt_decode((res, self.bwt_column))
        print ("BWT dec", res)
        # Run-length encoding (RLE) of initial data
        res = rle_decode(res)
        print ("RLE DEC:", res)
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