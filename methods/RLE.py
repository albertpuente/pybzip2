'''
Run Length Encoding encoding/decoding methods

encoding params (reverse for decoding)
input: list
output: list
'''

'''
rle_X implement the classic run length encoding, changing runs of N+M times the same char into
N times the same char + a byte coding M

rle2_X implement runa/runb coding, transform long chains of 0s to a bijective base-2 representation
of the run length. They're supposed to be used after MTF transform
'''

class rle_values:
    N = 4
    runa = 256
    runb = runa + 1

def rle_encode(msg) :
    if len(msg) == 0: return msg
    
    N = rle_values.N
    coded = [msg[0]]
    count = 1
    for i in range(1, len(msg)):
        if msg[i] == msg[i-1] :
            count += 1
            if count >= 255 - N :
                coded.append(count - N)
                count = 0
            if count <= N:
                coded.append(msg[i])
        else :
            if count >= N:
                coded.append(count - N)
            coded.append(msg[i])
            count = 1
    if count > N :
        coded.append(count - N)
    return coded

def rle_decode(coding) :
    if len(coding) == 0 : return coding
    
    N = rle_values.N
    msg = [coding[0]]
    count = 1
    for i in range(1, len(coding)):
        if count == N :
            msg += [msg[-1]] * coding[i]
            count = 0
        else :
            msg.append(coding[i])
            if coding[i] == coding[i-1]:
                count += 1
            else :
                count = 1
    return msg

def bb2code(n):
    '''
    transforms an arbitrarily big integer into its
    bijective base 2 codification, using runa, runb as symbols
    '''
    def bij(l, t=0):
        if t == n:
            return l
        elif t > n:
            return None
        else:
            la = lb = l
            r = bij(l + [rle_values.runa], t + 2**len(l))
            if r is not None : return r
            r = bij(l + [rle_values.runb], t + 2*2**len(l))
            return r # it exists, no need to check now
    return bij([], 0)

def bb2decode(runab):
    '''
    transforms a runa,runb bijective base 2 codification
    into the integer it represents
    '''
    n = 0
    for i in range(len(runab)):
        if runab[i] == rle_values.runa:
            n += 2**i
        else:
            n += 2**i * 2
    return n

def rle2_encode(msg):
    '''
    transforms runs of '0's to a bijective base-2 representation
    of the run length. e.g: 0,0,0,0,0,1,3,1,0,0 -> runa,runb,1,3,1,runb
    '''
    count = 0
    coded = []
    for x in msg:
        if x == 0 :
            if count < 900*2**10: # < blocksize, 900k
                count += 1
            else :
                coded += bb2code(count)
                count = 1
        else :
            if count > 0 :
                coded += bb2code(count)
                count = 0
            coded += [x]
    return coded

def rle2_decode(coded):
    '''
    transforms run-length encodings into chains of zeroes.
    '''
    msg = []
    runab = []
    for c in coded:
        if c == rle_values.runa or c == rle_values.runb:
            runab += [c]
        else:
            msg += [0]*bb2decode(runab)
            msg += [c]
            runab = []
    return msg
