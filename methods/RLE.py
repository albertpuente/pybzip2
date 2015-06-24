'''
Run Length Encoding encoding/decoding methods

encoding params (reverse for decoding)
input: list
output: list
'''

def rle_encode(msg) :
    if len(msg) == 0: return msg

    coded = [msg[0]]
    count = 1
    for i in range(1, len(msg)):
        if msg[i] == msg[i-1] :
            count += 1
            if count > 251 :
                coded.append(count - 4)
                count = 0
        else :
            count = 0
        if count <= 4 :
            coded.append(msg[i])
    if count > 4 :
        coded.append(count - 4)
    return coded

def rle_decode(coding) :
    if len(coding) < 3 : return coding
    msg = [coding[0]]
    count = 1
    for i in range(1, len(coding)):
        if count == 4 :
            msg.append(msg[-1]*coding[i])
            count = 0
        else :
            msg.append(coding[i])
            if coding[i] == coding[i-1]:
                count += 1
            else :
                count = 0
    return msg
