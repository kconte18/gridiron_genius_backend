import requests
import pandas as pd
from bs4 import BeautifulSoup

from ranking_app.models import Player
from ranking_app import helpers

sources = [{'url':'https://www.cbssports.com/fantasy/football/rankings/', 'scoring_type': 'PPR', 'position_ranking_type': 'OVERALL'}, {'url':'https://www.cbssports.com/fantasy/football/rankings/standard/top200/', 'scoring_type': 'STANDARD', 'position_ranking_type': 'OVERALL'}]

def web_scrape(players_dict):    
    for source in sources:
        r = requests.get(source['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('div', class_='experts-column')
        players = s.find_all('span', class_='player-name')
        print(players)
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
        raw_df = pd.DataFrame(ranking_data)

        # Player names to id
        source['df_list'] = helpers.swap_name_with_id(raw_df, players_dict)
    return sources