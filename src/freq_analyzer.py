'''
Created on Jun 24, 2018

@author: jonas
'''

import os

import matplotlib.pyplot as plt
import pandas as pd
from src.config import window_size, data_dir, min_freq, \
    nr_of_empty, nr_of_stones


def preprocess_data(sequences):
    sequences = sequences = sequences[sequences['pattern'] != '?' * (window_size * window_size)]
    sequences = remove_infrequent_patterns(sequences)
    sequences = remove_non_changing_patterns(sequences)
    return sequences

def make_plot(data_dir, filename):
    sequences = pd.read_csv(filename, index_col=False)
    sequences = sequences[sequences['pattern'] != '?' *(window_size*window_size)]
    plt.show()
    sequences = preprocess_data(sequences)
    if len(sequences) == 0:
        return
    sequences['nr_of_wildcards'] = sequences.apply(lambda row: row['pattern'].count('?'), axis=1)
    
    sequences = sequences[sequences['nr_of_wildcards'] == (window_size*window_size - nr_of_stones - nr_of_empty)]
    for nr_wild in sequences['nr_of_wildcards'].unique():
        s = sequences[sequences['nr_of_wildcards'] == nr_wild]
        s.hist(bins=10)
        ax = plt.gca()
        for pattern in s['pattern'].unique():
            if len(s[s['pattern'] == pattern]) != 0:
                s[s['pattern'] == pattern].plot(x='strength', y='freq_ratio', ax=ax)
        
        plt.title('frequency per sequence')
        plt.legend(sequences['pattern'].unique().tolist())
        #plt.show()
    

        filename = filename.split('/')[-1]
        filename = filename.split('.')[-2]
        #plt.savefig(data_dir + "plot/" + filename + ".png")
        plt.show()

def make_all_plots():
    data_dir = "../data_output/"
    for file in os.listdir(data_dir):
            if file.startswith("freqs_"):
                filename = os.path.join(data_dir, file)
                
                make_plot(data_dir, filename)

def row_should_be_removed(remove_patterns, row):
    return not remove_patterns.count(row['pattern']) > 0

def remove_infrequent_patterns(sequences):
    # a pattern is not interesting, if it is not frequent in at least one strength
    remove_patterns = []
    for pattern  in sequences['pattern'].unique():
        s = sequences[sequences['pattern'] == pattern]
        highest_freq = s['frequency'].max()
        if highest_freq < min_freq:
            remove_patterns.append(pattern)
    
    new_s = sequences
    for p in remove_patterns:
        new_s = new_s[new_s['pattern'] != p]
    return new_s

def remove_non_changing_patterns(sequences):
    new_s = sequences
    pattern_diffs = []
    for pattern  in sequences['pattern'].unique():
        s = new_s[new_s['pattern'] == pattern]
        diff = s['freq_ratio'].max() - s['freq_ratio'].min()
        pattern_diffs.append((pattern, diff))
    # sort, highest diff first
    pattern_diffs.sort(key=lambda p_d: p_d[1])

    # remove all patterns that are not in top ten. TODO refactor!!    
    for p_d in pattern_diffs[10:]:
        new_s = new_s[new_s['pattern'] != p_d[0]]
    return new_s


if __name__ == '__main__':
    file = 'freqs_patterns10000_games10846578.0_ws3_stones4_strengthHash687526298596_striped.csv'
    #make_plot(data_dir, file)
    
    make_all_plots()
