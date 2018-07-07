'''
Created on Jun 24, 2018

@author: jonas
'''

window_size = 3
board_size = 19
max_nr_of_moves = 150
nr_of_stones = 3
nr_of_empty = 2
nr_of_patterns = 10000  # increases execution time linearly
nr_of_intermediates = 1000
max_games_per_strength = 10000  # is O(games*len(strengths)), but also adds time for set up
max_common_sequences = 1000000  # search most common max_common_sequences in the given files
min_freq = 10 #0.0001*max_games_per_strength# number of occurences in at least one strength
min_freq_change = 0.002
max_entries = 8
min_entries = 6
games_dir = "/home/jonas/Downloads/sgf_database/"
data_dir = "../data_output/"

append_prefix = True
append_only_one_point_in_time = True
strengths = ['18k', 'guest1011', 'topspin', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '1p', '2p', '9p']
strengths = ['18k', 'guest1011', '1k', 'topspin','1p', '9p']
strengths = ['lz_m_2017-12','lz_m_2018-01','lz_m_2018-02','lz_m_2018-03','lz_m_2018-04','lz_m_2018-05','lz_m_2018-06']

#strengths = ['18k', '9p']
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
    return h * h * h * h


strengthHash = sum(map(lambda s : int(deterministic_hash(s)), strengths))

