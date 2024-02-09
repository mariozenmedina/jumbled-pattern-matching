import time
import numpy as np

size = 3200 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic string
#str_array = np.array([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]) #Create generic string
cunha_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 cunha index table
idx_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 index table

def cunha_algorithm(array):
    counted = get_counted(array)
    window = 0
    total_of_1 = 0
    for i in range(0, len(counted), 2):
        for j in range(i, len(counted), 2):
            window += counted[j]
            window += 0 if j == i else counted[j-1]
            total_of_1 += counted[j]
            cunha_table_max_1[window-1] = max(cunha_table_max_1[window-1], total_of_1)
        window = 0
        total_of_1 = 0
        
    windonize_table(cunha_table_max_1)

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
    counted = counted if str_array[0] == 1 else counted[1:] #Remove first 0s
    counted = counted if str_array[-1] == 1 else counted[:-1] #Remove last 0s
    return counted

def get_summed(array):
    summed = []
    tot = 0
    for i in range(array.size):
        lft = tot
        if array[i] == 1:
            tot += 1
        summed.append([lft, tot])
    return summed

def windonize_table(table):
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])

def the_new_try(summed, array, table):
    i = 0
    while i < len(summed):
        
        qnt_0 = 0
        window = len(summed)-i-1
        
        for j in range(0, len(summed)-window):
            
            if array[j] == 1 or array[window+j] == 1:
            
                count = summed[window+j][1]-summed[j][0]
                if count >= table[window]:
                                    
                    qnt_0_jan_esq = 0
                    m = j
                    while m < (window+1) and array[m] == 0:
                        qnt_0_jan_esq += 1
                        m += 1
                    m = j+window
                    qnt_0_jan_dir = 0
                    while m > j and array[m] == 0:
                        qnt_0_jan_dir += 1
                        m -= 1
                        
                    qnt_0_jan = qnt_0_jan_esq + qnt_0_jan_dir
                    
                    if count == table[window]:
                        qnt_0 = max(qnt_0, qnt_0_jan)
                    if count > table[window]:
                        table[window] = count
                        qnt_0 = qnt_0_jan
        
        #agora sabemos o quanto podemos diminuir
        i += qnt_0 if qnt_0 > 0 else 1
        
    windonize_table(table)
            
        
start_time = time.time()
cunha_algorithm(str_array)
print("Cunha's algorithm: --- %s seconds ---" % (time.time() - start_time))
#print(cunha_table_max_1)


start_time = time.time()
summed = get_summed(str_array)
the_new_try(summed, str_array, idx_table_max_1)
print("New try algorithm: --- %s seconds ---" % (time.time() - start_time))
#print(idx_table_max_1)

#Check if algorithm works
print( (idx_table_max_1==cunha_table_max_1).all() )
