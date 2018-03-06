import requests
import re
import shutil

def getScore(r):
    regScore = re.compile('<div class=\"fr scoreBoxBig .*\">.*</div>')

    score = re.findall(regScore,r.text)
    score = ''.join(map(str,score))
    score = re.findall('\d\d',score)
    score = ''.join(map(str,score))

    return score

def getCover(r):
    regCover = re.compile('src=\"/images/covers/s/.*\.jpg\"')

    cover = re.findall(regCover,r.text)
    cover = ''.join(map(str,cover))
    cover = re.findall('/.*\.jpg',cover)
    cover = ''.join(map(str,cover))

    return cover

def downloadCover(url,i,score):
    rpic = requests.get(url, stream=True)
    if rpic.status_code == 200:
        with open('gameCovers2/' + 'game_' + str(i) + '_' + str(score) + '.jpg','wb') as f:
            rpic.raw.decode_content = True
            shutil.copyfileobj(rpic.raw,f)

filename = open('games2.txt')
game_list = [i for i in filename.readlines()]

text_file = open('games_good2.txt','w')

for i in range(0,len(game_list)):
    URL = 'http://www.mobygames.com' + game_list[i]

    r = requests.get(URL)
    score = getScore(r)
    cover = getCover(r)
    if not score or not cover:
        print('bad game')
    else:
        #It'll be easier if the scoring scale is smaller
        score = round(int(score)/10)
        text_file.write(game_list[i]+'\n')
        print(str(i) + ':' + str(score) + ' ' + cover)
        downloadCover('http://www.mobygames.com' + cover,i,score)

text_file.close()
        
        
