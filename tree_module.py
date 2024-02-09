class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = []
    
    def has_child(self, num):
        for i in range(len(self.children)):
            if self.children[i].value == num:
                return i
        return -1
    
    def append(self, num):
        self.children.append(Node(num))
        return len(self.children)-1
    
    def build(self, counted):
        if counted:
            child_idx = self.has_child(counted[0])
            if child_idx < 0:
                child_idx = self.append(counted[0])
            self.children[child_idx].build(counted[1:])
    
    

class Tree(object):
    def __init__(self, root):
        self.root = Node(root)
        self.count = 0
    
    def pre_order_subs(self, start, subs, table, w_v = [0, 0], digit = False, depth = 0):
        self.count += 1
        if start:
            """ if depth > 0:
                subs.append(start.value)
            if digit:
                if depth > 1:
                    w_v[0] += subs[0] + subs[1]
                    w_v[1] += subs[1]
                else:
                    w_v = [subs[0], subs[0]]
                #table[w_v[0]-1] = max(table[w_v[0]-1], w_v[1])
                #print(subs, w_v, depth)
                #subs = []
            
            depth += 1 """
            for i in range(len(start.children)):
                self.pre_order_subs(start.children[i], subs, table, w_v, not digit, depth)