import requests
from html.parser import HTMLParser
import re
import fnmatch
import urllib.request
import shutil

# Useful regular expressions to read the HTML. This can definitely be improved
regex = re.compile('<a href=\"/game.*?\">')
regexGenre = re.compile('<a href=\"/genre.*?\">.*</a>')
regex2 = re.compile('.*\"/')

game_list = []

text_file = open('games3.txt','w')

fromTextFile = 0

if fromTextFile ==1:
        try:
                for j in range(0,5325,25):
                        mobyURL = 'http://www.mobygames.com/browse/games/ps3/offset,' + str(j) + '/so,0a/list-games/'
                        r = requests.get(mobyURL)
                        i = 0
                        for line in r.iter_lines():
                                i += 1
                                #Specify which lines in the HTML code to read - can be made obselete
                                lower_lim = 145
                                upper_lim = 170
                                if j == 5300:
                                        upper_lim = 159
                                
                                if i in range(lower_lim,upper_lim):
                                        #Parse the strings and remove DLC
                                        gameURL = re.findall(regex,line.decode('utf-8'))
                                        gameURL = ''.join(map(str,gameURL))
                                        gameURL = gameURL[9:len(gameURL)-2]
                                        gameGENRE = re.findall(regexGenre,line.decode('utf-8'))
                                        gameGENRE = ''.join(map(str,gameGENRE))
                                        if ('DLC' not in gameGENRE) and ('Compilation' not in gameGENRE):
                                                print(gameURL)
                                                game_list.append(gameURL)
                                                text_file.write(gameURL+'\n')
        finally:
                text_file.close()

filename = open('games2.txt')
game_list = [i for i in filename.readlines()]

#All games should be written to a text file. Now we can iterate over each game and grab the art and metacritic score
#This code needs to be improved considerably.
regex = re.compile('>.*<')
regCover = re.compile('\/images.*.jpg')
game = 1
for item in game_list:
        game_url = 'http://www.mobygames.com' + item
        r = requests.get(game_url)

        i = 0
        for line in r.iter_lines():
                i += 1
                if i == 124:
                        #Get cover art
                        cover_url = re.findall(regCover,line.decode('utf-8'))
                        cover_url = ''.join(map(str,cover_url))
                        cover_url = cover_url.replace('"','')
                        cover_url = 'http://www.mobygames.com' + cover_url
                        print(cover_url)
                        
                if i == 131:
                        score = re.findall(regex,line.decode('utf-8'))
                        score = ''.join(map(str,score))
                        score = score.replace('<','')
                        score = score.replace('>','')
                        score = score.replace('...','')
                        #print('_'+score+'_')
                        try:
                                if score != '':
                                        rpic = requests.get(cover_url, stream=True)
                                        if rpic.status_code == 200:
                                                with open('gameCovers/' + 'game_' + str(game) + '_' + score + '.jpg','wb') as f:
                                                        rpic.raw.decode_content = True
                                                        shutil.copyfileobj(rpic.raw,f)
                                                        game +=1
                        except:
                                print('something messed up')


