'''
Performs tests over a series of encoding/decoding methods
'''

import random
from utils.mytimeit import timeit

def test(coder, decoder, msg=None, N = 2**10, alphabet=list("abcdefghijklmnopqrstuvwxyz")) :
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

    from methods.BWT import *
    test(bwt_encode, bwt_decode)

    from methods.delta import *
    test(delta_encode, delta_decode, alphabet=list(range(10)))