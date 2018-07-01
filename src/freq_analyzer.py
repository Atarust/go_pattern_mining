'''
Created on Jun 24, 2018

@author: jonas
'''

import os

import matplotlib.pyplot as plt
import pandas as pd
from src.config import window_size, data_dir
from src.miner import remove_infrequent_patterns, remove_non_changing_patterns


def preprocess_data(sequences):
    sequences = sequences = sequences[sequences['pattern'] != '?' * (window_size * window_size)]
    sequences = remove_infrequent_patterns(sequences)
    sequences = remove_non_changing_patterns(sequences)
    
def make_plot(data_dir, filename):
    ax = plt.gca()
    sequences = pd.read_csv(filename, index_col=False)
    preprocess_data(sequences)
    for pattern in sequences['pattern'].unique():
        if pattern != '?' *(window_size*window_size): # TODO refactor
            sequences[sequences['pattern'] == pattern].plot(x='strength', y='freq_ratio', ax=ax)
    
    plt.title('frequency per sequence')
    plt.legend(sequences['pattern'].unique().tolist())
    

    filename = filename.split('/')[-1]
    filename = filename.split('.')[-2]
    plt.savefig(data_dir + "plot/" + filename + ".png")
    plt.show()

def make_all_plots():
    data_dir = "../data_output/"
    for file in os.listdir(data_dir):
            if file.startswith("freqs_"):
                filename = os.path.join(data_dir, file)
                
                make_plot(data_dir, filename)

if __name__ == '__main__':
    file = 'freqs_patterns10000_games10846578.0_ws3_stones4_strengthHash687526298596_striped.csv'
    make_plot(data_dir, file)
    
    #make_all_plots()
