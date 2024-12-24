import numpy as np

class SuffixTree:
    def __init__(self, array, digit = 1):
        self.array = array  # The input string (as a numpy array of integers)
        self.n = len(array)  # Length of the string
        self.digit = digit
        self.build_tree()
        
    class Node:
        def __init__(self, start=-1, end=-1, digit = -1):
            self.start = start  # Starting index of the edge
            self.end = end  # Ending index of the edge
            self.children = {}  # Dictionary to store children (keyed by character)
            self.suffix_link = None  # Suffix link for efficient traversal
            
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
        self.remainder += 1  # Increase the number of suffixes to process
        self.last_created_internal_node = None  # Reset the last created internal node
        
        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = i  # Start with the edge at index i
            if self.array[self.active_edge] not in self.active_node.children:
                # Create a new leaf node
                if i % 2 == 0:
                    currentDigit = self.digit
                else:
                    currentDigit = 1 if self.digit == 0 else 0
                self.active_node.children[self.array[self.active_edge]] = self.Node(start=i, end=self.n, digit=currentDigit)
                
                # Suffix link handling: if we already have an internal node
                if self.last_created_internal_node is not None:
                    self.last_created_internal_node.suffix_link = self.active_node
                
                # Update the last created internal node
                self.last_created_internal_node = self.active_node
            else:
                # We have an existing child for this character, so walk down the edge
                next_node = self.active_node.children[self.array[self.active_edge]]
                edge_length = next_node.end - next_node.start
                
                if self.active_length >= edge_length:
                    # The active length exceeds the edge, so we need to move to the next edge
                    self.active_edge += edge_length
                    self.active_length -= edge_length
                    self.active_node = next_node
                    continue  # Re-evaluate the current suffix
            
                if self.array[next_node.start + self.active_length] == self.array[i]:
                    # We have a match, extend the active length
                    self.active_length += 1
                    if self.last_created_internal_node is not None:
                        self.last_created_internal_node.suffix_link = self.active_node
                    break
                else:
                    # We have a mismatch, so split the edge
                    split_node = self.Node(start=next_node.start, end=next_node.start + self.active_length)
                    self.active_node.children[self.array[self.active_edge]] = split_node
                    
                    # Create the new leaf node
                    split_node.children[self.array[i]] = self.Node(start=i, end=self.n)
                    next_node.start += self.active_length
                    split_node.children[self.array[next_node.start]] = next_node
                    
                    # Suffix link handling
                    if self.last_created_internal_node is not None:
                        self.last_created_internal_node.suffix_link = split_node
                    self.last_created_internal_node = split_node
                    
            self.remainder -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = i - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link is not None else self.root
                
    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        
        for child_key, child_node in node.children.items():
            edge_string = ''.join(map(str, self.array[child_node.start:child_node.end]))
            print(f"{' ' * depth}Edge {edge_string}: Node({child_node.start}, {child_node.end})")
            self.print_tree(child_node, depth + 2)

    # Pre-order traversal method
    def pre_order_traversal(self, node=None):
        # Default to root if no node is provided
        if node is None:
            node = self.root
        
        # First, process the current node (print or collect its information)
        edge_string = ''.join(map(str, self.array[node.start:node.end])) if node.start != -1 and node.end != -1 else "Root"
        print(f"Node({node.start}, {node.end}): Edge = {edge_string}")
        
        # Then, recursively visit all children
        for child_key, child_node in node.children.items():
            self.pre_order_traversal(child_node)

# Example usage:
text = np.array([1, 0, 1, 1, 0, 1, 0, 1])  # Binary string as a numpy array (e.g., "10110101")
suffix_tree = SuffixTree(text)

# Print the tree (for debugging purposes)
suffix_tree.pre_order_traversal()