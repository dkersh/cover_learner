# Scrub metacritic for games
import requests
import re
import shutil
import time

def makeGameList():
    text_file = open('meta1.txt','w')

    for i in range(0,16):
        url = 'http://www.metacritic.com/browse/games/release-date/available/ps3/date?view=condensed&page=' + str(i)
        r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
        
        games = re.findall('<a href=\"/game/playstation-3/.*\">',r.text)

        for item in games:
            item = item.replace('<a href="','')
            item = item.replace('">','')
            print(item)
            text_file.write(item)
            text_file.write('\n')

    text_file.close()

def getScore(r):
    regScore = re.compile('<div class=\"metascore_w xlarge .*\"ratingValue\">\d\d<.*>')
    score = re.findall(regScore,r.text)
    score = ''.join(map(str,score))
    score = re.search('>\d\d<',score)
    try:
        score = score.group(0)
        score = ''.join(map(str,score))
        score = score.replace('>','')
        score = score.replace('<','')
    except:
        score = None

    return score

def getCover(r):
    regCover = re.compile('og:image\".*>')
    cover = re.findall(regCover,r.text)
    cover = ''.join(map(str,cover))
    cover = cover.replace('og:image" content="','')
    cover = cover.replace('">','')

    return cover

def downloadCover(url,i,score):
    rpic = requests.get(url, stream=True)
    if rpic.status_code == 200:
        with open('metaCovers/' + 'game_' + str(i) + '_' + str(score) + '.jpg','wb') as f:
            rpic.raw.decode_content = True
            shutil.copyfileobj(rpic.raw,f)

filename = open('meta1.txt')
text_file = open('meta_good.txt','w')
game_list = [i for i in filename.readlines()]

try:
    for i in range(0,len(game_list)):
        progress = str(i+1) + '/' + str(len(game_list)) + ' - '
        URL = 'http://www.metacritic.com/' + game_list[i]
        r = requests.get(URL,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

        score = getScore(r)
        cover = getCover(r)

        if not score or not cover:
            print(progress + 'bad game' + ' ' + game_list[i])
        else:
            print(progress + score + ' ' + game_list[i])
            score = round(int(score)/10)
            text_file.write(game_list[i])
            downloadCover(cover,i,score)
finally:
    text_file.close()
