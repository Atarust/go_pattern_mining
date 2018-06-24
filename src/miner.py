'''
Created on Jun 24, 2018

@author: jonas

'''

import random

from src.move import Player
from src.renderer import Renderer
from src.sequenceConverter import SequenceConverter
from src.utils import open_files

import pandas as pd


def findAllPatterns(pattern, sequences):
    matchedSeqs = []
        
    for seq in sequences:
        match = True
        matrix = to_matrix(seq)
        for pos in range(0, len(pattern)):
                if pattern[pos] != Player.dontcare and matrix[pos] != pattern[pos]:
                    match = False
        if match:
            matchedSeqs.append(seq)

    return matchedSeqs


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


def gen_rand_pattern(size, nr_of_stones):
    set_stone = 0
    pattern = [Player.dontcare] * (size * size)
    while set_stone < nr_of_stones and set_stone < size * size:
        pos = random.randint(0, len(pattern) - 1)
        if(pattern[pos] == Player.dontcare):
            # is free
            pattern[pos] = random.choice([Player.b, Player.w])
            set_stone += 1
    return pattern


window_size = 2
board_size = 19
nr_of_stones = 8
nr_of_patterns = 10
max_games_per_strength = 10
games_dir = "../sgfs/"
data_dir="../data_output/"

renderer = Renderer(board_size, window_size)

patterns = [gen_rand_pattern(window_size, nr_of_stones) for _ in range(nr_of_patterns)]

strengths = ['1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p']
#strengths = ['1p', '2p']
seqs = []
nr_of_games = []
nr_of_seqs = []
for strength in strengths:
    sgf_dir = games_dir + strength
    files_content = open_files(sgf_dir)[:max_games_per_strength]
    seq_conv = SequenceConverter(sgf_dir, board_size, window_size)

    count_games = 0
    count_seq = 0
    sequences = []
    for content in files_content:
        g = seq_conv.file_to_sgf(content)
        s = seq_conv.create_window_seq(g)
        sequences += s
        count_games += 1
        count_seq += len(s)
    seqs.append(sequences)
    nr_of_games.append(count_games)
    nr_of_seqs.append(count_seq)
    

sequences = pd.DataFrame({'strength' : strengths, 'sequence' : seqs, 'nrOfGames' : nr_of_games, 'nrOfSequences' : nr_of_seqs})  

data_strength = []
data_pattern = []
data_nr_of_stones = []
data_window_size = []
data_nr_of_games = []
data_nr_of_seqs = []

data_freq = []
for index, item in sequences.iterrows():
    pattern_freqs = []
    for pattern in patterns:
        data_freq.append(len(findAllPatterns(pattern, item['sequence'])))
        data_strength.append(item['strength'])
        data_nr_of_games.append(item['nrOfGames'])
        data_nr_of_seqs.append(item['nrOfSequences'])
        data_pattern.append(renderer.render_matrix(pattern))
        data_nr_of_stones.append(nr_of_stones)
        data_window_size.append(window_size)
    
df = pd.DataFrame({'strength' : data_strength,
                   'pattern' : data_pattern,
                   'frequency' : data_freq,
                   'nrOfStones' : data_nr_of_stones,
                   'nrOfGames' : data_nr_of_games,
                   'nrOfSequences' : data_nr_of_seqs})
    
print(df)

total_nr_games = df['nrOfGames'].sum()

filename = data_dir + 'freqs'
filename += '_patterns' + str(nr_of_patterns) 
filename += '_games' + str(total_nr_games) 
filename += '_ws' + str(window_size)
filename += '_stones' + str(nr_of_stones) 
filename += '.csv'

df.to_csv(filename, index=False)

# User pattern
# pattern = ['_', '_', 'B',
#           '_', '_', 'B',
#           '_', '_', 'B']
# pattern = list(map(lambda p: Player(p), pattern))
    
