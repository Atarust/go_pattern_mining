'''
Created on Jun 24, 2018

@author: jonas
'''
import os

import matplotlib.pyplot as plt
import pandas as pd


def drawLineGraph(data, x='strength', y='freq_ratio', filename=""):
    ax = plt.gca()
    # data = data.groupby(['runTime', 'commRange'], as_index=False).mean()
    
    # with and without communication
    # data[data['commRange'] > 100].plot(x=x, y=y, ax=ax)
    data.plot(x=x, y=y, ax=ax)
    # data.plot(x='strength', y='frequency', ax=ax)
    #ax.legend(['l1'])
    plt.title(y)
    plt.savefig(data_dir + "plot/" + filename + ".png")
    plt.show()


data_dir = "../data_output/"
for file in os.listdir(data_dir):
        if file.startswith("freqs_"):
            filename = os.path.join(data_dir, file)
            
            df = pd.read_csv(filename, index_col=False)
            df['freq_ratio'] = df['frequency']/df['nrOfSequences']
            
            for pattern in df['pattern'].unique():
                d = df[df['pattern'] == pattern]
                
                ax = plt.gca()
                
                d.plot(x='strength', y='freq_ratio', ax=ax)
                
            ax.legend(df['pattern'].unique())
            plt.title('frequency per sequence')
            
            # Make name a bit 
            filename = filename.split('/')[-1]
            filename = filename.split('.')[-2]
            
            plt.savefig(data_dir + "plot/" + filename + ".png")
            plt.show()

