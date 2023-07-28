import re
import json
import requests
import pandas as pd

from .. import helpers
from ..data import rankings_sources

sources = rankings_sources.fantasypros_sources

def web_scrape(players_dict):
    for source in sources:    
        text = requests.get(source['url']).text
        data = re.search(r'ecrData = (.*);', text).group(1)
        data = json.loads(data)

        raw_df = pd.DataFrame(data['players'])

        column_list = raw_df.columns.tolist()
        column_list.remove("player_name")
        column_list.remove("rank_ecr")
        # column_list.remove("player_positions")
        # column_list.remove("player_team_id")

        # Drop all columns EXCEPT: player_name, player_positions, player_team_id, player_bye_week, rank_ecr
        raw_df = raw_df.drop(columns=column_list)
        raw_df = raw_df.rename(columns={"rank_ecr":"rank"})
        raw_df = raw_df.iloc[lambda x: x.index < 100]

        # Player names to id
        source['df_list'] = helpers.swap_name_with_id(raw_df, players_dict)
    return sources