'''
Created on Jun 24, 2018

@author: jonas
'''

from src.move import Move, Player


class SequenceConverter(object):
    '''
    classdocs
    '''

    def __init__(self, sgf_directory, board_size, window_size):
        '''
        Constructor
        '''
        self.board_size = board_size
        self.window_size = window_size

        
    def file_to_sgf(self,content):
        moves = content.split(';')
        
        # cut away header
        moves = moves[2:]
        
        game = []
        for move in moves:
            if(move[0] == 'A'):
                continue
            if(move[0] not in [item.value for item in Player]):
                print("warning, throwing away: " + move)
                continue
            player = Player(move[0])
            x = ord(move[2]) - ord('a')
            y = ord(move[3]) - ord('a')
            game.append(Move(player, x, y))
        return game


    def create_window_seq(self, game):
        sequences = []
        # a sliding window is defined by a starting point and length
        for i in range(0, (self.board_size - 1) - self.window_size):
            for j in range(0, (self.board_size - 1) - self.window_size):
                    # for all windows get all moves that were made inside the window starting at (i,j) and put them into a sequence.
                    seq = filter(lambda move: move.x >= i and move.x < i + self.window_size and move.y >= j and move.y < j + self.window_size, game)
                    
                    # Normalize moves, so that they start at (0,0)
                    seq = map(lambda move: Move(move.player, move.x - i, move.y - j), seq)
                    sequences.append(list(seq))
        return sequences
