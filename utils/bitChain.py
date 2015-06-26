'''
Work with bits/bytes/hex/ints without pain
'''
from utils.convert import *

class bitChain:
    def __init__(self, inputData = [], bitLength = None):
        self.chain = []
        if inputData:
            if bitLength:
                self.append(inputData, bitLength)
            else:
                if type(inputData) != bytes:
                    raise Exception('bitChain must initialized with bytes'\
                    ' when no bitLength is specified')
                self.append(inputData, len(inputData)*8)
        
    def length(self):
        return len(self.chain)

    def append(self, data, bitLength):
        if type(data) == str:
            data = str.encode(data)
        if type(data) == bytes: 
            ints = list(data)
            for i in ints:
                bits = "{0:b}".format(i)
                bits = "0"*(8-len(bits)) + bits
                self.chain += [int(x) for x in bits]
            
        elif type(data) == int:
            new = []
            while bitLength > 0:
                if data%2: new.insert(0, 1)
                else: new.insert(0, 0)
                bitLength -= 1
                data >>= 1
            self.chain += new
        else:
            raise Exception("bitChain.append expects int or bytes type")
        

    def toBytes(self):
        #if len(self.chain)%8 != 0:
            #print ("Warning: bitChain is not complete (byte whole)")
            
        B = b""
        ints = []
        for i in range (0, len(self.chain), 8):
            bitString = ''.join([str(b) for b in self.chain[i:i+8]])
            ints += [int(bitString, 2)]
        return bytes(ints)
        
    def bits(self):
        return self.chain
        
    def toHex(self):
        data = self.toBytes()
        return binascii.hexlify(bytearray(data))
    
    def toInt(self):
        data = self.toBytes()
        return int.from_bytes(data, byteorder = 'big')
        
    def get(self, start, end):
        if start < 0 or end >= self.length() or start > end:
            raise Exception('bitChain.get with wrong parameters')
        new = bitChain()
        new.chain = self.chain[start:end+1]
        return new
        
    def __str__(self):
        s = str(''.join([str(b) for b in self.chain]))
        return s