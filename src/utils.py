'''
Created on Jun 24, 2018

@author: jonas
'''

import codecs
import os
import random


def open_files(sgf_dir, max_games_per_strength):   
    files_content = [] 
    list_files = os.listdir(sgf_dir)
    list_files = random.sample(list_files, min(max_games_per_strength, len(list_files)))
    for file in list_files:
        sgf_string = ''
        if file.endswith(".sgf"):
            filename = os.path.join(sgf_dir, file)
            
            f = codecs.open(filename, encoding='utf-8', errors="ignore")
            for line in f:
                sgf_string += line
        sgf_string = sgf_string.replace('\n', '')
        files_content.append(sgf_string)
    return files_content

def read_file(filename):
    if not filename.endswith(".sgf"):
        print('not sgf')
        return
    
    files_content = ''
    f = codecs.open(filename, encoding='utf-8', errors="ignore")
    for line in f:
        files_content += line
    return files_content
    
    
    