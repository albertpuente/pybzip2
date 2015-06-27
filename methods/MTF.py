'''
Move To Front transform encoding/decoding methods
encoding params (reverse for decoding)
input: list
output: list, mtf_stack
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

def mtf_decode2(coding, symbols):
    res = []
    for i in range(len(coding)):
        idx = coding[i]
        res += [symbols[idx]]
        symbols.pop(idx)
        symbols.insert(0, res[-1])
    return res