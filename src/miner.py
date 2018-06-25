'''
Created on Jun 24, 2018

Further Ideas:
    * Make more efficient
        -> hashing of pattern, hashing of sequences to compare faster (would allow MANY patterns to compare in probably near sublinear time
        -> build  tree of patterns, then save sequences in that tree. (would allow MANY sequences to compare MANY patterns. O(logn) I guess - but probably small window size...
        -> use a different approach to find most common patterns - not good. I am no necessarily intereted in most common patterns, more in how they differ strength-wise. 
        -> Do some iterative approach, to filter out early patterns that are not common in any strength level anyway.
        -> Make some kind of mutation (not moving stones, more like getting more specific or something
        -> Find association rules. That is, moves that are played on a certain pattern!!
        -> Visualize the patterns better (maybe create micro picture of pattern)
        -> Visualize pattern tree
        -> make a status bar + estimated end time
@author: jonas

'''

from collections import Counter
import random
import time

import pandas as pd
from src.config import window_size, data_dir, games_dir, max_games_per_strength, nr_of_patterns, nr_of_stones, strengths, estimatedTime, \
    estimatedTimeSetup, strengthHash
from src.move import Player
from src.renderer import render_matrix
from src.sequenceConverter import file_to_sgf, create_window_seq, find_all_patterns, to_matrix_string
from src.utils import open_files


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


#print(str(estimatedTime) + " sec estimated.")
print(str(estimatedTime/(60*60)) + " h estimated.")
print(str(estimatedTimeSetup) + " sec estimated for setup.")


t = time.time()
totalTime = t

patterns = [gen_rand_pattern(window_size, nr_of_stones) for _p in range(nr_of_patterns)]

seqs = []
nr_of_games = []
nr_of_seqs = []
for strength in strengths:
    sgf_dir = games_dir + strength
    files_content = open_files(sgf_dir, max_games_per_strength)

    count_games = 0
    count_seq = 0
    sequences = []
    for content in files_content:
        g = file_to_sgf(content)
        s = create_window_seq(g)
        sequences += s
        count_games += 1
        count_seq += len(s)
    #sequences = list(map(lambda s: to_matrix_string(s), sequences))
    #seqs.append(Counter(sequences))
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

nr_of_files = sequences['nrOfGames'].sum()
print("time to read all files: total=" + str(time.time() - t) + 'sec. Per file=' + str((time.time() - t)/nr_of_files))
t = time.time()

data_freq = []
for index, item in sequences.iterrows():
    pattern_freqs = []

    for pattern in patterns:
        #t = time.time()
        data_freq.append(len(find_all_patterns(pattern, item['sequence'])))
        #print("time find_all_patterns per sec/250k sequences (250k is average per game): " + str(250000*(time.time() - t)/len(item['sequence'])))

        data_strength.append(item['strength'])
        data_nr_of_games.append(item['nrOfGames'])
        data_nr_of_seqs.append(item['nrOfSequences'])
        data_pattern.append(render_matrix(pattern))
        data_nr_of_stones.append(nr_of_stones)
        data_window_size.append(window_size)

df = pd.DataFrame({'strength' : data_strength,
                   'pattern' : data_pattern,
                   'frequency' : data_freq,
                   'nrOfStones' : data_nr_of_stones,
                   'nrOfGames' : data_nr_of_games,
                   'nrOfSequences' : data_nr_of_seqs})

print(df)

print("total time = " + str((time.time() - totalTime)/(60*60)) + 'h')


total_nr_games = df['nrOfGames'].sum()

filename = data_dir + 'freqs'
filename += '_patterns' + str(nr_of_patterns) 
filename += '_games' + str(total_nr_games) 
filename += '_ws' + str(window_size)
filename += '_stones' + str(nr_of_stones) 
filename += '_strengthHash' + str(strengthHash)
filename += '.csv'

df.to_csv(filename, index=False)

# User pattern
# pattern = ['_', '_', 'B',
#           '_', '_', 'B',
#           '_', '_', 'B']
# pattern = list(map(lambda p: Player(p), pattern))
    
