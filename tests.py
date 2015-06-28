'''
Performs tests over a series of encoding/decoding methods

This file doesn't test the pybzip2 algorithm by itself
'''

import random
from utils.mytimeit import timeit

def test(coder, decoder, msg=None, N = 2**10, alphabet=list(range(10))) :
    '''
    encodes and decodes a message, checking if the result coincides with the original
    :param coder: coder function
    :param decoder: decoder function
    :param msg: message to be processed, by default is randomly generated
        :param N: length of msg to be generated (if random)
        :param alphabet: list of elements used to build the message (if random)
    :return:
    '''
    if msg is None :
        # build random message if none is passed
        msg = []
        for _ in range(N) :
            msg += [alphabet[random.randint(0, len(alphabet) - 1)]]
    else :
        N = len(msg)

    print("\n" + ">"*2 + " running tests (length: " + str(N) + ") for: ", end ="")
    print(coder.__name__ + ", " + decoder.__name__)
    coded   = timeit(coder  ) (msg)
    decoded = timeit(decoder) (coded)
    # print("Compression ratio (literal):", getsizeof(coded) / getsizeof(decoded))
    if msg == decoded : print("Decode coincides with the original message")
    else :
        print("Decoding went wrong:")
        print("Original:", msg[:30])
        print("Coded   :", coded[:30])
        print("Decoded :", decoded[:30])

if __name__ == '__main__' :
    from methods.MTF import *
    test(mtf_encode, mtf_decode)

    from methods.RLE import *
    test(rle_encode, rle_decode)
    test(rle2_encode, rle2_decode, msg=[0,0,0,0,0,1,2,0,0,0,3])

    from methods.BWT import *
    test(bwt_encode, bwt_decode)

    from methods.other import *
    test(delta_encode, delta_decode)
    test(unarize, deunarize, alphabet=list(range(1,50)))

    # add more tests here