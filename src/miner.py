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
        -> normalize pattern, so that reflection, turning, mirror and color does not matter
        -> extract patterns from most occuring sequences - if you do it for all strengths, you could select randomly 10 pattern out of 100 most occuring patterns per strength.
@author: jonas

'''

from collections import Counter
import random

import pandas as pd
from src.config import window_size, data_dir, games_dir, max_games_per_strength, nr_of_patterns, nr_of_stones, strengths, estimatedTime, \
    estimatedTimeSetup, strengthHash, nr_of_sequences, nr_of_empty
from src.freq_analyzer import make_plot
from src.move import Player
from src.sequenceConverter import file_to_sgf, create_window_seq, find_all_patterns, to_matrix_string
from src.utils import open_files


def createSequences():
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
        
        sequences = list(map(lambda s:to_matrix_string(s), sequences))
        sequences = Counter(sequences)
        sequences = sequences.most_common(nr_of_sequences)
        seqs.append(sequences)
        nr_of_games.append(count_games)
        nr_of_seqs.append(count_seq)
    
    sequences = pd.DataFrame({'strength':strengths, 'sequence':seqs, 'nrOfGames':nr_of_games, 'nrOfSequences':nr_of_seqs})
    return sequences

def create_frequencies(patterns, sequences):
    data_strength = []
    data_pattern = []
    data_nr_of_stones = []
    data_window_size = []
    data_nr_of_games = []
    data_nr_of_seqs = []
    data_freq = []
    for _index, item in sequences.iterrows():
        for pattern in patterns:
            freq_of_pattern = sum(map(lambda pattern_freq:pattern_freq[1], find_all_patterns(pattern, item['sequence'])))
            data_freq.append(freq_of_pattern)
            data_strength.append(item['strength'])
            data_nr_of_games.append(item['nrOfGames'])
            data_nr_of_seqs.append(item['nrOfSequences'])
            data_pattern.append(pattern)
            data_nr_of_stones.append(nr_of_stones)
            data_window_size.append(window_size)
    
    df = pd.DataFrame({'strength':data_strength,
            'pattern':data_pattern,
            'frequency':data_freq,
            'nrOfStones':data_nr_of_stones,
            'nrOfGames':data_nr_of_games,
            'nrOfSequences':data_nr_of_seqs})
    return df


def gen_rand_pattern(size, nr_of_stones):
    nr_of_white = random.randint(0, nr_of_stones)
    nr_of_black = nr_of_stones - nr_of_white
    
    pattern = Player.w.value * nr_of_white
    pattern += Player.b.value * nr_of_black
    pattern += Player.empty.value * nr_of_empty
    pattern += Player.dontcare.value * (size * size - len(pattern))
    l = list(pattern)
    random.shuffle(l)
    return ''.join(l)

if __name__ == '__main__':
    print(str(estimatedTime) + " sec estimated.")
    print(str(estimatedTimeSetup) + " sec estimated for setup.")
    
    patterns = [gen_rand_pattern(window_size, nr_of_stones) for _p in range(nr_of_patterns)]
    sequences = createSequences()  
    df = create_frequencies(patterns, sequences)
    print(df)
    total_nr_games = df['nrOfGames'].sum()
    
    filename = 'freqs'
    filename += '_patterns' + str(nr_of_patterns) 
    filename += '_games' + str(total_nr_games) 
    filename += '_ws' + str(window_size)
    filename += '_stones' + str(nr_of_stones) 
    filename += '_strengthHash' + str(strengthHash)
    filename += '.csv'
    
    df.to_csv(data_dir + filename, index=False)
    make_plot(data_dir, data_dir + filename)
