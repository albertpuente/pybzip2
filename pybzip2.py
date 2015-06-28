'''
bzip2 python implementation

CDI-FIB
Joan Ginés, Albert Puente, Andrés Mingorance
'''

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
        # Run-length encoding (RLE) of initial data
        res = rle_encode(self.msg)

        # Burrows–Wheeler transform (BWT) or block sorting
        res, bwt_column = bwt_encode2(res)
        self.bwt_column = bwt_column
        symbols = list(set(res))
        # Move to front (MTF) transform
        res, _ = mtf_encode(res)

        # Run-length encoding (RLE) of MTF result
        res = rle2_encode(res)
        print ("RLE2: ", res)
        
        # Huffman coding
        coded_data, huffman_lengths, table_order = huffman_encode(res)
        self.content = bitChain(''.join(coded_data))
        self.huffman_groups = len(huffman_lengths)

        # Selection between multiple Huffman tables
        self.selectors_used = len(table_order)

        # store this to apply the mtf+unary encoding in packaging.py
        self.table_order = table_order

        # Delta encoding (Δ) of Huffman code bit-lengths
        # self.delta_bit_length = []
        # for lengths in huffman_lengths:
        #    self.delta_bit_length += [delta_encode(lengths)]
        self.delta_bit_length = huffman_lengths

        # Sparse bit array showing which symbols are used in our source
        self.bit_maps = sparse(symbols)

    def decompress(self):
        if self.content is None:
            raise Exception("Trying to decompress without having compressed")
        # Sparse bit array showing which symbols are used
        symbols = unsparse(self.bit_maps)
        
        # remove the 0s
        huffman_symbols = list(range(1,258))

        huffman_lengths  = self.delta_bit_length

        # Huffman coding
        res = self.content
        res = huffman_decode(res, huffman_lengths,self.table_order, huffman_symbols)
        # Run-length encoding (RLE) of MTF result
        res = rle2_decode(res)
        # Move to front (MTF) transform
        res = mtf_decode2(res, symbols)
        # Burrows–Wheeler transform (BWT) or block sorting
        res = bwt_decode((res, self.bwt_column))
        # Run-length encoding (RLE) of initial data
        res = rle_decode(res)
        self.decompressed = res