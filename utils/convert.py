'''
conversion methods
'''
import struct

def intlist2bytes(l):
    bytelist = (struct.pack("B", x) for x in l)
    return b''.join(bytelist)