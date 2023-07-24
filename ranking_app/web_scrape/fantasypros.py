import re
import json
import requests
import pandas as pd

sources = [
    { 'url': 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php', 'ppr': 0 }, 
    { 'url':'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php', 'ppr': 1 }]

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
        df = raw_df.drop(columns=column_list)
        df = df.rename(columns={"player_positions":"position", "player_team_id":"team", "rank_ecr":"rank"})
        df = df.iloc[lambda x: x.index < 100]
        source['df'] = df
    return sources