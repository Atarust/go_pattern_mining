'''
Created on Jun 27, 2018

@author: jonas
'''
from src.config import window_size


class PatternTree(object):
    
    def __init__(self, pattern):
        self.children = []
        self.pattern = pattern
        self.sequences_counted = []
    
    def __is_at_least_as_general_as(self, other_pattern):
        # make sure sizes are correct?
        for pos in range(len(other_pattern)):
            if self.pattern[pos] != '?' and self.pattern[pos] != other_pattern[pos]:
                return False
        return True
    
    def __is_at_least_as_specific_as(self, other_pattern):
        # make sure sizes are correct?
        for pos in range(len(other_pattern)):
            if other_pattern[pos] != '?' and self.pattern[pos] != other_pattern[pos]:
                return False
        return True

    def __add_child_here(self, new_child):
        self.children.append(new_child) # See if any of the old children fit in the new child
        children_to_remove = []
        for child in self.children:
            if child != new_child: # refactor this out...
                if (new_child.__is_at_least_as_general_as(child.pattern)):
                    new_child.insert_patternTree(child)
                    children_to_remove.append(child)
        
        for child in children_to_remove:
            self.children.remove(child)
            
        # see if sequences can be put into any of the children
        for seq_counted in self.sequences_counted:
            self.insert_sequence_counted(seq_counted)

    def insert_patternTree(self, new_child):
        if(self is new_child):
            print("how can this bee???")
            return
        if self.pattern == new_child.pattern:
            self.sequences_counted += new_child.sequences_counted  # TODO we have a counted sequence, can't just join them!
            for new_child_child in new_child.children:
                self.insert_patternTree(new_child_child)
            return
                
        # does this pattern belong in this subtree?
        if not self.__is_at_least_as_general_as(new_child.pattern):
            print('warning, is not subset')
            return
        
        # does this pattern belong in any of my children
        for child in self.children:
            if child.__is_at_least_as_general_as(new_child.pattern):
                child.insert_patternTree(new_child)
                return
    
        # it does not belong to any of my children, so I must keep it myself        
        self.__add_child_here(new_child)
    
    def insert_sequence_counted(self, seq_counted):
        if not self.__is_at_least_as_general_as(seq_counted[0]):
            print('warning')
            return
        
        # does this pattern belong in any of my children
        for child in self.children:
            if child.__is_at_least_as_general_as(seq_counted[0]):
                child.insert_sequence_counted(seq_counted)
                return
        
        # it does not belong in any of my children, so I must keep it myself
        # TODO: maybe just create a new child from all sequences_counted - if sequence list gets very long, just find a pattern to get rid of many sequences_counted!
        self.sequences_counted.append(seq_counted)
        
    def get_tree_frequency(self): 
        freq = sum(map(lambda s: s[1], self.sequences_counted))
        return freq + sum(map(lambda child: child.get_tree_frequency(), self.children))
    
    def get_frequency_of_pattern(self, pattern):
        
        # When to count a pattern
        # ?? <- Let's try to get freuency of this pattern
        # bw
        
        # ?w <- then also this (frequency is defined as sum of freq of itself and all children)!
        # bw
        
        # ?w <- not this! But maybe children of this!
        # ?w
        
        if self.__is_at_least_as_general_as(pattern):
            if(self.pattern == pattern):
                return self.get_tree_frequency()
            else:
                # Self is more general than pattern
                freq = 0
                for child in self.children:
                    freq += child.get_frequency_of_pattern(pattern)
                return freq
        
        if self.__is_at_least_as_specific_as(pattern):
            return self.get_tree_frequency()
        
        # Partial order says that there may be no relationship between them. -> try children!
        freq = 0
        for child in self.children:
            freq += child.get_frequency_of_pattern(pattern)
        return freq
        
    def get_patterns(self):
        patterns = [self.pattern]
        for child in self.children:
            patterns += child.get_patterns()
        return patterns
         
    def __eq__(self, other):
        if isinstance(other, PatternTree):
            return self.pattern == other.pattern
        return False  
    
    def __repr__(self):
        return self.print_frequencies()
    
    def print_frequencies(self, depth=0):
        string = '{' + str(self.get_tree_frequency()) + ' ' +self.pattern + ' | '
        for child in self.children:
            string += '\n' + depth*'---- ' + child.print_frequencies(depth=depth+1)
        string += '}'
        return string

    
def get_root():
    return PatternTree('?' * (window_size * window_size))
