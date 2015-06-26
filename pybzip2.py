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
from utils.bitChain import bitChain

def unarize(lengths):
    '''
    transforms a list of lengths into its unary codification
    ex: [1,2,3] -> 10110111
    returns a bitChain
    '''
    return bitChain('0'.join(x*'1' for x in lengths))


def deunarize(bc):
    from itertools import groupby
    # transform bit chain to list of 1s and 0s
    bits = (bc[i] for i in range(len(bc)))
    # group by 1s, output the length of the group
    return [len(list(k)) for x,k in groupby(bits) if x == 1]

print(deunarize(unarize([1,2,3])))

def sparse(source):
    '''
    returns a sparse array given a source of bytes.
    if a byte value (0..255) appears in the source, the array holds a 1 in its [value] position, 0 otherwise
    the array is divided in blocks of 16 to avoid long sequences of 0s, and blocks of 16 0s are ommitted
    '''
    bytes_in_source = [''.join('1' if x in source else '0' for x in range(i*16, i*16+16)) for i in range(16)]
    all0 = lambda x : all(b=='0' for b in x)
    return bitChain(''.join('0' if all0(block) else '1' for block in bytes_in_source) + # front header
                    ''.join(block for block in bytes_in_source if not all0(block)))     # values
    # front = ''
    # used = ''
    # for i in range(16):
    #     all0 = True
    #     for j in range(i*16, i*16 + 16):
    #         if j in source:
    #             used += '1'
    #             all0 = False
    #         else : used += '0'
    #     if all0:
    #         front += '0'
    #         used = used[:-16]
    #     else :
    #         front += '1'
    # return bitChain(front+used)

def unsparse(bc):
    values = []
    non0blocks = 0
    for i in range(16):
        if bc[i] == 1: # block contains some non0 value
            for j in range(16):
                if bc[16 + non0blocks*16 + j] == 1:
                    values += [i*16 + j]
    return values

print(unsparse(sparse(range(20,30))))

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
        res = rle2_encode(res)
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
        res = rle2_decode(res)
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