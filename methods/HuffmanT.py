
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
    return D
    
    
def huffman_encode(data):
    # construct a priority queue with counts for each character
    counts = get_counts(data)
    
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
    CB = canonical_code = huffman_canonical(codebook)
    
    # map input data
    codedata = [len(CB[x]) for x in data]
    #print(codedata)
    return codedata
    