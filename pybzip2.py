'''
bzip2 python implementation

CDI-FIB
Joan Ginés, Albert Puente, Andrés Mingorance
'''

import os
import utils.convert as uc
from tests import test

file_name = "input.txt"
file_path = "input/" + file_name
file_size = os.path.getsize(file_path)

with open(file_path, "rb") as file:
    bytes = file.read(file_size)
    from methods.MTF import *
    # test(mtf_encode, mtf_decode, msg=bytes)

    print(bytes)
    coded = mtf_encode(bytes)
    decoded = mtf_decode(coded)

    print(uc.intlist2bytes(coded[0]))
    print(uc.intlist2bytes(decoded))

    # from methods.RLE import *
    # test(rle_encode, rle_decode, msg=bytes)
    #
    # from methods.BWT import *
    # test(bwt_encode, bwt_decode, msg=bytes)
    #
    # from methods.delta import *
    # test(delta_encode, delta_decode, msg=bytes)