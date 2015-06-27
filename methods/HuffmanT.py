
from heapq import heappush, heappop, heapify
from collections import OrderedDict
from math import ceil

# represents a node
class node:
    def __init__(self, count, symbol='', index=0):
        self.count = count
        self.symbol = symbol      
        self.index = index
        self.word = ''
        
    def __lt__(self, other):
        return self.count < other.count
        
# creates a dictionary d[x]=px, where x is a character and px its probability
# from the input data
def get_counts(data):
    d = {}
    for c in data:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    return(d)
    
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
            
# build an implicit Huffman tree from a priority queue of nodes
# and compute codewords for each node
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
        
# construct a canonical Huffman encoding from an existing codebook
# codebook is a dictionary mapping each character to a binary string
def make_canonical(codebook):
    # sort items according to code length, then symbol value
    D = OrderedDict(sorted(codebook.items(), key = lambda x: (len(x[1]),x[0])))
    # construct canonical code
    first = True
    pre = ''
    for key in D:
        if first:
            # first value gets a string of '0' of the same length
            first = False
            D[key] = '0'*len(D[key])
            pre = D[key]
        else:
            # binary add one
            post = bin(int(pre,2) + int('1',2))[2:]
            # ensure length constancy
            post = pre[0]*(max(0,len(pre)-len(post))) + post
            # if length is greater in original coding add 0s (shift left)
            if (len(D[key]) > len(pre)):
                post += '0'*(len(D[key])-len(pre))
            D[key] = post
            pre = post
    return OrderedDict(sorted(D.items()))
    
# obtain the 6 more frequent symbols after counting
# from a dict d[x]=px
def get_rel_syms(counts):
    if len(counts) <= 6:
        return list(reversed(sorted(counts.items(), key = lambda x: (x[1],x[0]))))
    else:
        L = sorted(counts.items(), key = lambda x: (x[1],x[0]))
        k = len(L)
        return [x for x in reversed(L[k-6:k])]

# obtain the number of tables that should be used in order to compress
# from of pairs (x,px) (minimum 2 tables)
def get_number_tables(mainsyms):
    k = 2
    for i in range(2,len(mainsyms)):
        if mainsyms[i][1] / mainsyms[i-1][1] >= 0.75 and mainsyms[i][1] > 512:
            k += 1
            if k == 6:
                break
        else:
            break
    return k
    
# returns the huffman table that should be used to encode
# (ie the one where the most occuring symbol has a shorter code length)
def select_huffman_table(mainsyms, datablock):
    maxcountsym = max(sorted(list(get_counts(datablock).items())), key = lambda x: (x[1],x[0]))
    for i in range(len(mainsyms)):
        if mainsyms[i][0] == maxcountsym[0]:
            return i


# encode data using multitable huffman encoding    
def huffman_encode(data):
    # construct a dictionary with counts for each character
    N = len(data)
    counts = get_counts(data)

    # get 6 more relevant symbols
    mainsyms = get_rel_syms(counts)
    
    # get number of tables to use and predominant symbols
    numtables = get_number_tables(mainsyms)
    mainsyms = mainsyms[:numtables]
    
    # construct list of huffman tables
    huffman_tables = []
    for i in range(numtables):
        # change most occuring symbols
        previous_sym = mainsyms[max(0,i-1)][0]
        current_sym = mainsyms[i][0]
        
        counts[current_sym] = counts[previous_sym]
        counts[previous_sym] = mainsyms[i][1]
        
        # build priority queue
        counts2 = [(px,x) for x,px in counts.items()]
        heapify(counts2)
        
        #turn counts intro a priority queue of nodes
        nodes = list2nodes(counts2)
    
        # build a Huffman tree using nodes
        make_huffman_tree(nodes)
    
        # make encoding codebook
        codebook = {}
        for x in nodes:
            codebook[x.symbol] = x.word        
            
        # transform to canonical huffman encoding
        codebook = make_canonical(codebook)
        
        # add to list of tables
        huffman_tables.append(codebook)
    
    # encode data using multiple huffman tables
    codedata = []
    tablesused = []
    
    # each block of 50 uses a certain table, according to its counts
    for i in range(ceil(N/50)):
        # obtain block of data
        start = i*50
        end = min(N, start+50)
        
        # choose encoding table
        datablock = data[start:end]
                
        table_index = select_huffman_table(mainsyms, datablock)
        if not table_index:
            # non-existent defaults to 0 (statistical)
            table_index = 0
        
        # encode block
        codeblock = [huffman_tables[table_index][x] for x in datablock]
        codedata += codeblock
        
        # record table used
        tablesused.append(table_index)
    
    # store tables just with length values (because of canonical huffman)
    tables = [[len(x) for x in y.values()] for y in huffman_tables]
    
    return (codedata, tables, tablesused)
    
    
