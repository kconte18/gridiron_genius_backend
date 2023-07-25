import re
import json
import requests
import pandas as pd

from ranking_app.models import Player
from .. import helpers

sources = [{ 'url': 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php', 'ppr': 0 }, { 'url':'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php', 'ppr': 1 }]

def web_scrape():
    for source in sources:    
        text = requests.get(source['url']).text
        data = re.search(r'ecrData = (.*);', text).group(1)
        data = json.loads(data)

        raw_df = pd.DataFrame(data['players'])

        column_list = raw_df.columns.tolist()
        column_list.remove("player_name")
        column_list.remove("rank_ecr")

        # Drop all columns EXCEPT: player_name, player_positions, player_team_id, player_bye_week, rank_ecr
        raw_df = raw_df.drop(columns=column_list)
        raw_df = raw_df.rename(columns={"rank_ecr":"rank"})
        raw_df = raw_df.iloc[lambda x: x.index < 100]

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