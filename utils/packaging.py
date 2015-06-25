'''
Bytes for constructing .bz2 streams
'''
import binascii
import utils.convert

'''
.magic:16                       = 'BZ' signature/magic number
.version:8                      = 'h' for Bzip2 ('H'uffman coding)
.hundred_k_blocksize:8          = '1'..'9' block-size 100 kB-900 kB (uncompressed)

    BLOCK START

.compressed_magic:48            = 0x314159265359 (BCD (pi))
.crc:32                         = checksum for this block
.randomised:1                   = 0=>normal, 1=>randomised (deprecated)
.origPtr:24                     = starting pointer into BWT for after untransform
.huffman_used_map:16            = bitmap, of ranges of 16 bytes, present/not present
.huffman_used_bitmaps:0..256    = bitmap, of symbols used, present/not present (multiples of 16)
.huffman_groups:3               = 2..6 number of different Huffman tables in use
.selectors_used:15              = number of times that the Huffman tables are swapped (each 50 bytes)
*.selector_list:1..6            = zero-terminated bit runs (0..62) of MTF'ed Huffman table (*selectors_used)
.start_huffman_length:5         = 0..20 starting bit length for Huffman deltas
*.delta_bit_length:1..40        = 0=>next symbol; 1=>alter length
                                                { 1=>decrement length;  0=>increment length } (*(symbols+2)*groups)
.contents:2..∞                  = Huffman encoded data stream until end of block (max. 7372800 bit)

    BLOCK END

.eos_magic:48                   = 0x177245385090 (BCD sqrt(pi))
.crc:32                         = checksum for whole stream
.padding:0..7                   = align to whole byte
'''

def file_signature(): # 4 Bytes
    # BZ with huffman and blocks of 900KB (max)
    return b'BZh9'

def block_start(): # 6 Bytes
    return bytearray.fromhex('314159265359') # pi

def block_end(): # 6 Bytes
    return bytearray.fromhex('177245385090') # sqrt(pi)

def block_crc32(data): # 4 Bytes
    if type(data) == list:
        data = intlist2bytes(data)
    crc = binascii.crc32(data) 
    return bytearray.fromhex(format(crc, 'x'))
    