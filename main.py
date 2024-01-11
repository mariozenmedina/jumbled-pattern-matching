import numpy as np


class JumbledPatternMatch:
    size = 16
    str_array = np.zeros(size).astype(int)
    ref_table = np.zeros(size).astype(int)
    idx_table = np.zeros(size).astype(int)

    def new_random(self):
        self.ref_table[:] = 0
        self.idx_table[:] = 0
        self.str_array = np.random.randint(2, size=(1, self.size))[0]
        self.ref_index_table(self.str_array)

    def ref_index_table(self, str_array):
        for i in range(self.size):
            for j in range(self.size - i):
                self.ref_table[i] = max(self.ref_table[i], np.sum(self.str_array[j:j + i + 1]))
        return self.ref_table

    def n_logn(self, str_array):

        edge_zeros = self.remove_edge_zeros_string(str_array)
        counted = self.get_counted(str_array, edge_zeros)

        if counted.size > 1:
            root = self.find_root(counted, edge_zeros)
            self.root_to_edges(counted, root)

            #divide string
            if root[1] == 0:
                #print('init', str_array[(counted[0]+edge_zeros[0]):])
                self.n_logn(str_array[(counted[0]+edge_zeros[0]):])
            elif root[1] == counted.size-1:
                #print('end', str_array[:-(counted[-1]+edge_zeros[1])])
                self.n_logn(str_array[:-(counted[-1]+edge_zeros[1])])
            else:
                #print('mid-init', str_array[:np.sum(counted[:(root[1]+1)])+edge_zeros[0]])
                #print('mid-end', str_array[np.sum(counted[:root[1]])+edge_zeros[0]:])
                self.n_logn(str_array[:np.sum(counted[:(root[1]+1)])+edge_zeros[0]])
                self.n_logn(str_array[np.sum(counted[:root[1]])+edge_zeros[0]:])

        self.windonize_table(self.idx_table)

    def verify_algorithm(self):
        differ = 0
        for i in range(self.size):
            if self.ref_table[i] != self.idx_table[i]:
                differ += 1
        return differ

    def print_tables(self, differ):
        print(jpm.str_array)
        print(self.ref_table)
        print(self.idx_table)
        print((self.ref_table==self.idx_table).all(), ' by: ', differ)

    def windonize_table(self, table):
        for i in range(table.size-2, -1, -1):
            table[i] = max(table[i], table[i+1]-1)
        for i in range(1, table.size):
            table[i] = max(table[i], table[i-1])

    def root_to_edges(self, counted, root):
        offset_left = 0
        offset_right = 0
        offset = 0

        window_value = np.array([root[0], root[0]])

        while (offset_left + offset_right) < counted.size-1:

            left = counted[root[1]-1-offset-offset_left] if (root[1]-1-offset-offset_left > 0) else 0
            right = counted[root[1]+1+offset+offset_right] if (root[1]+1+offset+offset_right < counted.size) else 0

            while (offset < counted.size // 2) & (left == right):
                offset += 1
                left = counted[root[1]-1-offset-offset_left] if (root[1]-1-offset-offset_left > 0) else 0
                right = counted[root[1]+1+offset+offset_right] if (root[1]+1+offset+offset_right < counted.size) else 0
            
            side = (left - right) * (-1 if offset % 2 == 1 else 1)
            if left == 0: #out of bounds
                side = 1
            if right == 0: #out of bounds
                side = -1

            if  side > 0: #grow to right
                self.update_idx_table(window_value, counted[root[1]+offset_right+1])
                window_value[0] += counted[root[1]+offset_right+1] + counted[root[1]+offset_right+2]
                window_value[1] += counted[root[1]+offset_right+2]
                offset_right += 2
            else: #grow to left
                self.update_idx_table(window_value, counted[root[1]-offset_left-1])
                window_value[0] += counted[root[1]-offset_left-1] + counted[root[1]-offset_left-2]
                window_value[1] += counted[root[1]-offset_left-2]
                offset_left += 2
            offset = 0


    def find_root(self, counted, edge_zeros):
        root = np.zeros(2).astype(int)
        offsetPos = 0
        offset = 0
        zeros = np.sum(edge_zeros)
        while counted.size > 1:
            self.update_idx_table([np.sum(counted), np.sum(counted[::2])], zeros)
            while (offset < counted.size // 2) & (counted[0+offset] == counted[-1-offset]):
                offset += 1
           
            side = (counted[offset] - counted[-1-offset]) * (-1 if offset % 2 == 1 else 1)

            if side > 0: #remove right trailing 1s and 0s
                cut1 = counted[-1]
                zeros = counted[-2]
                counted = np.delete(counted, [-1, -2])
            else: #remove left trailing 1s and 0s
                cut1 = counted[0]
                zeros = counted[1]
                offsetPos += 2
                counted = np.delete(counted, [0, 1])
            offset = 0

        root = [counted[0], offsetPos]
        self.update_idx_table([np.sum(counted), np.sum(counted[::2])], zeros)
        return root
    
    def update_idx_table(self, window_value, zeros):
        for i in range(zeros+1):
            self.idx_table[window_value[0]-1+i] = max(window_value[1], self.idx_table[window_value[0]-1+i])

    def get_counted(self, str_array, edge_zeros):
        counted = np.array([]).astype(int)
        soma = 1

        for index, i in enumerate(str_array):
            if index == 0:
                continue
            if i == str_array[index - 1]:
                soma += 1
            else:
                counted = np.append(counted, soma)
                soma = 1
        counted = np.append(counted, soma)

        return counted[(1 if edge_zeros[0] else 0):(-1 if edge_zeros[-1] else counted.size)]

    def remove_edge_zeros_string(self, str_array):
        trailing_zeros = np.zeros(2).astype(int)
        while str_array[0] == 0:
            trailing_zeros[0] += 1
            str_array = np.delete(str_array, 0)
        while str_array[-1] == 0:
            trailing_zeros[1] += 1
            str_array = np.delete(str_array, -1)
        return trailing_zeros
    
    def set_str_array(self, str_array):
        self.str_array = str_array
        self.ref_table[:] = 0
        self.ref_index_table(self.str_array)


jpm = JumbledPatternMatch()
jpm.set_str_array([1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1])
#jpm.new_random()
jpm.n_logn(jpm.str_array)
differ = jpm.verify_algorithm()
jpm.print_tables(differ)


""" differ = 0
stack_limit = 500
while (differ == 0) & (stack_limit > 0):
    jpm.new_random()
    print(jpm.str_array)
    jpm.n_logn(jpm.str_array)
    differ = jpm.verify_algorithm()
    stack_limit -= 1

jpm.print_tables(differ) """