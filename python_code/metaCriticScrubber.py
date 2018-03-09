# Scrub metacritic for games
import requests
import re
import shutil
import time

# Create a textfile which contains all the games from a specific platform.
def makeGameList(platform,filename):
    text_file = open(filename,'w')

    if platform == 'ps3':
        baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps3/date?view=condensed&page='
        reg = '<a href=\"/game/playstation-3/.*\">'
    elif platform == 'xbox360':
        baseURL = 'http://www.metacritic.com/browse/games/release-date/available/xbox360/date?view=condensed&page='
        reg = '<a href=\"/game/xbox-360/.*\">'
    elif platform == 'ps2':
        baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps2/date?view=condensed&page='
        reg = '<a href=\"/game/playstation-2/.*\">'
    elif platform == 'ps4':
        baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps4/date?view=condensed&page='
        reg = ' <a href=\"/game/playstation-4/.*\">'
    elif platform == 'xbone':
        baseURL = 'http://www.metacritic.com/browse/games/release-date/available/xboxone/date?view=condensed&page='
        reg = ' <a href=\"/game/xbox-one/.*\">'
        
    reg_score = '<div class=\"metascore.*\">.*</div>'
    
    try:
        for i in range(0,16):
            url = baseURL + str(i)
            r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
            
            games = re.findall(reg,r.text)
            scores = re.findall(reg_score,r.text)

            for i in range(0,len(games)):
                games[i] = games[i].replace(' <a href="','')
                games[i] = games[i].replace('">','')
                games[i] = games[i].replace(' ','')
                scores[i] = re.sub('<.*\">','',scores[i])
                scores[i] = re.sub('</div>','',scores[i])
                
                #Filter games with no scores
                if scores[i] == 'tbd':
                    print('BAD ' + games[i])
                else:
                    print('GOOD ' + games[i])
                    text_file.write(games[i]+'\n')

    finally:
        text_file.close()

def combineGameList(filenames):
    with open('allGames.txt','w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                  for line in infile:
                      outfile.write(line)

    #remove duplicates
    #This code is a complete mess and could be improved considerably
    textfile = open('allGames.txt','r')
    x_orig = textfile.read().splitlines()
    textfile.close()
    x = x_orig

    for i in range(0,len(x)):
        x[i] = x[i].replace('/game/xbox-360/','')
        x[i] = x[i].replace('/game/playstation-3/','')
        x[i] = x[i].replace('/game/playstation-2/','')
        x[i] = x[i].replace('/game/playstation-4/','')
        x[i] = x[i].replace('/game/xbox-one/','')
        
    x = list(set(x))

    textfile = open('allGames.txt','r')
    x_orig = textfile.read().splitlines()
    textfile.close()

    final_x = []

    for i in range(0,len(x)):
        for j in range(0,len(x_orig)):
            if x[i] in x_orig[j]:
                final_x.append(x_orig[j])
                break

    with open('allUniqueGames.txt','w') as outfile:
        for item in final_x:
            outfile.write(item+'\n')

# with a requests.get object, obtain the score from a metacritic game website.
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

def getGenre(r):
    regGenre = re.compile('<span class=\"label\">Genre\(s\)\: </span><span class="data" itemprop="genre">.*</span>')
    genre = re.findall(regGenre,r.text)
    genre = ''.join(map(str,genre))
    genre = re.sub('<span class=\"label\">Genre\(s\)\: </span><span class="data" itemprop="genre">','',genre)
    genre = re.sub('</span>.*','',genre)

    return genre

# with a requests.get object, obtain the cover link from a metacritic game website.
def getCover(r):
    regCover = re.compile('og:image\".*>')
    cover = re.findall(regCover,r.text)
    cover = ''.join(map(str,cover))
    cover = cover.replace('og:image" content="','')
    cover = cover.replace('">','')

    return cover

# Download cover artwork
def downloadCover(url,i,score):
    rpic = requests.get(url, stream=True)
    if rpic.status_code == 200:
        with open('metaCoversTest/' + 'game_' + str(i) + '_' + str(score) + '.jpg','wb') as f:
            rpic.raw.decode_content = True
            shutil.copyfileobj(rpic.raw,f)

# With a list of games, download the cover artwork and critic score from metacritic. Ignore games without scores.
def collect(gamelist):
    filename = open(gamelist)
    game_list = [i for i in filename.readlines()]
    score_file = open('metaCoversTest/scores.txt','w')
    genre_file = open('metaCoversTest/genre.txt','w')
    all_file = open('metaCoversTest/all.txt','w')

    try:
        for i in range(0,len(game_list)):
            progress = str(i+1) + '/' + str(len(game_list)) + ' - '
            URL = 'http://www.metacritic.com' + game_list[i]
            r = requests.get(URL,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

            score = getScore(r)
            cover = getCover(r)
            genre = getGenre(r)

            score_file.write(score + '\n')
            genre_file.write(genre + '\n')
            all_file.write(game_list[i] + ',' + score + ',' + genre)

            print(progress + game_list[i].replace('\n','') + ',' + score + ',' + genre)
            score = round(int(score)/10)
            downloadCover(cover,i,score)
            
    finally:
        score_file.close()
        genre_file.close()
        all_file.close()

#makeGameList('ps2','ps2Good.txt')
#makeGameList('ps3','ps3Good.txt')
#makeGameList('ps4','ps4Good.txt')
#makeGameList('xbone','xboneGood.txt')
#makeGameList('xbox360','xbox360Good.txt')
#combineGameList(['ps3Good.txt','ps2Good.txt','ps4Good.txt','xboneGood.txt','xbox360Good.txt'])
collect('allUniqueGames.txt')
