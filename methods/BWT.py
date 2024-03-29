'''
Burrows-Wheeler Transform encoding/decoding methods

encoding params (reverse for decoding)
input: list
output: list, bwt_column
'''

def bwt_encode(msg) :
    all_rots = []
    for _ in range(len(msg)) :
        all_rots += [msg]
        msg = msg[1:] + msg[:1]
    all_rots.sort()

    return [row[-1] for row in all_rots], all_rots.index(msg) + 1

def bwt_encode2(text):
    import sys
    sys.setrecursionlimit(20000)
    def radix_sort(values, key, step=0):
        # print(step)
        if len(values) < 2:
            for value in values:
                yield value
            return

        bins = {}
        for value in values:
            bins.setdefault(key(value, step), []).append(value)

        for k in sorted(bins.keys()):
            for r in radix_sort(bins[k], key, step + 1):
                yield r

    def bw_key(text, value, step):
        return text[(value + step) % len(text)]

    from functools import partial
    asd = list(radix_sort(range(len(text)), partial(bw_key, text)))
    return [text[i - 1] for i in asd], asd.index(0) + 1

def bwt_encode3(text):
    N = len(text)
    text2 = text * 2
    class K:
        def __init__(self, i):
            self.i = i
        def __lt__(a, b):
            i, j = a.i, b.i
            for k in range(N): # use `range()` in Python 3
                if text2[i+k] < text2[j+k]:
                    return True
                elif text2[i+k] > text2[j+k]:
                    return False
            return False # they're equal

    inorder = sorted(range(N), key=K)
    return [text2[i+N-1] for i in inorder], inorder.index(0) + 1

def bwt_decode(coding) :
    coded = coding[0]
    index = coding[1] - 1
    permutation = sorted((t, i) for i, t in enumerate(coded))
    msg = []
    for _ in coded :
        c, index = permutation[index]
        msg += [c]
    return msg