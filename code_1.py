#%%
import time
import numpy as np
import suffix_tree as sf #https://pypi.org/project/suffix-tree/

size = 6000 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic string
#str_array = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]) #Create generic string
naive_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 naive index table
cunha_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 cunha index table
cunha_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 cunha index table
idx_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 index table
idx_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 index table

def naive_algorithm(array):
    for i in range(array.size):
        for j in range(array.size - i):
            naive_table_max_1[i] = max(naive_table_max_1[i], np.sum(array[j:j + i + 1]))

def cunha_algorithm(array):
    global un
    counted = get_counted(array)

    start_of_1 = 0 if array[0] == 1 else 1
    start_of_0 = 0 if array[0] == 0 else 1
    
    window = 0
    total_of_1 = 0
    for i in range(start_of_1, len(counted), 2):
        for j in range(i, len(counted), 2):
            un += 1
            window += counted[j]
            window += 0 if j == i else counted[j-1]
            total_of_1 += counted[j]
            cunha_table_max_1[window-1] = max(cunha_table_max_1[window-1], total_of_1)
        window = 0
        total_of_1 = 0
    
    window = 0
    total_of_0 = 0
    for i in range(start_of_0, len(counted), 2):
        for j in range(i, len(counted), 2):
            un += 1
            window += counted[j]
            window += 0 if j == i else counted[j-1]
            total_of_0 += counted[j]
            cunha_table_max_0[window-1] = max(cunha_table_max_0[window-1], total_of_0)
        window = 0
        total_of_0 = 0
        
    windonize_table(cunha_table_max_1)
    windonize_table(cunha_table_max_0)

def get_counted(array):
    counted = []
    cnt = 1
    for i in range(1, array.size):
        if array[i] == array[i-1]:
            cnt += 1
        else:
            counted.append(cnt)
            cnt = 1
    counted.append(cnt)
    return counted

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
    #ignore root node
    if node.end > 0:
        #ignore leaf with terminator
        if ''.join(map(str, node.S[node.start : node.end])) != '$':
            #ignore substring starting with 0
                if ord(node.S[node.start]) > 96:
                    index(node.start, node.end, (node.parent.end - node.parent.start + 1) // 2 * 2)

def index(ini, end, start):
    global counted
    #ignore substring ending in 0 with parent already indexed
    if (end-ini) % 2 != 0 or end-ini-start > 1:
        window = 0
        count = 0
        for i in range(0, start, 2):
            window += counted[ini+i]
            window += 0 if i == 0 else counted[ini+i-1]
            count += counted[ini+i]
        for i in range(start, end-ini, 2):
            global un
            un += 1
            window += counted[ini+i]
            window += 0 if i == 0 else counted[ini+i-1]
            count += counted[ini+i]
            idx_table_max_1[window-1] = max(count, idx_table_max_1[window-1])

def windonize_table(table):
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])
    
un = 0
special_encode = specialPatternEncode(str_array)
counted = get_counted(str_array)
counted = counted if str_array[0] == 1 else counted[1:] #Remove first 0s
counted = counted if str_array[-1] == 1 else counted[:-1] #Remove last 0s
tree = ukkonen_tree(special_encode)
start_time = time.time()
tree.pre_order(get_leaf_str)
windonize_table(idx_table_max_1)
print("SuffixT algorithm: --- %s seconds ---" % (time.time() - start_time))
print('p²= ', un)
#print(idx_table_max_1)

start_time = time.time()
un = 0
cunha_algorithm(str_array)
print("Cunha's algorithm: --- %s seconds ---" % (time.time() - start_time))
print('p²= ', un)
#print(cunha_table_max_0)
#print(cunha_table_max_1)

""" start_time = time.time()
naive_algorithm(str_array)
print("--- %s seconds ---" % (time.time() - start_time))
print(naive_table_max_1) """

#Check if algorithm works
print( (idx_table_max_1==cunha_table_max_1).all() )