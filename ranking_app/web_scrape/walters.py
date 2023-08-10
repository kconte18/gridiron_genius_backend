import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

from ..data import rankings_sources
from ranking_app import helpers

sources = rankings_sources.walters_sources

def web_scrape(players_dict):
    for source in sources:
        r = requests.get(source['url'])
        soup = BeautifulSoup(r.content, 'html.parser')
        soup_li = soup.find_all('li', class_='player')
        players_spans = []
        for li in soup_li:
            spans = li.find_all('span')
            players_spans.append(spans[1])
        players = []
        rank_num = 1
        for player_span in players_spans:
            # MUST CHECK POSITION FROM SPAN DUE TO WEBSITE NOT HAVING SEPARATE URLS BY POSITION
            if source['position_ranking_type'] != 'OVERALL':
                if re.search(str(source['position_ranking_type']), str(player_span)) == None:
                    continue
            player_span = re.sub('<span>', '', str(player_span))
            player_name = re.sub(r'[,].*', '', player_span)
            player = {
                'player_name': player_name,
                'rank': rank_num
            }
            rank_num+=1
            players.append(player)

        df = pd.DataFrame(players)
        if(source['position_ranking_type'] == 'OVERALL'):
            df = df.iloc[lambda x: x.index < 100]
        elif(source['position_ranking_type'] == 'QB'):
            df = df.iloc[lambda x: x.index < 32]
        elif(source['position_ranking_type'] == 'RB'):
            df = df.iloc[lambda x: x.index < 50]
        elif(source['position_ranking_type'] == 'WR'):
            df = df.iloc[lambda x: x.index < 50]
        elif(source['position_ranking_type'] == 'TE'):
            df = df.iloc[lambda x: x.index < 35]
        
        source['df_list'] = helpers.swap_name_with_id(df, players_dict)
    return sources  