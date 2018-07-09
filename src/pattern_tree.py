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
        assert(len(self.pattern) == len(other_pattern)), str(len(self.pattern)) + ' ' + str(len(other_pattern))
        return PatternTree.is_at_least_as_general_as_pattern(self.pattern, other_pattern)
    
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
        remove_seq_c = []
        for seq_counted in self.sequences_counted:
            for child in self.children:
                if child.__is_at_least_as_general_as(seq_counted[0]):
                    remove_seq_c.append(seq_counted)
                    child.insert_sequence_counted(seq_counted)
                    break
        for rem in remove_seq_c:
            self.sequences_counted.remove(rem)

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
        freq = total_nr_seqs(self.sequences_counted)
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
    
    def __merge_node(self):
        for child in self.children:
            self.sequences_counted += child.sequences_counted
        self.children = []
    
    def __split_node(self):
        
        if self.pattern.count('?') == 0:
            # is leaf, thus do nothing
            return
        
        # create possible candidates
        candidates = []
        for pos in range(len(self.pattern)):
            c = self.pattern[pos]
            if c == '?':
                for replace_with in ['b', 'w', '_']:
                    new_pattern = self.pattern[:pos] + replace_with + self.pattern[pos + 1:]
                    
                    for child in self.children:
                        if child.pattern == new_pattern:
                            continue
                    
                    freq_of_new_pattern = 0
                    for s_c in self.sequences_counted:
                        if PatternTree.is_at_least_as_general_as_pattern(new_pattern, s_c[0]):
                            freq_of_new_pattern += s_c[1]
                    
                    if freq_of_new_pattern > 0:
                        candidates.append(new_pattern)
        
        # evaluate candidates, how even they distribute the patterns
        candidates_split_efficiency = []
        for candidate in candidates:
            # how many sequences in candidate?
            seq_in_candidate = 0
            for s_c in self.sequences_counted:
                if PatternTree.is_at_least_as_general_as_pattern(candidate, s_c[0]):
                    seq_in_candidate += s_c[1]
            
            # how much does it differ from an even split (optimal = both patterns get the same amount of sequences
            seq_per_node_decrease = abs(total_nr_seqs(self.sequences_counted)/2 - seq_in_candidate)
            if seq_in_candidate > 0:
                candidates_split_efficiency.append((candidate, seq_per_node_decrease))
        
        if candidates_split_efficiency != []:
            # which candidate has the best efficiency ( eff=0 means that the pattern divides the sequences optimally)
            candidates_split_efficiency.sort(key=lambda p_eff: p_eff[1], reverse=True)
            self.insert_patternTree(PatternTree(candidates_split_efficiency[0][0]))
    
    def balance_tree(self):
        # balance the tree such that all nodes roughly have the same amount of sequences
        min_seq_per_subtree = 5
        max_seq_per_node = 500
        
        # TODO: this is more complicated than this. You must look at other levels too!
        if self.get_tree_frequency() < min_seq_per_subtree:
            self.__merge_node()
        
        freq_only_this_node = total_nr_seqs(self.sequences_counted)
        if freq_only_this_node > max_seq_per_node:
            self.__split_node()
        for child in self.children:
            child.balance_tree()
        
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
        string = '{' + str(self.get_tree_frequency()) + ' ' + self.pattern + ' | '
        for child in self.children:
            string += '\n' + depth * '---- ' + child.print_frequencies(depth=depth + 1)
        string += '}'
        return string
    
    @staticmethod
    def is_at_least_as_general_as_pattern(first_pattern, second_pattern):
        for pos in range(len(second_pattern)):
            if first_pattern[pos] != '?' and first_pattern[pos] != second_pattern[pos]:
                return False
        return True


def get_root():
    return PatternTree('?' * (window_size * window_size))


def total_nr_seqs(seq_counted):
    return sum(map(lambda s: s[1], seq_counted))

