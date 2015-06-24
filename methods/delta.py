'''
delta (differencing) encoding/decoding methods
'''

from functools import reduce

def delta_encode(msg):
    msgz = msg + [0]    # so msgz[-1] == 0
    return [msgz[i] - msgz[i-1] for i in range(len(msg))]

def delta_decode(coding):
    return reduce(lambda msg, c: msg + [c + msg[-1]],
                  coding[1:], [coding[0]])