import requests
import pandas as pd
from bs4 import BeautifulSoup

from ..data import rankings_sources
from .. import helpers

sources = rankings_sources.fftoday_sources

def web_scrape(players_dict):
    for source in sources:
        r = requests.get(source['url'])
        soup = BeautifulSoup(r.content, 'html5lib')

        s_list = soup.find_all('td', class_='smallbody', align='LEFT')
        s_list = s_list[0:100]
        player_list = []
        rank_list = []
        rank_num = 1
        for s in s_list:
            player_list.append(s.text.strip())
            rank_list.append(rank_num)
            rank_num = rank_num + 1

        ranking_data = {'player_name':player_list, 'rank':rank_list}
        raw_df = pd.DataFrame(ranking_data)

        source['df_list'] = helpers.swap_name_with_id(raw_df, players_dict)
    return sources
