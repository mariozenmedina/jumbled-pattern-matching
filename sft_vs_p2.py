import sys
import time
import suffix_tree as sf #https://pypi.org/project/suffix-tree/
import numpy as np
import matplotlib.pyplot as plt

class SuffixTree:
    def __init__(self, array):
        self.array = array  # The input string (as a numpy array of integers)
        self.n = len(array)  # Length of the string
        self.build_tree()
        
    class Node:
        def __init__(self, start=-1, end=-1, parent=None):
            self.start = start  # Starting index of the edge
            self.end = end  # Ending index of the edge
            self.children = {}  # Dictionary to store children (keyed by character)
            self.suffix_link = None  # Suffix link for efficient traversal
            self.parent = parent  # Pointer to the parent node
            self.prefix_size = 0
            
    def build_tree(self):
        self.root = self.Node()  # Root node of the tree
        self.active_node = self.root  # Current active node (used for Ukkonen's algorithm)
        self.active_edge = -1  # The active edge (represented by an index into the string)
        self.active_length = 0  # The length of the active edge
        self.remainder = 0  # Number of suffixes to process
        self.last_created_internal_node = None  # Last created internal node for suffix links

        # Process each character in the input string
        for i in range(self.n):
            self.extend_tree(i)

    def extend_tree(self, i):
        self.remainder += 1
        self.last_created_internal_node = None
        
        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = i

            current_char = self.array[self.active_edge]

            if current_char not in self.active_node.children:
                # Criar nova folha
                new_leaf = self.Node(start=i, end=self.n, parent=self.active_node)
                self.active_node.children[current_char] = new_leaf

                # Suffix link para o último nó interno criado
                if self.last_created_internal_node is not None:
                    self.last_created_internal_node.suffix_link = self.active_node

                self.last_created_internal_node = self.active_node
            else:
                next_node = self.active_node.children[current_char]
                edge_length = next_node.end - next_node.start

                if self.active_length >= edge_length:
                    # Move para o próximo nó
                    self.active_edge += edge_length
                    self.active_length -= edge_length
                    self.active_node = next_node
                    continue

                if self.array[next_node.start + self.active_length] == self.array[i]:
                    # Caracter correspondente: extende o comprimento ativo
                    self.active_length += 1
                    if self.last_created_internal_node is not None:
                        self.last_created_internal_node.suffix_link = self.active_node
                    break
                else:
                    # Dividir aresta
                    split_node = self.Node(start=next_node.start, 
                                        end=next_node.start + self.active_length, 
                                        parent=self.active_node)
                    self.active_node.children[current_char] = split_node

                    # Atualizar o nó dividido
                    next_node.start += self.active_length
                    next_node.parent = split_node
                    split_node.children[self.array[next_node.start]] = next_node

                    # Criar novo nó folha
                    new_leaf = self.Node(start=i, end=self.n, parent=split_node)
                    split_node.children[self.array[i]] = new_leaf

                    # Configurar suffix link
                    if self.last_created_internal_node is not None:
                        self.last_created_internal_node.suffix_link = split_node

                    self.last_created_internal_node = split_node

            self.remainder -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = i - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link or self.root
    
    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        
        for child_key, child_node in node.children.items():
            edge_string = ''.join(map(str, self.array[child_node.start:child_node.end]))
            parent_info = f" (Parent Start: {child_node.parent.start if child_node.parent else 'None'})"
            print(f"{' ' * depth}Edge {edge_string}: Node({child_node.start}, {child_node.end}){parent_info}")
            self.print_tree(child_node, depth + 2)

            
############################################################ CONFIGS ############################################################

size = 5000 #Binary String Size
str_array = np.random.randint(2, size=(1, size))[0] #Create generic binary string

""" size = 10 #Binary String Size
str_array = np.array([1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]) #Create generic binary string """

jbm2017_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 Jbm2017 algorithm index table
jbm2017_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 Jbm2017 algorithm index table
sftree_table_max = np.array([
    np.zeros(str_array.size).astype(int), #T_max_1 SfTree index table
    np.zeros(str_array.size).astype(int) #T_max_0 SfTree index table
])

