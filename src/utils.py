'''
Created on Jun 24, 2018

@author: jonas
'''

import codecs
import os


def open_files(sgf_dir):   
    files_content = [] 
    for file in os.listdir(sgf_dir):
        if file.endswith(".sgf"):
            filename = os.path.join(sgf_dir, file)
            
            f = codecs.open(filename, encoding='utf-8', errors="ignore")
            for line in f:
                files_content.append(repr(line))
            
            # with open(filename, 'r') as myfile:
            #    data = myfile.read()
    return files_content
