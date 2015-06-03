'''
Performs tests over a series of encoding/decoding methods
'''

import random
from mytimeit import timeit

def test(coder, decoder, N = 2**10, alphabet="abcdefghijklmnopqrstuvwxyz") :
    msg = []
    for _ in range(N) : msg += [alphabet[random.randint(0, len(alphabet) - 1)]]

    print("\n" + ">"*2 + " running tests (length: " + str(N) + ") for: ", end ="")
    print(coder.__name__ + ", " + decoder.__name__)
    coded   = timeit(coder  ) (msg)
    decoded = timeit(decoder) (coded)
    # print("Compression ratio (literal):", getsizeof(coded) / getsizeof(decoded))
    if msg == decoded : print("Decode coincides with the original message")
    else :
        print("Decoding went wrong:")
        print("Original:", msg[:30])
        print("Decoded :", decoded[:30])

if __name__ == '__main__' :
    from MTF import *
    test(mft_encode, mft_decode)

    from RLE import *
    test(rle_encode, rle_decode)

    from BWT import *
    test(bwt_encode, bwt_decode)