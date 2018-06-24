'''
Created on Jun 24, 2018

@author: jonas
'''


class Renderer(object):
    '''
    classdocs
    '''

    def __init__(self, board_size, window_size):
        '''
        Constructor
        '''
        self.board_size = board_size
        self.window_size = window_size
        
    def render_matrix(self, matrix):
        string = ""
        i = 0
        for m in matrix:
            string += str(m.value)
            i += 1
            if(i % self.window_size == 0):
                string += "\n"
        return string
