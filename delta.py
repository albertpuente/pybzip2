'''
delta (differencing) encoding/decoding methods
'''

from functools import reduce

def delta_encode(msg):
    msg += [0]
    return [msg[i] - msg[i-1] for i in range(len(msg))]

def delta_decode(coding):
    return reduce(lambda msg, c: msg + [c + msg[-1]],
                  coding[1:], [coding[0]])