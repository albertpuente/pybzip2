'''
Burrows-Wheeler Transform encoding/decoding methods
'''

def bwt_encode(msg) :
    all_rots = []
    for _ in range(len(msg)) :
        all_rots += [msg]
        msg = msg[1:] + msg[:1]
    all_rots.sort()

    return [row[-1] for row in all_rots], all_rots.index(msg)

def bwt_decode(coding) :
    coded = coding[0]
    index = coding[1]
    permutation = sorted((t, i) for i, t in enumerate(coded))
    msg = []
    for _ in coded :
        c, index = permutation[index]
        msg += [c]
    return msg