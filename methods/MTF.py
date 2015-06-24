'''
Move To Front transform encoding/decoding methods
'''

def mtf_encode(msg) :
    recent = list(set(msg))
    recent.sort()

    coded = []
    for c in msg :
        idx = recent.index(c)
        coded += [idx]
        # update recently used
        recent.pop(idx)
        recent.insert(0, c)

    return coded, recent

def mtf_decode(coding) :
    coded  = coding[0][::-1]
    recent = coding[1]

    msg = []
    for idx in coded :
        c = recent[0]
        msg += [c]
        # reverse-update recently used
        recent.pop(0)
        recent.insert(idx, c)
    return msg[::-1]