'''
Created on Jun 24, 2018

@author: jonas
'''

import random

from src.config import board_size, window_size, append_prefix, \
    append_only_one_point_in_time, max_nr_of_moves
from src.move import Move, Player


def file_to_sgf(content):
    moves = content.split(';')
    
    start_of_moves = 2
    game = []
    for move in moves[start_of_moves:start_of_moves+max_nr_of_moves]:
        if(len(move) < 4):
            continue
        if(move[0] == 'A'):
            continue
        if(move[0] not in [item.value for item in Player]):
            continue
        player = Player(move[0])
        x = ord(move[2]) - ord('a')
        y = ord(move[3]) - ord('a')
        game.append(Move(player, x, y))
    return game

def create_window_seq(game):
    sequences = []
    # a sliding window is defined by a starting point and length
    for i in range(0, (board_size - 1) - window_size):
        for j in range(0, (board_size - 1) - window_size):
                # for all windows get all moves that were made inside the window starting at (i,j) and put them into a sequence.
                seq = filter(lambda move: move.x >= i and move.x < i + window_size and move.y >= j and move.y < j + window_size, game)
                
                # Normalize moves, so that they start at (0,0)
                seq = list(map(lambda move: Move(move.player, move.x - i, move.y - j), seq))
                if(len(seq) == 0):
                    continue
                
                seq_in_one_pos = [seq]
                if append_prefix:
                    seq_in_one_pos += all_prefix(seq)
                if append_only_one_point_in_time:
                    seq_in_one_pos = random.choice(seq_in_one_pos)
                sequences.append(seq_in_one_pos)
    return sequences
    
def to_matrix(seq):
    matrix = []
    # indices are turned. Make this nicer, somehow
    for j in range(0, window_size):
        for i in range(0, window_size):
            possible_move = list(filter(lambda move: move.x == i and move.y == j, seq))
            if len(possible_move) == 0 :
                matrix.append(Player.empty)
            elif len(possible_move) == 1:
                matrix.append(possible_move[0].player)
            elif len(possible_move) >= 2: 
                # TODO: something ko is going on...
                matrix.append(Player.x)
    return matrix

def to_matrix_string(seq):
    matrix_string = ''
    m = to_matrix(seq)
    for move in m:
        matrix_string += str(move.value)
    return matrix_string


def find_all_patterns(pattern, sequences):
    matchedSeqs = []

    for seq in sequences:
        match = True
        for pos in range(0, len(pattern)):
                if pattern[pos] != '?' and seq[0][pos] != pattern[pos]:
                    match = False
        if match:
            matchedSeqs.append(seq)
    return matchedSeqs
    
def all_prefix(seq):
    prefixs = []
    for l in range(1,len(seq)):
        prefixs.append(seq[0:l])
    return prefixs
