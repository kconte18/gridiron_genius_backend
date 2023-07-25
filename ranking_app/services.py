import numpy as np
import pandas as pd

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    rankings = []
    # try:
    #     rankings.append(cbs.web_scrape())
    #     # cbs_rankings = rankings[0]['df']
    # except:
    #     print("CBS Failed")
    # try:
        # rankings.append(fantasypros.web_scrape())
        # fantasypros_rankings = rankings[0]['df']
    # except:
        # print("Fantasy Pros Failed")

    #  TEMP BELOW
    rankings.append(fantasypros.web_scrape())

def update_players():
    Player.objects.all().delete()
    player_df = pd.read_csv('ranking_app/data/players_2023.csv')
    player_list = player_df.values.tolist()
    for player in player_list:
        new_player = Player(id= player[0], player_name= player[1], team= player[2], position=player[3], bye_week=player[4])
        new_player.save()