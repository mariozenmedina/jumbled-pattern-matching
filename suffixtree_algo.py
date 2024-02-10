import time
import suffix_tree as sf #https://pypi.org/project/suffix-tree/
import numpy as np

size = 1000 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic binary string
sftree_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 SfTree index table
sftree_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 SfTree index table

############### SF Tree Main Function ###############
def suffix_tree_algorithm(array):
    counted = get_counted(array)
    special_encode = get_special_encode(counted)
    global summed
    summed = get_summed(counted)
    tree = sf.Tree({'A': special_encode}) #starts tree
    tree.pre_order(get_leaf_str) #starts traversal
    windonize_table(sftree_table_max_1)
    windonize_table(sftree_table_max_0)    

############### Auxiliary Functions ###############
def get_counted(array): #Returns array of each run size
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

def windonize_table(table): #Windonize table
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])

def get_special_encode(counted): #Returns array of special encoded
    special_encode = []
    for i,v in enumerate(counted):
        if (i+str_array[0]) % 2 == 0:
            special_encode.append(chr(64+v))
        else:
            special_encode.append(chr(96+v))
    return special_encode

def get_summed(counted): #Auxiliary array, prevents repeated sum of prefix for each tree suffix
    summed, window, tot_1 = [], 0, 0
    for i,v in enumerate(counted):
        window += v
        if (i+str_array[0]) % 2 != 0:
            tot_1 += v
        summed.append([window, tot_1])
    return summed

def get_leaf_str(node): #Each node when traversing the tree
    if node.end > 0: #ignore root node
        if isinstance(node.S[node.start], str): #ignore leaf with terminator
            if (node.start+str_array[0]) % 2 == 0: #substring starting with 0
                index(node.start, node.end, ((node.parent.end - node.parent.start + 1) // 2 ) * 2, sftree_table_max_0, 0)
            else: #substring starting with 1
                index(node.start, node.end, ((node.parent.end - node.parent.start + 1) // 2 ) * 2, sftree_table_max_1, 1)
                

def index(ini, end, start, table, digit): #Index function for each branch
    global summed
    end = len(summed) if end > len(summed) else end
    if (end-ini) % 2 != 0 or end-ini-start > 1:
        window, count = 0, 0
        for i in range(start, end-ini, 2):
            window = summed[ini+i][0]-(0 if ini == 0 else summed[ini-1][0])
            if digit:
                count = summed[ini+i][1]-(0 if ini == 0 else summed[ini-1][1])
            else:
                count = window - (summed[ini+i][1]-(0 if ini == 0 else summed[ini-1][1]))
            table[window-1] = max(count, table[window-1])

############ Starts Suffix Tree Algorithm ############
start_time = time.time()
suffix_tree_algorithm(str_array)
print("Suffix Tree algorithm: --- %s seconds ---" % (time.time() - start_time))
print(sftree_table_max_1)
print(sftree_table_max_0)