############### JBM 2017 Main Function ###############
def jumbled_matching_2017(array):
    counted = get_counted(array)
    counted_1 = counted
    counted_1 = counted_1 if array[0] == 1 else counted_1[1:] #Remove first 1s
    counted_1 = counted_1 if array[-1] == 1 else counted_1[:-1] #Remove last 1s
    jbm2017_index(counted_1, jbm2017_table_max_1) #Index each run of 1s
    counted_0 = counted
    counted_0 = counted_0 if array[0] == 0 else counted_0[1:] #Remove first 0s
    counted_0 = counted_0 if array[-1] == 0 else counted_0[:-1] #Remove last 0s
    jbm2017_index(counted_0, jbm2017_table_max_0) #Index each run of 0s
    windonize_table(jbm2017_table_max_1)
    windonize_table(jbm2017_table_max_0)

############### SF Tree Main Function ###############
def suffix_tree_algorithm(array, table):
    counted = get_counted(array)
    summed = get_summed(counted)
    tree = SuffixTree(counted)
    #tree.print_tree()
    suffix_indexing_iterative(tree, summed, table)
    windonize_table(table[0])
    windonize_table(table[1])

############### Auxiliary Functions ###############
def jbm2017_index(counted, table): #Index each run
    window, total = 0, 0
    for i in range(0, len(counted), 2):
        for j in range(i, len(counted), 2):
            window += counted[j]
            window += 0 if j == i else counted[j-1]
            total += counted[j]
            table[window-1] = max(table[window-1], total)
        window, total = 0, 0

def get_counted(array):  # Returns array of each run size
    counted = np.zeros(array.size, dtype=int)  # Initialize an array to store the counts
    cnt = 1
    idx = 0  # Index for inserting run lengths into `counted`
    
    # Loop through the array to count consecutive runs
    for i in range(1, array.size):
        if array[i] == array[i-1]:
            cnt += 1
        else:
            counted[idx] = cnt
            idx += 1  # Move to the next index for a new run
            cnt = 1  # Reset the count for the next run
    
    # Don't forget to append the last run's count
    counted[idx] = cnt
    idx += 1  # Increment index for the final run
    
    # Slice `counted` to the exact number of runs
    return counted[:idx]

def windonize_table(table): #Windonize table
    for i in range(table.size-2, -1, -1):
        table[i] = max(table[i], table[i+1]-1)
    for i in range(1, table.size):
        table[i] = max(table[i], table[i-1])

def get_summed(counted): #Auxiliary array, prevents repeated sum of prefix for each tree suffix
    summed, window, tot_1 = np.zeros((counted.size, 2), dtype=int), 0, 0
    str_array0 = str_array[0]
    for i,v in enumerate(counted):
        window += v
        if (i+str_array0) % 2 != 0:
            tot_1 += v
        summed[i] = [window, tot_1]
    return summed

def suffix_indexing_iterative(tree, summed, table):
    str_array0 = str_array[0]
    stack = [tree.root]
    
    while stack:
        node = stack.pop()
        
        if node.parent is not None:
            
            next_parent = node.parent
            if next_parent.start != -1:
                while next_parent.start != -1:
                    node.prefix_size -= next_parent.end - next_parent.start
                    next_parent = next_parent.parent
            
            string_start = node.start+node.prefix_size
            
            # Compute `digit` and indices once for all iterations
            digit = 0 if (string_start % 2 == 0) == (str_array0 == 0) else 1
            index = table[digit]
            
            # Where the string really starts
            """ edge_string = ''.join(map(str, tree.array[node.start:node.end]))
            parent_info = f" (ParentNode: {node.parent.start if node.parent else 'None'}, {node.parent.end if node.parent else 'None'})"
            print(f"Edge {edge_string}: Node({node.start}, {node.end}) {parent_info}", digit, node.prefix_size) """
            
            summedParent = summed[string_start - 1] if string_start != 0 else np.array([0, 0], dtype=summed.dtype)
            
            # Pré-carregando valores dos pais
            summedParent0, summedParent1 = summedParent
            
            # Determina os slices de uma vez (para evitar loops individuais)
            start, end = string_start, node.end
            range_indices = np.arange(start, end, 2)
            
            # Cache de valores das faixas no numpy
            summedRange = summed[range_indices]
            summedRange0 = summedRange[:, 0]  # Primeiro valor
            summedRange1 = summedRange[:, 1]  # Segundo valor
            
            # Cálculo das janelas (window)
            windows = summedRange0 - summedParent0
            
            # Cálculo dos counts vetorizados
            if digit == 0:
                counts = windows - (summedRange1 - summedParent1)
            else:
                counts = summedRange1 - summedParent1

            # Atualização vetorizada de índices
            np.maximum.at(index, windows - 1, counts)

        # Add children to stack (push children of the current node)
        for child_key, child_node in node.children.items():
            stack.append(child_node)

