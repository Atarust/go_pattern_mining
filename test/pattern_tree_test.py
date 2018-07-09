'''
Created on Jun 28, 2018

@author: jonas
'''
import unittest

from src import pattern_tree
from src.pattern_tree import PatternTree


class Test(unittest.TestCase):

    def test_init(self):
        pt = PatternTree('bwbw')
        self.assertEqual(pt.pattern, 'bwbw')
        self.assertNotEqual(pt.pattern, '????')
        
        root = pattern_tree.get_root()
        self.assertEqual(root.pattern, '????')
    
    def test_insert_patternTree(self):
        pt = pattern_tree.get_root()
        pt.insert_patternTree(PatternTree('wwww'))
        self.assertEqual(len(pt.children), 1, pt)
        self.assertEqual(pt.children[0].pattern, 'wwww')
        
        pt.insert_patternTree(PatternTree('wwww'))
        self.assertEqual(len(pt.children), 1, pt)
        self.assertEqual(pt.children[0].pattern, 'wwww')

        pt.insert_patternTree(PatternTree('wwwb'))
        self.assertEqual(len(pt.children), 2)
        self.assertTrue(pt.children[0].pattern == 'wwww' or pt.children[0].pattern == 'wwwb')
        self.assertTrue(pt.children[1].pattern == 'wwww' or pt.children[1].pattern == 'wwwb')
        
        pt.insert_patternTree(PatternTree('www?'))
        self.assertEqual(len(pt.children), 1, 'children should be sorted into more specific patterns, if one is added.')
        self.assertTrue(pt.children[0].pattern == 'www?')
        child = pt.children[0]
        self.assertEqual(len(child.children), 2)
        self.assertTrue(child.children[0].pattern == 'wwww' or child.children[0].pattern == 'wwwb')
        self.assertTrue(child.children[1].pattern == 'wwww' or child.children[1].pattern == 'wwwb')
        
        pt = pattern_tree.get_root()
        pt.insert_patternTree(PatternTree('wb??'))
        pt.insert_patternTree(PatternTree('bw??'))
        pt.insert_patternTree(PatternTree('b??w'))
        self.assertEqual(len(pt.children), 3)
        
    def test_sequence_counted(self):
        pt = pattern_tree.get_root()
        for p in ['wwww', 'wwwb', 'www?']:
            pt.insert_patternTree(PatternTree(p))
        
        self.assertEqual(pt.get_frequency_of_pattern('wwww'), 0)
        pt.insert_sequence_counted(('wwww', 10))
        self.assertEqual(pt.get_frequency_of_pattern('wwww'), 10)
        
        self.assertEqual(pt.get_frequency_of_pattern('www?'), 10)
        pt.insert_sequence_counted(('wwwb', 20))
        self.assertEqual(pt.get_frequency_of_pattern('wwww'), 10)
        self.assertEqual(pt.get_frequency_of_pattern('wwwb'), 20)
        self.assertEqual(pt.get_frequency_of_pattern('www?'), 30)
        self.assertEqual(pt.get_frequency_of_pattern('????'), 30)
        
        
        pt.insert_sequence_counted(('wwwb', 20))
        self.assertEqual(pt.get_frequency_of_pattern('www?'), 50)
        
        pt = pattern_tree.get_root()
        pt.insert_patternTree(PatternTree('wb??'))
        pt.insert_patternTree(PatternTree('bw??'))
        pt.insert_patternTree(PatternTree('b??w'))
        self.assertEqual(len(pt.children), 3)
        pt.insert_sequence_counted(('wbwb', 10))
        self.assertEqual(pt.get_frequency_of_pattern('wb??'), 10)
        self.assertEqual(pt.get_frequency_of_pattern('w???'), 10)
        self.assertEqual(pt.get_frequency_of_pattern('????'), 10)
        self.assertEqual(pt.get_frequency_of_pattern('b??w'), 0)
        
        pt.insert_sequence_counted(('wbww', 20))
        self.assertEqual(pt.get_frequency_of_pattern('wb??'), 30)
        self.assertEqual(pt.get_frequency_of_pattern('w???'), 30)
        self.assertEqual(pt.get_frequency_of_pattern('????'), 30)
        
        
        pt = pattern_tree.get_root()
        pt.insert_patternTree(PatternTree('www?'))
        pt.insert_sequence_counted(('wwbb', 10))
        self.assertEqual(pt.get_frequency_of_pattern('ww??'), 0, 'Can count pattern only if it is in pattern tree')
        pt.insert_patternTree(PatternTree('ww??'))
        self.assertEqual(pt.get_frequency_of_pattern('ww??'), 10, 'Gets sorted into to most specific pattern, even if pattern is added after the sequence')
    
    def test_balance_tree_split(self):
        pt = pattern_tree.get_root()
        for p in ['ww??']:
            pt.insert_patternTree(PatternTree(p))
        
        pt.insert_sequence_counted(('wwbw', 1000))
        pt.insert_sequence_counted(('wwbb', 1000))
        self.assertEqual(len(pt.children[0].children), 0)
        
        pt.balance_tree()
        self.assertEqual(len(pt.children[0].children), 1)
        self.assertEqual(len(pt.children[0].children[0].children), 1)
        self.assertEqual(len(pt.children[0].children[0].children[0].children), 0)
        
        self.assertTrue(pt.children[0].children[0].children[0].pattern == 'wwbb' or pt.children[0].children[0].children[0].pattern == 'wwbw')
        
    def test_balance_tree_merge(self):
        pt = pattern_tree.get_root()
        for p in ['wwww','wwwb', 'www?']:
            pt.insert_patternTree(PatternTree(p))
        
        pt.insert_sequence_counted(('wwbw', 5))
        pt.insert_sequence_counted(('wwbb', 5))
        self.assertEqual(len(pt.children[0].children), 2)
        
        pt.balance_tree()
        self.assertEqual(len(pt.children[0].children), 0)
        
        
    def test_generality(self):
        self.assertTrue(PatternTree.is_at_least_as_general_as_pattern('wwww', 'wwww'))
        self.assertTrue(PatternTree.is_at_least_as_general_as_pattern('www?', 'wwww'))
        self.assertTrue(PatternTree.is_at_least_as_general_as_pattern('ww??', 'www?'))
        self.assertFalse(PatternTree.is_at_least_as_general_as_pattern('ww??', 'bww?'))
        self.assertFalse(PatternTree.is_at_least_as_general_as_pattern('bw?w', 'bww?'))
        
        
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testInit']
    unittest.main()
