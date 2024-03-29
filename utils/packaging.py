'''
Functions for constructing .bz2 streams
'''
import binascii
from utils.bitChain import *
from utils.convert import *
from pybzip2 import *

'''
Returns the CRC32 (4 Bytes) of a sequence of bytes
'''
def crc32(data):
    if type(data) == list:
        data = intlist2bytes(data)
    elif type(data) != bytes:
        raise Exception("crc32(data) expects bytes or [int8]")
        
    return binascii.crc32(data)
    
'''
Writes a .bz2 file using bzipBlocks (class pybzip2compressor)
'''
def write_bz2(path, bzipBlocks):

    dataChain = bitChain() # What is going to be written
    streamChain = bitChain() # To compute the global CRC32
    
    # "BZ" with "h"uffman and blocks of "9"00KB (max)
    dataChain.append(b'BZh9', 32) # File signature
    
    for bzipBlock in bzipBlocks:

        blockChain = bitChain()
        
        # Block start, PI
        blockChain.append(0x314159265359, 48)
        
        # CRC 32 of this block
        blockChain.append(crc32(bzipBlock.content.toBytes()), 32)
        
        # Randomization (deprecated)
        blockChain.append(0, 1)
        
        # Starting pointer into BWT for after untransform
        blockChain.append(bzipBlock.bwt_column, 24)
        
        # Bitmaps, of ranges of 16 bytes, present/not present + 
        # Bitmap, of symbols used, present/not present (multiples of 16)
        blockChain.append(bzipBlock.bit_maps)

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
        # start by adding 1 to the indices for the unary encoding to work
        table_order = bzipBlock.table_order
        # table_order = [t + 1 for t in table_order]
        # apply mtf
        mtf_tables_used, _ = mtf_encode(table_order)

        unarized = unarize(mtf_tables_used)
        blockChain.append(unarized) # 1..6*selectors_used
        
        # delta_bit_length
        deltas_blocks = bzipBlock.delta_bit_length
        for deltas in deltas_blocks:
            # 0..20 starting bit length for Huffman deltas
            blockChain.append(deltas[0], 5)
            lastLength = deltas[0]
            i = 1
            # Deltas
            while i < len(deltas):
                if deltas[i] == lastLength: # Next symbol
                    blockChain.append('0')
                    i += 1
                else:
                    if deltas[i] > lastLength:
                        blockChain.append('10')
                        lastLength += 1
                    else: # lengths[i] < lastNum:
                        blockChain.append('11')
                        lastLength -= 1
            blockChain.append('0')
        
        # Contents
        blockChain.append(bzipBlock.content) # 2bits..900KB
        streamChain.append(bzipBlock.content)
        
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
    
'''
Writes a decompressed file using bzipBlocks (class pybzip2compressor)
'''
def write_file(path, bzipBlocks):
    # Write to file
    file = open(path, 'wb+')
    for block in bzipBlocks:
        file.write(intlist2bytes(block.decompressed))
    file.close()
    
'''
Finds the start positions of a sequence of bits that appear in a larger sequence
'''
def find_start(sub, big):
    R = []
    for i in range(0, len(big) - len(sub) + 1):
        if big[i:i+len(sub)] == sub:
            R.append(i)
    return R