# decodes an encoded data using the encoded tables as lengths, the sequence of 
# tables used and the symbols in the stream
def huffman_decode(encdata, tables, tablesused, symbols):
    # sort list of symbols used
    sym = sorted(symbols)
    N = len(encdata)
    
    # restore lengths to mappings
    decbooks = []
    for table in tables:
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
                # binary add one
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
        decbooks.append(decbook)
    
    # decode to obtain original data
    original = []
    
    # each block 50 symbols goes to a certain table, according to counts
    for i in range(ceil(N/50)):
        start = i*50
        end = min(N, start+50)
        
        # choose table and decode with it
        datablock = encdata[start:end]
        table_index = tablesused[i]
                
        oriblock = [decbooks[table_index][x] for x in datablock]
        original += oriblock
        
    return original
    
'''
L = [3, 0, 0, 0, 0, 88, 3, 3, 0, 0, 0, 0, 114, 25, 0, 0, 0, 0, 67, 2, 0, 0, 57, 1, 0, 0, 10, 1, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 21, 1, 0, 0, 0, 0, 8, 8, 56, 64, 4, 68, 1, 0, 74, 66, 0, 70, 6, 0, 0, 5, 3, 4, 0, 2, 7, 0, 0, 0, 0, 18, 1, 12, 0, 0, 0, 0, 112, 1, 0, 0, 0, 0, 19, 2, 0, 6, 8, 0, 3, 0, 0, 0, 0, 19, 30, 0, 61, 9, 66, 13, 70, 13, 3, 13, 37, 0, 14, 4, 48, 0, 2, 8, 5, 64, 5, 0, 0, 3, 10, 1, 15, 1, 62, 4, 0, 3, 0, 5, 74, 17, 17, 3, 5, 7, 1, 6, 0, 1, 0, 2, 5, 3, 27, 0, 66, 5, 15, 0, 6, 18, 3, 0, 74, 1, 8, 10, 256, 257, 0, 1, 7, 3, 1, 2, 10, 7, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,18, 11, 1, 7, 7, 0, 64, 21, 6, 17, 21, 7, 29, 20, 0, 16, 69, 5, 15, 12, 15, 15, 15, 11, 12, 20, 13, 4, 0, 6, 7, 1, 2, 23, 7, 7, 13, 8, 3, 5, 0, 0, 8, 1, 2, 2, 6, 3, 17, 4, 22, 11, 11, 14, 0, 0, 0, 0, 7, 3, 0, 10, 1, 15, 6, 0, 12, 62, 12, 57, 6, 2, 4, 3,3,3,3,3,3,3,3,3,3,3,3,3,3,42, 10, 13, 5, 22, 18, 6, 17, 4, 2, 2, 0, 0, 12, 6, 0, 3, 13, 1, 13, 0, 6, 11, 39, 3, 4, 14, 71, 21, 3, 9, 14, 0, 19, 5, 4, 15, 13, 11, 8, 6, 13, 3, 0, 2, 9, 15, 19, 257, 256, 234]

#L2 = [88,257,74]

enc = huffman_encode(L)
symbols = [x[0] for x in get_counts(L).items()]

res = huffman_decode(enc[0],enc[1],enc[2],symbols)
print(res==L)
'''