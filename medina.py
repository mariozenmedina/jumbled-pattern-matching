#%%
import time
import numpy as np
import suffix_tree as sf #https://pypi.org/project/suffix-tree/

size = 1000 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic string
idx_table_max_1 = np.zeros(size).astype(int) #T_max_1 index table

def specialPatternEncode(str_array):
    special_encode = []
    count = 1
    for i in range(1, str_array.size):
        if str_array[i] == str_array[i-1]:
            count += 1
        else:
            if str_array[i-1] == 0:
                count = chr(64+count) #Int to Char
            else:
                count = chr(96+count) #Int to Char
            special_encode.append(count)
            count = 1
    special_encode.append(chr(64+count) if str_array[-1] == 0 else chr(96+count))
    special_encode = np.array(special_encode)
    special_encode = special_encode if str_array[0] == 1 else special_encode[1:] #Remove first 0s
    special_encode = special_encode if str_array[-1] == 1 else special_encode[:-1] #Remove last 0s
    return ''.join(special_encode)

def ukkonen_tree(special_encode):
    tree = sf.Tree({'A': special_encode})
    return tree

def get_leaf_str(node):
    #ignore substring of internal nodes
    if type(node) is sf.node.Leaf:
        #ignore leaf starting in letter
        if isinstance(node.S[node.start], str) and ord(node.S[node.start]) > 96:
            #ignore leaf that end in termination symbol $
            if node.end-(node.start+node.parent.end-node.parent.start) > 1:
                str_to_index = ''.join(map(str, node.S[node.start : node.end-1]))
                index(str_to_index)

def index(str):
    window = 0
    count = 0
    for i in range(0, len(str), 2):
        window += (ord(str[i])-96)
        window += 0 if i == 0 else (ord(str[i-1])-64)
        count += (ord(str[i])-96)
        idx_table_max_1[window-1] = max(count, idx_table_max_1[window-1])

def windonize_table(table):
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])
    
start_time = time.time()
special_encode = specialPatternEncode(str_array)
tree = ukkonen_tree(special_encode)
tree.post_order(get_leaf_str)
windonize_table(idx_table_max_1)
print("--- %s seconds ---" % (time.time() - start_time))
print(idx_table_max_1)