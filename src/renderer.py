'''
Created on Jun 24, 2018

@author: jonas
'''
from src.config import window_size
        
def render_matrix(matrix):
    string = ""
    i = 0
    for m in matrix:
        string += m
        i += 1
        if(i % window_size == 0):
            string += "\n"
    return string

