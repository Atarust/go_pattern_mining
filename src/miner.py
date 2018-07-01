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
        -> postprocessing: reduce number of patterns by finding meaningful patterns - those with a min occurence in at least one strength and who have a min variance (max_occ_per_strength - min_occ_strength)
@author: jonas

'''

from collections import Counter
import random

import pandas as pd
from src import pattern_tree
from src.config import window_size, data_dir, games_dir, max_games_per_strength, nr_of_patterns, nr_of_stones, strengths, estimatedTime, \
    estimatedTimeSetup, strengthHash, nr_of_empty, max_common_sequences, \
    nr_of_intermediates
from src.freq_analyzer import make_plot
from src.move import Player
from src.pattern_tree import PatternTree
from src.sequenceConverter import file_to_sgf, create_window_seq, to_matrix_string
from src.utils import open_files

def createSequences():
    seqs_strength = []
    nr_of_games = []
    nr_of_seqs = []
    for strength in strengths:
        sgf_dir = games_dir + strength
        files_content = open_files(sgf_dir, max_games_per_strength)
        count_games = 0
        sequences = []
        for content in files_content:
            g = file_to_sgf(content)
            s = create_window_seq(g)
            sequences += s
            count_games += 1
        sequences = list(map(lambda s:to_matrix_string(s), sequences))
        sequences = Counter(sequences)
        sequences = sequences.most_common(max_common_sequences)
        seqs_strength.append(sequences)
        nr_of_games.append(count_games)
        count_sequences = 0
        for seq_freq in sequences:
            count_sequences += seq_freq[1]
        nr_of_seqs.append(count_sequences)
    
    sequences = pd.DataFrame({'strength':strengths, 'sequence':seqs_strength, 'nrOfGames':nr_of_games, 'nrOfSequences':nr_of_seqs})
    return sequences


def create_frequencies(sequences):

    # sort frequencies into PatternTrees
    sequences.apply(lambda row: insert_in_tree(row['PatternTree'], row['strength']), axis=1)
    patterns = sequences['PatternTree'].iloc[0].get_patterns()
    
    def get_freq(sequences, pattern, strength):
        s = sequences[sequences['strength'] == strength]['PatternTree'].iloc[0]
        # TODO what if there is a strength multiple times? -> Ignore!
        return s.get_frequency_of_pattern(pattern)
    
    pattern_data = []
    freq_data = []
    strength_data = []
    nr_games_data = []
    nr_sequences_data = []
    for pattern in patterns:
        for strength in strengths:
            freq = get_freq(sequences, pattern, strength)
            freq_data.append(freq)
            strength_data.append(strength)
            pattern_data.append(pattern)
            nr_games_data.append(sequences[sequences['strength']==strength]['nrOfGames'].mean())
            nr_sequences_data.append(sequences[sequences['strength']==strength]['nrOfSequences'].mean())


    df = pd.DataFrame({'pattern':pattern_data, 'strength':strength_data,'nrOfGames':nr_games_data, 'nrOfSequences':nr_sequences_data, 'frequency':freq_data})
    df['nrOfStones'] = nr_of_stones
    df['window_size'] = window_size

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

def create_pattern_tree(patterns):
    root = pattern_tree.get_root()
    for pattern in patterns:
        root.insert_patternTree(PatternTree(pattern))
    return root

def insert_in_tree(pattern_tree, strength):
    for _index, seq_per_strength  in sequences[sequences['strength'] == strength].iterrows():
        for seq_counted in seq_per_strength['sequence']:
            pattern_tree.insert_sequence_counted(seq_counted)

if __name__ == '__main__':
    print('nr_of_patterns:'  + str(nr_of_patterns) + ', ' + 'max_games_per_strength:' + str(max_games_per_strength))
    
    patterns = [gen_rand_pattern(window_size, nr_of_stones) for _p in range(nr_of_patterns)]
    # create some intermediate patterns
    for intermediate in range(nr_of_intermediates):
        stones = random.randint(1,nr_of_stones)
        patterns.append(gen_rand_pattern(window_size, stones))
    
    sequences = createSequences()  
    sequences['nrOfStones'] = nr_of_stones
    sequences['window_size'] = window_size
    # create trees with patterns
    sequences['PatternTree'] = pd.Series([create_pattern_tree(patterns) for s in sequences.count()])
    
    sequences = create_frequencies(sequences)
    sequences['freq_ratio'] = sequences['frequency'] / sequences['nrOfSequences']
    total_nr_games = sequences['nrOfGames'].sum()
    
    filename = 'freqs'
    filename += '_patterns' + str(nr_of_patterns) 
    filename += '_games' + str(total_nr_games) 
    filename += '_ws' + str(window_size)
    filename += '_stones' + str(nr_of_stones) 
    filename += '_strengthHash' + str(strengthHash)
    filename += '.csv'
    
    print(sequences)
    sequences.to_csv(data_dir + filename, index=False)
    make_plot(data_dir, data_dir + filename)
