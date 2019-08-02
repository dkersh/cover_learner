import requests
import re
import shutil
import time
import urllib
import urllib.request
from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed
CPU_CORES = multiprocessing.cpu_count()
print('CPU CORES: ' + str(CPU_CORES))

def findGames():    
    platforms = ['ps3','xbox360','ps4','xbone']
    gamelist_file = open('gamelist.txt','w')
    scorelist_file = open('scorelist.txt','w')
    try:
        for system in platforms:
            print(system)
            if system == 'ps3':
                baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps3/date?view=condensed&page='
                reg = '<a href=\"/game/playstation-3/.*\">'
                indices = range(0,16)
            elif system == 'xbox360':
                baseURL = 'http://www.metacritic.com/browse/games/release-date/available/xbox360/date?view=condensed&page='
                reg = '<a href=\"/game/xbox-360/.*\">'
                indices = range(0,15)
            elif system == 'ps2':
                baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps2/date?view=condensed&page='
                reg = '<a href=\"/game/playstation-2/.*\">'
            elif system == 'ps4':
                baseURL = 'http://www.metacritic.com/browse/games/release-date/available/ps4/date?view=condensed&page='
                reg = ' <a href=\"/game/playstation-4/.*\">'
                indices = range(0,22)
            elif system == 'xbone':
                baseURL = 'http://www.metacritic.com/browse/games/release-date/available/xboxone/date?view=condensed&page='
                reg = ' <a href=\"/game/xbox-one/.*\">'
                indices = range(0,17)

            reg_score = '<div class=\"metascore.*\">.*</div>'

            #Get URL source
            for pagenum in indices:
                url = baseURL + str(pagenum)
                r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
                games = re.findall(reg,r.text)
                scores = re.findall(reg_score,r.text)

                #Remove trailers
                games = [x for x in games if "trailers" not in x]

                #Scrub scores
                for j in range(len(scores)):
                    scores[j] = re.findall('\d+',scores[j])

                print('Page: ' + str(pagenum) + ' - ' + str(len(games)) + '(' + str(len(scores)) + ')')
                for j in range(len(games)):
                    games[j] = games[j].replace('<a href=\"','')
                    games[j] = games[j].replace('\">','')
                    games[j] = games[j].strip()

                    if len(scores[j])>0:
                        #write to file
                        gamelist_file.write(games[j]+'\n')
                        sco = ''.join(scores[j])
                        scorelist_file.write(sco + '\n')
    finally:
        gamelist_file.close()
        scorelist_file.close()
        
findGames()

with open('gamelist.txt') as f:
    games = f.read().splitlines()
    
with open('scorelist.txt') as f:
    scores = f.read().splitlines()
    
full_urls = []
covernames = []
for i in range(len(games)):
    num = "%04d" %(i+1)
    full_urls.append('https://www.metacritic.com' + games[i])
    covernames.append('covers/game' + num + '_' + str(scores[i]) + '.jpg')
      
def get_cover(url,covername):
    try:
        r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        #r = requests.get(url,stream=True)
        imgfile = re.findall('<meta property=\"og:image\" content=\".*\">',r.text)
        imgfile = ''.join(imgfile)
        imgfile = imgfile.replace('<meta property=\"og:image\" content=\"','')
        imgfile = imgfile.replace('\">','')

        #return imgfile

        urllib.request.urlretrieve(imgfile,covername)
    except:
        print('error')

#for i in range(len(full_urls)):
#    print(covernames[i])
#    get_cover(full_urls[i],covernames[i])
    
Parallel(n_jobs=4)(delayed(get_cover)(full_urls[i],covernames[i]) for i in tqdm(range(len(full_urls))))
