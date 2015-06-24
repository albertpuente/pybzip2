'''
Run Length Encoding encoding/decoding methods

encoding params (reverse for decoding)
input: list
output: list
'''

from functools import reduce

def rle_encode(msg) :
    if len(msg) == 0: return msg

    coded = []
    counter = 1
    last = msg[0]
    for c in msg[1:] :
        if c == last : counter += 1
        else :
            coded += [(counter, last)]
            last = c
            counter = 1
    coded += [(counter, last)]
    return coded

def rle_decode(coding) :
    return reduce(lambda msg, cf : msg + cf[0]*[cf[1]], coding, [])
