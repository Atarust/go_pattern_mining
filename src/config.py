'''
Created on Jun 24, 2018

@author: jonas
'''

window_size = 3
board_size = 19
nr_of_stones = 4
nr_of_patterns = 2 # increases execution time linearly
max_games_per_strength = 2  # is O(games*len(strengths)), but also adds time for set up
games_dir = "/home/jonas/Downloads/sgf_database/"
data_dir = "../data_output/"

append_prefix = True
strengths = ['18k','1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p']
strengths = ['18k','1p']
# execution time: t = setupTime*(games*strengths) + matchTime*patterns*(games*strengths)

# 61.75 sec = 5.168 + 56.58
# 5.168 = setupTime*(10*9), 56.58=matchTime*10*(10*9)
# -> setupTime = 0.0574, match=0.0628

# 40.439 sec = 15.21 + 25.22
# 15.21 sec = setupTime*(50*9), 25.22 = matchTime*1*(50*9)
# -> setupTime =0.0338 , match=0.056

#  588.47 sec = 25.7 + 562.77
#  25.7 sec = setupTime*(100*9), 562.77  = matchTime*10*(100*9)
setupTime = 0.02
matchTime = 0.07
estimatedTimeSetup = setupTime * max_games_per_strength * len(strengths)
estimatedTime = estimatedTimeSetup + matchTime * nr_of_patterns * max_games_per_strength * len(strengths)

def deterministic_hash(string):
    h = sum(map(lambda char : ord(char), string))
    return h*h*h*h

strengthHash = sum(map(lambda s : int(deterministic_hash(s)), strengths))