'''
Reads a file and creates a list of bzipBlocks (class pybzip2compressor)
Depending on the file that is read, the bzipBlocks will contain compressed or
raw data
'''
def read_bz2(path):
    bzipBlocks = []
    file = open(path, 'rb')
    inputData = file.read()
    rawBytes = inputData
    file.close()
    
    dataChain = bitChain(rawBytes) # To parse the file
    streamChain = bitChain() # To compute the global CRC
    
    if inputData == dataChain.toBytes():
        print ('File converted to bitChain correctly.')
    else:
        raise Exception('bitChain class is not working!')
    
    # File signature
    signature = dataChain.get(0, 24).toBytes()
    if signature != b'BZh': # bzipBlocks will be used to compress data
        print('Unknown signature: raw file mode')
        
        NB = 900000 # Blocks of 900KB (maximum)
        rawIntBytes = list(rawBytes)
        blocks = [rawIntBytes[i:i+NB] for i in range(0, len(rawIntBytes), NB)]
        
        bzipBlocks = [pybzip2compressor(block) for block in blocks]
        
        return ('raw', bzipBlocks) # Notice this return!
        
    else: # bzipBlocks will be used to decompress data
        print ('File signature recognised:', signature)
        
    blockSize = dataChain.get(24,32).toBytes()
    print ("Block size:", int(blockSize)*100000,"uncompressed Bytes")
        
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
        
        print ("BLOCK start at position", start)
        print ("    PI:", 
            dataChain.get(start, start + 48).toHex())
        
        start += 48
        blockCRC = dataChain.get(start, start + 32).toInt()
        print ("    Block CRC", blockCRC)
            
        start += 32
        print ("    Randomized:",
            dataChain.get(start, start+1))
            
        start += 1
        bzipBlock.bwt_column = dataChain.get(start, start+24).toInt()
        print ("    BWT Start pointer:",bzipBlock.bwt_column)
        
        start += 24
        bzipBlock.bit_maps = dataChain.get(start, start+16)
        print ("    Used bitmaps:", bzipBlock.bit_maps)
        start += 16
        N = sum(bzipBlock.bit_maps.bits())
        huffman_used_bitmaps = dataChain.get(start, start+16*N) 
        for i in range(0, N):
            print ("        Bitmap:", huffman_used_bitmaps.get(i*16, (i+1)*16))
        bzipBlock.bit_maps.append(huffman_used_bitmaps)
        
        
        start += 16*N
        bzipBlock.huffman_groups = dataChain.get(start, start + 3).toInt()
        print ("    Huffman groups:", bzipBlock.huffman_groups)
            
        start += 3
        bzipBlock.selectors_used = dataChain.get(start, start + 15).toInt()
        print ("    Selectors used:", bzipBlock.selectors_used)
            
        start += 15

        # Selector list
        selector_list = [0]
        i = 0
        while i < bzipBlock.selectors_used:
            if dataChain.get(start, start+1).toInt() == 1:
                selector_list[-1] += 1
                if i + 1 == bzipBlock.selectors_used and selector_list[-1] == 5:
                    i += 1
            else:
                selector_list += [0]
                i += 1
            start += 1
        # undo the mtf, pass the list of possible values (we have up to 6 huffman tables)
        print ("    Undoing the mtf...")
        selector_list = mtf_decode2(selector_list, list(range(6)))
        bzipBlock.table_order = selector_list
        print ("    Done.")
        
        print ("    Reading deltas...")
        # Delta bit lengths for each huffman table
        bzipBlock.delta_bit_length = []
        start -= 1
        for _ in range(bzipBlock.huffman_groups):
            deltas = [] # Deltas for this table
            firstLength = dataChain.get(start, start + 5).toInt()
            deltas.append(firstLength) # First length
            start += 5
            
            lastNum = firstLength
            for i in range (257): # 258 - 1 deltas following the first
                while dataChain[start] == 1:
                    start += 1
                    if dataChain[start] == 0:
                        lastNum += 1
                    else: 
                        lastNum -= 1
                    start += 1
                start += 1
                deltas.append(lastNum) # Next delta (difference with the previous number)
            bzipBlock.delta_bit_length.append(deltas)
        print ("    Done.")
        # Compressed block
        if iBlock == len(blocks) - 1:
            end = blocks_end[0]
        else:
            end = blocks[iBlock + 1]
        
        bzipBlock.content = dataChain.get(start, end)
        streamChain.append(bzipBlock.content)
        
        if (crc32(bzipBlock.content.toBytes()) == blockCRC):
            print ("    Block CRC32 is correct.")
        else:
            print ("    Block CRC32 is not correct!")
        # Block end, append to the list
        bzipBlocks.append(bzipBlock)
    
    # Global CRC_32
    CRC_position = blocks_end[0] + 48
    globalCRC = dataChain.get(CRC_position, CRC_position+32).toInt()
    print ('    Global CRC is:', globalCRC)
    
    if (crc32(streamChain.toBytes()) == globalCRC):
        print ("    Global CRC32 is correct.")
    else:
        print ("    Global CRC32 is not correct!")
    
    # Padding
    if (CRC_position + 32)%8 != 0:
        print ('Padding detected:', 
            dataChain.get(CRC_position+32, len(dataChain)))
            
    return ('bz2', bzipBlocks)