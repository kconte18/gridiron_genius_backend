import requests
import pandas as pd
from bs4 import BeautifulSoup

sources = [{'url':'https://www.cbssports.com/fantasy/football/rankings/', 'ppr':1}, {'url':'https://www.cbssports.com/fantasy/football/rankings/standard/top200/', 'ppr':0}]

def web_scrape():    
    for source in sources:
        r = requests.get(source['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='experts-column')
        players = s.find_all('span', class_='player-name')
        rank_num = 1
        player_name_list = []
        rank_list = []
        for player in players:
            player_name_list.append(player.text)
            rank_list.append(rank_num)
            rank_num= rank_num + 1
            if(rank_num == 101):
                break
        ranking_data = {'player_name':player_name_list, 'rank':rank_list}
        df = pd.DataFrame(ranking_data)
        source['df'] = df
    return sources