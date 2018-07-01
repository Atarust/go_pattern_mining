'''
Created on Jun 25, 2018

@author: jonas
'''

import time, os, re, random

import requests, zipfile, io

from src.config import games_dir, data_dir
from src.utils import read_file


years = range(2012, 2018)
months = range(1, 12)
users = ['guest1011', 'topspin', 'elch2']


def getRank(filename, user):
    content = read_file(filename)
    #get_main_variation(content)
    # is user black or white?
    mb = re.search('PB\[' + user + '\]', content)
    mw = re.search('PW\[' + user + '\]', content)
    is_black = False
    if mb:
        is_black = True
    elif mw:
        is_black = False
    else:
        return 'player not found'
    
    if is_black:    
        m = re.search('BR\[([^\]]*)\]', content)
        if m:
            return m.group(1)
    else:
        m = re.search('WR\[([^\]]*)\]', content)
        if m:
            return m.group(1)
    return 'unranked'

def getDate(filename, user):
    content = read_file(filename) 
    m = re.search('DT\[([^\]]*)\]', content)
    if m:
        return m.group(1)
    return 'date_unknown'

def get_main_variation(sgf_string):
    sgf_string = sgf_string.replace('\n', '')  # remove line break
    main_variation = re.search('\(([^\)]*)\)', sgf_string)
    if not main_variation:
        print('no main variation')
    main_variation = main_variation.group(1)
    print(main_variation)
    
    a = re.findall('\(', main_variation)
    m = main_variation
    i = m.index('(')
    
    
    #side_variations = re.search('\(([^\)]*)\)', main_variation)
    #for var in side_variations:
    #    main_variation = main_variation.replace('(' + var + ')', '')
        

def download():
    for user in users:
        for year in years:
            for month in months:        
                zip_file_url = 'https://www.gokgs.com/servlet/archives/en_US/' + user + '-all-' + str(year) + '-' + str(month) + '.zip'
                print(zip_file_url)
                try:
                    r = requests.get(zip_file_url)
                    print(r)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    z.extractall(path='./' + user)
                except:
                    print(zip_file_url)
                    print('error, LIFE GOES ON!!')
                time.sleep(60)
            
def rename():
    for user in users:
        for year in os.listdir(user + '/'): 
            for month in os.listdir(user + '/' + str(year) + '/'): 
                for day in os.listdir(user + '/' + str(year) + '/' + str(month) + '/'):
                    for sgf in os.listdir(user + '/' + str(year) + '/' + str(month) + '/' + day):
                        old = user + '/' + str(year) + '/' + str(month) + '/' + day + '/' + sgf
                        new = games_dir + user + '/' + str(year) + '_' + str(month) + '_' + day + '_' + sgf
                        os.rename(old, new) 

def leela_sgf_to_files():
    def getDateOfLeelaGame(game):
        m = re.search('DT\[([^\]]*)\]', game)
        if m:
            date = m.group(1)
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            return year, month, day
        print('no date found in sgf!')
        return '1969', '10', '05' # release date of monty python :)
        
    filename = games_dir + 'all_leela.sgf'
    content = read_file(filename)
    
    content = content.replace('\n', '')  # remove line break
    content_separated_into_games = re.findall('\(([^\)]*)\)', content)
    games = []
    for game in content_separated_into_games:
        games.append(game)
    
    for game in games:
        # sort into separate files with name 
        year, month, day = getDateOfLeelaGame(game)
        game_dir = games_dir + 'lz_' + year + '-' + month
        game_name = 'leela_' + year + '-' + month + '-' + day + '_' + str(random.randint(0,100000)) + '.sgf'
        
        if not os.path.exists(game_dir):
            os.makedirs(game_dir)
            
        f = open(game_dir + '/' + game_name,"w+")
        f.write('(' + game + ')')
        f.close()
        # TODO create file with filename
        

leela_sgf_to_files()
#rename()



#download()
#filename = 'guest1011/2013/1/27/guest1011.sgf'
#content = read_file(filename)
#get_main_variation(content)


