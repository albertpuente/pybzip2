'''
Work with bits/bytes/hex/ints without pain
'''
from utils.convert import *

class bitChain:
    def __init__(self):
        self.chain = []
        
    def length(self):
        return len(self.chain)

    def append(self, data, bitLength):
        T = type(data)
        if T == bytes: 
            data = int.from_bytes(data, byteorder = 'little')
        elif T == str:
            data = str.encode(data)
        elif T != int:
            raise Exception("bitChain.append expects int or bytes type")
            
        new = []
        while bitLength > 0:
            if data%2: new.insert(0, 1)
            else: new.insert(0, 0)
            bitLength -= 1
            data >>= 1
        self.chain += new

    def toBytes(self):
        if len(self.chain)%8 != 0:
            print ("bitChain is not complete (byte whole)")
            
        B = b""
        ints = []
        for i in range (0, len(self.chain), 8):
            bitString = ''.join([str(b) for b in self.chain[i:i+8]])
            ints += [int(bitString, 2)]
        return bytes(ints)
        
    def bits(self):
        return self.chain
        
    def __str__(self):
        s = str(''.join([str(b) for b in self.chain]))
        return s