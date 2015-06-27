'''
Bytes for constructing .bz2 streams
'''
import binascii
from utils.bitChain import *
from utils.convert import *
from pybzip2 import *

def crc32(data): # 4 Bytes
    if type(data) == list:
        data = intlist2bytes(data)
    elif type(data) != bytes:
        raise Exception("crc32(data) expects bytes or [int8]")
        
    return binascii.crc32(data)
    
def write_bz2(path, bzipBlocks):
    TODO = 0 # Provisional
    
    dataChain = bitChain() # What is going to be written
    streamChain = bitChain() # To compute the global CRC32
    
    # "BZ" with "h"uffman and blocks of "9"00KB (max)
    dataChain.append(b'BZh9', 32) # File signature
    
    for bzipBlock in bzipBlocks:

        blockChain = bitChain()
        
        # Block start, PI
        blockChain.append(0x314159265359, 48)
        
        # CRC 32 of this block
        blockChain.append(crc32(bzipBlock.compressed), 32)
        
        # Randomization (deprecated)
        blockChain.append(0, 1)
        
        # Starting pointer into BWT for after untransform
        blockChain.append(bzipBlock.bwt_start_pointer, 24)
        
        # Bitmaps, of ranges of 16 bytes, present/not present + 
        # Bitmap, of symbols used, present/not present (multiples of 16)
        blockChain.append(bzipBlock.bitmaps)

        # 2..6 number of different Huffman tables in use
        blockChain.append(bzipBlock.huffman_groups, 3)
        
        '''
        number of times that the Huffman tables are swapped (each 50 bytes)
        
        Every 50B table swap
        900*2**10 / 50 = 18432 changes
        Requires 14.17 bits to be codified
        '''
        blockChain.append(bzipBlock.selectors_used, 15)
        
        # zero-terminated bit runs (0..62) of MTF'ed Huffman table (*selectors_used)
        # blockChain.append(TODO, TODO) # 1..6
        
        # 0..20 starting bit length for Huffman deltas
        blockChain.append(bzipBlock.delta_bit_length[0], 5)
        
        # delta_bit_length
        lengths = bzipBlock.delta_bit_length
        lastNum = lengths[0]
        i = 1
        while i < len(lengths):
            if lengths[i] == lastNum: # Next symbol
                blockChain.append('0')
                lastNum = lengths[i]
                i += 1
            elif lengths[i] > lastNum:
                blockChain.append('0') 
                lengths[i] -= 1
            else: # lengths[i] < lastNum:
                blockChain.append('1') 
                lengths[i] += 1
        
        # Contents
        blockChain.append(bzipBlock.compressed) # 2bits..900KB
        streamChain.append(bzipBlock.compressed)
        
        # Block end
        dataChain.chain += blockChain.chain
        
    # Finish mark, SQRT(PI)
    dataChain.append(0x177245385090, 48)

    # Checksum for the whole stream
    dataChain.append(crc32(streamChain.toBytes()), 32)
    
    # Padding
    if len(dataChain)%8 != 0:
        dataChain.append(0, 8 - len(dataChain)%8)
    
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
    bzipBlocks = []
    file = open(path, 'rb')
    inputData = file.read()
    rawBytes = inputData
    file.close()
    
    dataChain = bitChain(rawBytes)
    
    
    if inputData == dataChain.toBytes():
        print ('File converted to bitChain correctly.')
    else:
        raise Exception('bitChain class is not working!')
    
    # File signature
    signature = dataChain.get(0, 24).toBytes()
    if signature != b'BZh':
        print('Unknown signature: raw file mode')
        
        NB = 900000 # Blocks of 900KB (maximum)
        rawIntBytes = list(rawBytes)
        blocks = [rawIntBytes[i:i+NB] for i in range(0, len(rawIntBytes), NB)]
        
        bzipBlocks = [pybzip2compressor(block) for block in blocks]
        
        return ('raw', bzipBlocks)
        
    else:
        print ('File signature recognised:', signature)
        
    blockSize = dataChain.get(24,32).toBytes()
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
    for iBlock in range(0, len(blocks)):
        start = blocks[iBlock]
        
        bzipBlock = pybzip2compressor()
        
        print ("BLOCK at position", start)
        print ("    PI:", 
            dataChain.get(start, start + 48).toHex())
        
        start += 48
        print ("    Block CRC",
            dataChain.get(start, start + 32).toInt())
            
        start += 32
        print ("    Randomized:",
            dataChain.get(start, start+1))
            
        start += 1
        bzipBlock.bwt_start_pointer = dataChain.get(start, start+24).toInt()
        print ("    BWT Start pointer:",bzipBlock.bwt_start_pointer)
        
        start += 24
        bzipBlock.bit_maps = dataChain.get(start, start+16)

        start += 16
        N = sum(bzipBlock.bit_maps.bits())
        huffman_used_bitmaps = dataChain.get(start, start+16*N) 
        bzipBlock.bit_maps.append(huffman_used_bitmaps)
        print ("    Huffman used map (sparse):", bzipBlock.bit_maps)
        nSymbols = sum(huffman_used_bitmaps.bits())
        print ("    N symbols: ", nSymbols)
        
        start += 16*N
        bzipBlock.huffman_groups = dataChain.get(start, start + 3).toInt()
        print ("    Huffman groups:", bzipBlock.huffman_groups)
            
        start += 4
        bzipBlock.selectors_used = dataChain.get(start, start + 15).toInt()
        print ("    Selectors used:", bzipBlock.selectors_used)
            
        start += 15
        
        # Selector_list?
        print ("    No idea ...")
        # start += 1..6
        start += 1 # Patillada
        
        # delta_bit_length
        bzipBlock.delta_bit_length = []
        
        firstLength = dataChain.get(start, start + 6).toInt()
        bzipBlock.delta_bit_length.append(firstLength)
        start += 6
        
        lastNum = firstLength
        for i in range (1, nSymbols):
            while dataChain[start] == 1:
                start += 1
                if dataChain[start] == 0:
                    lastNum += 1
                else: 
                    lastNum -= 1
            start += 1
            bzipBlock.delta_bit_length.append(lastNum)
        print ("    List of lengths: ",bzipBlock.delta_bit_length)
            

        # TO-DO
        
        # Compressed block
        if iBlock == len(blocks) - 1:
            end = blocks_end[0]
        else:
            end = blocks[iBlock + 1]
        
        bzipBlock.compressed = dataChain.get(start, end)
        
        # Block end, append to the list
        bzipBlocks.append(bzipBlock)
    
    # Global CRC_32
    CRC_position = blocks_end[0] + 48
    globalCRC = dataChain.get(CRC_position, CRC_position+32)
    print ('Global CRC is:', globalCRC.toInt())
    
    # Padding
    if (CRC_position + 31)%8 != 0:
        print ('Padding detected:', 
            dataChain.get(CRC_position+32, len(dataChain)))
            
    return ('bz2', bzipBlocks)
    
# TEST
read_bz2('./input/Test.txt.bz2')
