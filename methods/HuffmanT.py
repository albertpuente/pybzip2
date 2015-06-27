
from heapq import heappush, heappop, heapify
from collections import OrderedDict

# represents a node
class node:
    def __init__(self, count, symbol='', index=0):
        self.count = count
        self.symbol = symbol      
        self.index = index
        self.word = ''
                
    def __lt__(self, other):
        return self.count < other.count
                        
# creates a priority queue of pairs (px,x), where x is a character and
# px its probability, from the input data
def get_counts(data):
    d = {}
    for c in data:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    Q = [(px,x) for x,px in d.items()]
    heapify(Q)
    return(Q)
    
# creates a queue of nodes from a priority queue of pairs (px,x)
def list2nodes(Q):
    index = 0
    Q2 = []
    for elem in Q:
        index += 1
        Q2.append( node( elem[0], elem[1], index ) )
    return Q2
    
    
# returns first element x in list such that f(x) holds (efficient)
def find(f, L):
    for item in L:
        if f(item): 
            return item
            
# build a Huffman tree from a priority queue of nodes
def make_huffman_tree(nodes):
    # recursion base
    if len(nodes) == 1:
        # this is a leaf node (codeword empty)
        nodes[0].word = ''
    else:
        # pick 2 smallest nodes and delete
        deletednode = heappop(nodes)
        secondnode = heappop(nodes)
        second = secondnode.index
        
        # create a new node (keep symbol of bigger node)
        secondnode.count += deletednode.count
        heappush(nodes,secondnode)
        
        # keep joining nodes recursively until root
        make_huffman_tree(nodes)
        
        # build codeword for the previous 2 nodes
        xnode = find(lambda c: c.index == second, nodes)
        
        # smaller one gets 0 and push back
        deletednode.word = xnode.word+'0'
        heappush(nodes,deletednode)
        
        # bigger one gets 1 and is restored
        xnode.word += '1'
        xnode.count -= deletednode.count
        
 
def huffman_canonical(codebook):
    # sort items according to code length, then symbol value
    D = OrderedDict(sorted(codebook.items(), key = lambda x: (len(x[1]),x[0]) ))
    
    # construct canonical code
    first = True
    pre = ''
    
    for key in D:
        if first:
            first = False
            D[key] = '0'*len(D[key])
            pre = D[key]
        else:
            # add one
            post = bin(int(pre,2) + int('1',2))[2:]
            # ensure length constancy
            post = pre[0]*(max(0,len(pre)-len(post))) + post
            # if length is greater in original coding add 0s
            if (len(D[key]) > len(pre)):
                post += '0'*(len(D[key])-len(pre))
            D[key] = post
            pre = post
    #print(D)
    return dict(sorted(D.items()))
    
    
def huffman_encode(data):
    # construct a priority queue with counts for each character
    counts = get_counts(data)
    #print(counts)
    # turn counts intro a priority queue of nodes
    nodes = list2nodes(counts)
    
    # build a Huffman tree using nodes
    make_huffman_tree(nodes)
    
    # make encoding codebook
    codebook = {}
    for x in nodes:
        codebook[x.symbol] = x.word        
    
    #print(codebook)
    # transform to canonical huffman encoding
    codebook2 = huffman_canonical(codebook)
    
    # map input data
    codedata = [codebook2[x] for x in data]
    
    table = [len(x) for x in codebook2.values()]
    return (codedata,table)
    
    
def huffman_decode(encdata, table, symbols):
    # sort list of symbols used
    sym = sorted(symbols)
    # map symbols to table
    d = dict(zip(sym,table))
    # order by length to recover original order
    D = OrderedDict(sorted(d.items(), key = lambda x: (x[1],x[0]) ))
    
    # reconstruct canonical code
    first = True
    pre = ''
    
    for key in D:
        if first:
            first = False
            D[key] = '0'*D[key]
            pre = D[key]
        else:
            # add one
            post = bin(int(pre,2) + int('1',2))[2:]
            # ensure length constancy
            post = pre[0]*(max(0,len(pre)-len(post))) + post
            # if length is greater in original coding add 0s
            if (D[key] > len(pre)):
                post += '0'*(D[key]-len(pre))
            D[key] = post
            pre = post
            
    # revert mapping to obtain decoding dict
    decbook = {v: k for k, v in D.items()}
    
    # use decoding book to decode data (prefix code)
    original = [decbook[x] for x in encdata]
    #print(original)
    return original
    
'''
L = [3, 0, 0, 0, 0, 88, 3, 0, 0, 0, 0, 114, 25, 0, 0, 0, 0, 67, 2, 0, 0, 57, 1, 0, 0, 10, 1, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 21, 1, 0, 0, 0, 0, 8, 8, 56, 64, 4, 68, 1, 0, 74, 66, 0, 70, 6, 0, 0, 5, 3, 4, 0, 2, 7, 0, 0, 0, 0, 18, 1, 12, 0, 0, 0, 0, 112, 1, 0, 0, 0, 0, 19, 2, 0, 6, 8, 0, 3, 0, 0, 0, 0, 19, 30, 0, 61, 9, 66, 13, 70, 13, 3, 13, 37, 0, 14, 4, 48, 0, 2, 8, 5, 64, 5, 0, 0, 3, 10, 1, 15, 1, 62, 4, 0, 3, 0, 5, 74, 17, 17, 3, 5, 7, 1, 6, 0, 1, 0, 2, 5, 3, 27, 0, 66, 5, 15, 0, 6, 18, 3, 0, 74, 1, 8, 10, 7, 3, 1, 2, 10, 7, 18, 11, 1, 7, 7, 0, 64, 21, 6, 17, 21, 7, 29, 20, 0, 16, 69, 5, 15, 12, 15, 15, 15, 11, 12, 20, 13, 4, 0, 6, 7, 1, 2, 23, 7, 7, 13, 8, 3, 5, 0, 0, 8, 1, 2, 2, 6, 3, 17, 4, 22, 11, 11, 14, 0, 0, 0, 0, 7, 3, 0, 10, 1, 15, 6, 0, 12, 62, 12, 57, 6, 2, 4, 42, 10, 13, 5, 22, 18, 6, 17, 4, 2, 2, 0, 0, 12, 6, 0, 3, 13, 1, 13, 0, 6, 11, 39, 3, 4, 14, 71, 21, 3, 9, 14, 0, 19, 5, 4, 15, 13, 11, 8, 6, 13, 3, 0, 2, 9, 15, 19]

enc = huffman_encode(L)
symbols = [x[1] for x in get_counts(L)]

res = huffman_decode(enc[0],enc[1],symbols)
'''
