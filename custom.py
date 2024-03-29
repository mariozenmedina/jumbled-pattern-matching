import time
import suffix_tree as sf #https://pypi.org/project/suffix-tree/
import numpy as np

size = 5000 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic string
#str_array = np.array([0,0,1,1,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,1]) #Create generic string
cunha_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 cunha index table
cunha_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 cunha index table
idx_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 index table
idx_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 index table

def cunha_algorithm(array):
    counted = get_counted(array)
    
    counted_1 = counted
    counted_1 = counted_1 if array[0] == 1 else counted_1[1:] #Remove first 0s
    counted_1 = counted_1 if array[-1] == 1 else counted_1[:-1] #Remove last 0s
    
    cunha_p2_counted(counted_1, cunha_table_max_1)
    
    counted_0 = counted
    counted_0 = counted_0 if array[0] == 0 else counted_0[1:] #Remove first 0s
    counted_0 = counted_0 if array[-1] == 0 else counted_0[:-1] #Remove last 0s
    
    cunha_p2_counted(counted_0, cunha_table_max_0)
        
    windonize_table(cunha_table_max_1)
    windonize_table(cunha_table_max_0)
    
def cunha_p2_counted(counted, table):
    window = 0
    total = 0
    for i in range(0, len(counted), 2):
        for j in range(i, len(counted), 2):
            window += counted[j]
            window += 0 if j == i else counted[j-1]
            total += counted[j]
            table[window-1] = max(table[window-1], total)
        window = 0
        total = 0

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

def windonize_table(table):
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])

def get_summed(counted):
    summed = []
    window = 0
    tot_1 = 0
    for i,v in enumerate(counted):
        window += v
        if i % 2 == 0:
            tot_1 += v
        summed.append([window, tot_1])
    return summed

def get_leaf_str(node):
    #ignore root node
    if node.end > 0:
        #ignore leaf with terminator
        if isinstance(node.S[node.start], int):
            #ignore substring starting with 0
            if node.start % 2 == 0:
                index_1(node.start, node.end, (node.parent.end - node.parent.start + 1) // 2 * 2, idx_table_max_1)
            #starting with 0
            else:
                index_0(node.start, node.end, (node.parent.end - node.parent.start + 1) // 2 * 2, idx_table_max_0)

def index_1(ini, end, start, table):
    global summed
    if (end-ini) % 2 != 0 or end-ini-start > 1:
        window = 0
        count = 0
        for i in range(start, end-ini, 2):
            window = summed[ini+i][0]-(0 if ini == 0 else summed[ini-1][0])
            count = summed[ini+i][1]-(0 if ini == 0 else summed[ini-1][1])
            table[window-1] = max(count, table[window-1])

def index_0(ini, end, start, table):
    global summed
    if (end-ini) % 2 != 0 or end-ini-start > 1:
        window = 0
        count = 0
        for i in range(start, end-ini, 2):
            window = (len(summed) if ini+i >= len(summed) else summed[ini+i][0])-summed[ini-1][0]
            count = window - ((len(summed) if ini+i >= len(summed) else summed[ini+i][1])-summed[ini-1][1])
            table[window-1] = max(count, table[window-1])

def counting_reps(node):
    global repeated
    if node.end > 0:
        if isinstance(node, sf.node.Internal):
            repeated += 1



#print(str_array)
print('String size: ', str_array.size)
print('')

start_time = time.time()
cunha_algorithm(str_array)
print("Cunha's algorithm: --- %s seconds ---" % (time.time() - start_time))
#print(cunha_table_max_1)
#print(cunha_table_max_0)
#print('')


start_time = time.time()
counted = get_counted(str_array)
zeros = [0,0]
if str_array[0] == 0: #Remove first 0s
    zeros[0] = counted[0]
    counted = counted[1:]
if str_array[-1] == 0: #Remove las 0s
    zeros[1] = counted[-1]
    counted = counted[:-1]
#print('zeros', zeros)
summed = get_summed(counted)
#print(counted)
#print(summed)
#maximum run of 1s
max_run_1 = max(counted[::2])
idx_table_max_1[max_run_1-1] = max_run_1
tree = sf.Tree({'A': counted})
tree.pre_order(get_leaf_str)
windonize_table(idx_table_max_1)
windonize_table(idx_table_max_0)
#print('')
print("SfxTree algorithm: --- %s seconds ---" % (time.time() - start_time))
#print(idx_table_max_1)
#print(idx_table_max_0)

#Check if algorithm works
print('Max_1', (idx_table_max_1==cunha_table_max_1).all() )
print('Max_0', (idx_table_max_0==cunha_table_max_0).all() )

#counting reps
""" repeated = 0
tree.post_order(counting_reps)
print('Repetitions: ', repeated) """