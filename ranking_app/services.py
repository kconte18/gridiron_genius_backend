import numpy as np
import pandas as pd

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    players_dict = Player.objects.all().values()
    try:
        cbs_rankings = cbs.web_scrape(players_dict)
        for ranking in cbs_rankings:
            print(ranking['url'])
            print(ranking['scoring_type'])
            print(ranking['position'])
    except Exception as error:
        print("CBS Failed: " + error)
    try:
        fantasypros_rankings = fantasypros.web_scrape(players_dict)
        # print(fantasypros_rankings)
        # fantasypros_rankings = rankings[0]['df']
    except Exception as error:
        print("Fantasy Pros Failed: " + error)

def update_players():
    Player.objects.all().delete()
    player_df = pd.read_csv('ranking_app/data/players_2023.csv')
    player_list = player_df.values.tolist()
    for player in player_list:
        new_player = Player(id= player[0], player_name= player[1], team= player[2], position=player[3], bye_week=player[4])
        new_player.save()