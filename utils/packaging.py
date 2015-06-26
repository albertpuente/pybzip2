'''
Bytes for constructing .bz2 streams
'''
import binascii
from utils.bitChain import *
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
    file = open(path, 'wb+')
    file.write(dataChain.toBytes())
    file.close()
    
def find_start(sl,l):
    results = []
    sll = len(sl)
    for ind in (i for i,e in enumerate(l) if e == sl[0]):
        if l[ind:ind+sll] == sl:
            results.append(ind)
    return results

def read_bz2(path):
    file = open(path, 'rb')
    inputData = file.read()
    
    dataChain = bitChain(inputData)

    file.close()
    if inputData == dataChain.toBytes():
        print ('File converted to bitChain correctly.')
    else:
        raise Exception('bitChain class is not working!')
    
    # File signature
    signature = dataChain.get(0, 23).toBytes()
    if signature != b'BZh':
        raise Exception('Wrong file signature:', signature)
    else:
        print ('File signature recognised:', signature)
        
    blockSize = dataChain.get(24,31).toBytes()
    print ("Block size:", blockSize)
        
    # Search blocks starts
    pi = bitChain(0x314159265359, 48)
    blocks = find_start(pi.bits(), dataChain.bits())
    print ('Blocks begin at positions:', blocks)
    
    # Search blocks end
    sqrt_pi = bitChain(0x177245385090, 48)
    blocks_end = find_start(sqrt_pi.bits(), dataChain.bits())
    print ('Blocks end at position:', blocks_end)
    
    # For each block
    for start in blocks:
        print ("BLOCK at position", start)
        print ("    PI:", 
            dataChain.get(start, start + 47).toHex())
        
        start += 48
        print ("    Block CRC",
            dataChain.get(start, start + 31).toInt())
            
        start += 32
        print ("    Randomized:",
            dataChain.get(start, start))
            
        start += 1
        print ("    BWT Start pointer:",
            dataChain.get(start, start+23).toInt())
            
        start += 24
        print ("    Huffman used map:",
            dataChain.get(start, start+15))
            
        nBitMaps = sum(dataChain.get(start, start+15).bits())
        print ("    nBitMaps:", nBitMaps)
        
        start += 16
        for i in range (0, nBitMaps):
            print ("    Bitmap",i,":",
                dataChain.get(start, start+15))
            start += 16
            
        print ("    Huffman groups:",
            dataChain.get(start, start + 2).toInt())
            
        start += 3
        selectors_used = dataChain.get(start, start + 15).toInt()
        print ("    Selectors used:",
            selectors_used)
            
        start += 16
        
        print ("    No idea ...")
        
    
    # Global CRC_32
    CRC_position = blocks_end[0] + 48
    globalCRC = dataChain.get(CRC_position, CRC_position+31)
    print ('Global CRC is:', globalCRC.toInt())
    
    # Padding
    if (CRC_position + 31)%8 != 0:
        print ('Padding detected:', 
            dataChain.get(CRC_position+32, dataChain.length()-1))
    
# TEST
read_bz2('./input/subs.srt.bz2')
