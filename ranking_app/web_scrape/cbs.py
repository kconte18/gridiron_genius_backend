import requests
import pandas as pd
from bs4 import BeautifulSoup

from ranking_app.models import Player
from ranking_app import helpers

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
        raw_df = pd.DataFrame(ranking_data)

        # Player names to id
        raw_df_list = raw_df.values.tolist()
        players_dict = Player.objects.all().values()
        sorted_players_dict = sorted(players_dict, key=lambda x: x['player_name'])
        df_list = []
        for item in raw_df_list:
            player_id = helpers.binary_search_for_player(sorted_players_dict, 0, len(players_dict)-1, item[0])
            df_list_item = {'player_id': player_id, 'rank':item[1]}
            df_list.append(df_list_item)
        source['df_list'] = df_list
    return sources