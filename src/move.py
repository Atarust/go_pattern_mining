'''
Created on Jun 24, 2018

@author: jonas
'''
from enum import Enum     # for enum34, or the stdlib version

class Move(object):
    '''
    classdocs
    '''
    player = ''
    x = -1
    y = -1

    def __init__(self, player, x, y):
        '''
        Constructor
        '''
        self.player = player
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "move{" + str(self.player.value) + '(' + str(self.x) + ', ' + str(self.y) + ')}'

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.player == other.player and self.x == other.x and self.y == other.y
        return False

class Player(Enum):
    b = 'B'
    w = 'W'
    empty = '_'
    x = 'X'
    dontcare = '?'
    
