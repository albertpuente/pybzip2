'''
delta (differencing) encoding/decoding methods
'''
from utils.bitChain import bitChain
from functools import reduce

def delta_encode(msg):
    msgz = msg + [0]    # so msgz[-1] == 0
    return [msgz[i] - msgz[i-1] for i in range(len(msg))]

def delta_decode(coding):
    return reduce(lambda msg, c: msg + [c + msg[-1]],
                  coding[1:], [coding[0]])


def unarize(lengths):
    '''
    transforms a list of lengths into its unary codification
    ex: [1,2,3] -> 10110111
    returns a bitChain
    '''
    if any(map(lambda x: x < 0, lengths)) :
        raise Exception("Negative length found, please use positive numbers")
    return bitChain('0'.join(x*'1' for x in lengths))


def deunarize(bc):
    from itertools import groupby
    # transform bit chain to list of 1s and 0s
    bits = (bc[i] for i in range(len(bc)))
    # group by 1s, output the length of the group
    return [len(list(k)) for x,k in groupby(bits) if x == 1]

def sparse(source):
    '''
    returns a sparse array given a source of bytes.
    if a byte value (0..255) appears in the source, the array holds a 1 in its [value] position, 0 otherwise
    the array is divided in blocks of 16 to avoid long sequences of 0s, and blocks of 16 0s are ommitted
    '''
    bytes_in_source = [''.join('1' if x in source else '0' for x in range(i*16, i*16+16)) for i in range(16)]
    all0 = lambda x : all(b=='0' for b in x)
    return bitChain(''.join('0' if all0(block) else '1' for block in bytes_in_source) + # front header
                    ''.join(block for block in bytes_in_source if not all0(block)))     # values

def unsparse(bc):
    values = []
    non0blocks = 0
    for i in range(16):
        if bc[i] == 1: # block contains some non0 value
            for j in range(16):
                if bc[16 + non0blocks*16 + j] == 1:
                    values += [i*16 + j]
    return values