def create_fibonacci_word(length):
    # Inicialização das primeiras palavras
    fib_0 = "0"
    fib_1 = "01"
    
    # Continue gerando até atingir o tamanho necessário
    while len(fib_1) < length:
        fib_0, fib_1 = fib_1, fib_1 + fib_0  # Atualização baseada na definição

    # Corta a sequência até o tamanho desejado e converte para np.array
    return np.array(list(map(int, fib_1[:length])))

############ Print string size ############
print('String size: ', str_array.size)
print('')

############ Starts Suffix Tree Algorithm ############
start_time = time.time()
suffix_tree_algorithm(str_array, sftree_table_max)
print("Suffix Tree algorithm: --- %s seconds ---" % (time.time() - start_time))
#print(sftree_table_max[1])
print('')

############ Starts Jumbled Matching 2017 Algorithm ############
start_time = time.time()
jumbled_matching_2017(str_array)
print("Jumbled Matching 2017: --- %s seconds ---" % (time.time() - start_time))
#print(jbm2017_table_max_1)
print('')

############ Compare if tables match ############
print('Max_1', (sftree_table_max[1]==jbm2017_table_max_1).all() )
print('Max_0', (sftree_table_max[0]==jbm2017_table_max_0).all() )


#### média de comparações
""" cunha = []
sftree = []
for i in range(1):
    size = 100 #Binary String Size
    str_array = np.random.randint(2, size=(1, size))[0] #Create generic binary string
    #str_array = np.tile([1, 0], size // 2 + 1)[:size]
    #str_array = create_fibonacci_word(size)
    jbm2017_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 Jbm2017 algorithm index table
    jbm2017_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 Jbm2017 algorithm index table
    sftree_table_max = np.array([
        np.zeros(str_array.size).astype(int), #T_max_1 SfTree index table
        np.zeros(str_array.size).astype(int) #T_max_0 SfTree index table
    ])
    
    start_time = time.time()
    suffix_tree_algorithm(str_array, sftree_table_max)
    sftree.append(time.time() - start_time)
    
    start_time = time.time()
    jumbled_matching_2017(str_array)
    cunha.append(time.time() - start_time)

print('Cunha average: ', sum(cunha)/len(cunha))
print('Stree average: ', sum(sftree)/len(sftree))
print('')
print('Cunha min: ', min(cunha))
print('Stree min: ', min(sftree))
print('')
print('Cunha max: ', max(cunha))
print('Stree max: ', max(sftree))

cunha_count = 0
for i,v in enumerate(cunha):
    if sftree[i] >= v:
        cunha_count += 1

print(cunha_count) """


#### PLOT
""" # Function to measure time taken by a function
def measure_time(func, n):
    start_time = time.time()
    func(n)
    end_time = time.time()
    return end_time - start_time

# Input sizes to test
input_sizes = []

# Lists to store the time taken for each algorithm
cunha = []
sftree = []

for i in range(1, 500):
    size = 50 * i #Binary String Size
    input_sizes.append(size)
    #str_array = np.random.randint(2, size=(1, size))[0] #Create generic binary string
    #str_array = np.tile([1, 0], size // 2 + 1)[:size]
    str_array = create_fibonacci_word(size)
    jbm2017_table_max_1 = np.zeros(str_array.size).astype(int) #T_max_1 Jbm2017 algorithm index table
    jbm2017_table_max_0 = np.zeros(str_array.size).astype(int) #T_max_0 Jbm2017 algorithm index table
    sftree_table_max = np.array([
        np.zeros(str_array.size).astype(int), #T_max_1 SfTree index table
        np.zeros(str_array.size).astype(int) #T_max_0 SfTree index table
    ])
    
    start_time = time.time()
    suffix_tree_algorithm(str_array, sftree_table_max)
    sftree.append(time.time() - start_time)
    
    start_time = time.time()
    jumbled_matching_2017(str_array)
    cunha.append(time.time() - start_time)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(input_sizes, cunha, label="JBM2017", color='red', marker='x')
plt.plot(input_sizes, sftree, label="SFTree", color='blue', marker='o')

plt.xlabel('Input Size')
plt.ylabel('Time (seconds)')
plt.title('Comparison of Algorithm 1 and Algorithm 2')
plt.legend()
plt.grid(True)
plt.show() """