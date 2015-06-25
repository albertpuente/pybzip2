'''
Bytes for constructing .bz2 streams
'''
import binascii
from utils.convert import *

def crc32(data): # 4 Bytes
    if type(data) == list:
        data = intlist2bytes(data)
    elif type(data) != bytes:
        raise Exception("crc32(data) expects bytes or [int8]")
        
    return binascii.crc32(data)
    
def write_bz2(path, blocks):
    TODO = 0 # Provisional
    
    dataChain = bitChain() # What is going to be written
    streamChain = bitChain() # To compute the global CRC32
    
    # "BZ" with "h"uffman and blocks of "9"00KB (max)
    dataChain.append(b'BZh9', 32) # File signature
    
    for block in blocks:

        blockChain = bitChain()
        
        # Block start, PI
        blockChain.append(0x314159265359, 48)
        
        # CRC 32 of this block
        blockChain.append(crc32(block), 32)
        
        # Randomization (deprecated)
        blockChain.append(0, 1)
        
        # Starting pointer into BWT for after untransform
        blockChain.append(TODO, 24)
        
        # Bitmap, of ranges of 16 bytes, present/not present        
        blockChain.append(TODO, 16)
        
        # Bitmap, of symbols used, present/not present (multiples of 16)
        blockChain.append(TODO, TODO) # 0..256
        
        # 2..6 number of different Huffman tables in use
        blockChain.append(TODO, 3)
        
        # number of times that the Huffman tables are swapped (each 50 bytes)
        blockChain.append(TODO, 15)
        
        # zero-terminated bit runs (0..62) of MTF'ed Huffman table (*selectors_used)
        blockChain.append(TODO, TODO) # 1..6
        
        # 0..20 starting bit length for Huffman deltas
        blockChain.append(TODO, 5)
        
        # delta_bit_length
        blockChain.append(TODO, TODO) # 1..40
        
        # Contents
        blockChain.append(TODO, TODO) # 2bits..900KB
        streamChain.append(TODO, TODO)
        
        # Block end
        dataChain.chain += blockChain.chain
        
    # Finish mark, SQRT(PI)
    dataChain.append(0x177245385090, 48)

    # Checksum for the whole stream
    dataChain.append(crc32(streamChain.toBytes()), 32)
    
    # Padding
    if dataChain.length()%8 != 0:
        dataChain.append(0, 8 - dataChain.length()%8)
    
    # Write to file
    with open(path, 'bw+') as f: 
        f.write(dataChain.toBytes())
