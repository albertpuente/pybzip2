'''
bzip2 python implementation

CDI-FIB
Joan Ginés, Albert Puente, Andrés Mingorance
'''

filename = "input.txt"

with open("input/" + filename, "rb") as file:
    byte = file.read(1)
    while byte != "":
        # do something with the byte

        # then read the next
        byte = file.read(1)