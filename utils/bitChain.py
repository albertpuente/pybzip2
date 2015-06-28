'''
Work with bits/bytes/hex/ints without pain
'''
import binascii
from utils.convert import *

class bitChain:
    def __init__(self, inputData = [], bitLength = None):
        self.chain = []
        if inputData:
            self.append(inputData, bitLength)
        
    def append(self, data, bitLength = None):
        if type(data) == str:
            for x in data:
                if x != '0' and x != '1':
                    raise Exception('bitChain.append: string must be binary')
                self.chain.append(int(x))
        elif type(data) == bytes: 
            ints = list(data)
            for i in ints:
                bits = "{0:b}".format(i)
                bits = "0"*(8-len(bits)) + bits
                self.chain += [int(x) for x in bits]
            
        elif type(data) == int:
            if not bitLength:
                raise Exception("bitChain.append: int requires bitLength")
            binaryLength = '{0:0'+str(bitLength)+'b}'
            self.chain += list(binaryLength.format(data))
        elif type(data) == bitChain:
            self.chain += data.bits()
        elif type(data) == list:
            self.append(intlist2bytes(data))
        else:
            raise Exception("bitChain.append type:",type(data),'not supported')
        

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
        return int(str(self), 2)
        
    def get(self, start, end):
        if start < 0 or end > len(self) or start >= end:
            raise Exception('bitChain.get with wrong parameters')
        new = bitChain()
        new.chain = self.chain[start:end]
        return new
        
    # [] operator
    def __getitem__(self, index):
        return self.chain[index]
        
    def __str__(self):
        s = str(''.join([str(b) for b in self.chain]))
        return s
        
    def __len__(self):
        return len(self.chain)
