'''
Created on Jun 24, 2018

@author: jonas
'''
import unittest
from src.renderer import render_matrix
from src.move import Player
from src.config import window_size
from IPython.utils._tokenize_py2 import Ignore

class Test(unittest.TestCase):


    @Ignore
    def testRenderer(self):
        matrix = [Player.dontcare, Player.dontcare, Player.b,
                  Player.b,Player.b, Player.dontcare, 
                  Player.dontcare, Player.w, Player.dontcare]
        if(window_size != 3):
            print('this test will fail, because window size is not 3.')
        str = render_matrix(matrix)
        self.assertTrue(str == '??B\nBB?\n?W?\n')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRenderer']
    unittest.main()