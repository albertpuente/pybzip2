
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
    symbols = list(range(1,258))
    tables = [[len(y[x]) if x in y else 0 for x in symbols] for y in huffman_tables]
    
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
        d = dict([x for x in zip(sym,table) if x[1] != 0])
        
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
    
    # input to string
    encdata = str(encdata)
    N = len(encdata)
    
    # number of symbols alreadt decoded
    decoded_syms = 0
    
    # codeword limits
    indexa = 0
    indexb = 1
    
    while indexa < N:
        # match prefix
        codeword = encdata[indexa:indexb]
        
        # each block 50 symbols goes to a certain table, according to counts
        ind = decoded_syms // 50
        table_index = tablesused[ind]
        
        if codeword in decbooks[table_index]:
            original.append(decbooks[table_index][codeword])
            decoded_syms += 1
            indexa = indexb
            indexb += 1
        else:
            indexb += 1
            
    return original
    
'''
L = [5, 257, 8, 1, 2, 2, 6, 3, 17, 4, 22, 11, 11, 14, 256, 256, 257, 3, 256, 10, 1, 15, 6, 256, 12, 62, 12, 57, 6, 2, 4, 42, 10, 13, 5, 22, 18, 6, 17, 4, 2, 2, 257, 12, 6, 256, 3, 13, 1, 13, 256, 6, 11, 39, 3, 4, 14, 71, 21, 3, 9, 14, 256, 19, 5, 4, 15, 13, 11, 8, 6, 13, 3, 256, 2, 9, 15, 19, 3, 13, 11, 9, 256, 2, 15, 7, 13, 1, 13, 256, 5, 7, 2, 257, 47, 16, 42, 43, 43, 43, 45, 46, 2, 45, 4, 46, 26, 3, 10, 256, 256, 257, 50, 60, 256, 17, 23, 20, 256, 1, 61, 5, 34, 21, 25, 27, 2, 256, 3, 23, 2, 257, 22, 1, 30, 1, 10, 1, 10, 2, 256, 69, 3, 47, 1, 6, 1, 1, 27, 256, 8, 17, 20, 21, 256, 22, 1, 256, 2, 3, 2, 2, 2, 26, 4, 2, 257, 257,3, 26, 5, 20, 13, 29, 10, 2, 4, 5, 257, 25, 27, 1, 2, 1, 2, 256, 10, 1, 42, 7, 31, 10, 1, 2, 20, 17, 71, 18, 256, 6, 39, 256, 52, 257, 256, 257, 256, 257, 256, 14, 43, 1, 19, 256, 257, 256, 256, 19, 256, 256, 257, 2, 2, 257, 51, 256, 2, 1, 257, 1, 1, 1, 1, 1, 256, 1, 1, 257, 1, 257, 1, 256, 2, 1, 257, 1, 257, 1, 50, 1, 3, 41, 257, 256, 256, 1, 256, 2, 1, 257, 2, 257, 2, 2, 257, 257, 4, 256, 2, 1, 1, 256, 256, 48, 256, 256, 257, 2, 257, 17, 1, 256, 2, 256, 2, 2, 256, 2, 21, 1]

enc = huffman_encode(L)
symbols = list(range(1,258))
#print(enc[0], enc[1], enc[2])
msg = (''.join(enc[0]))
res = huffman_decode(msg,enc[1],enc[2],symbols)
print(res==L)
'''