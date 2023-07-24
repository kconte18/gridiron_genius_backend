import numpy as np
import pandas as pd

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    rankings = []
    try:
        rankings.append(cbs.web_scrape())
        # cbs_rankings = rankings[0]['df']
    except:
        print("CBS Failed")
    try:
        rankings.append(fantasypros.web_scrape())
        # fantasypros_rankings = rankings[0]['df']
    except:
        print("Fantasy Pros Failed")
    for ranking in rankings:
        print(rankings)

def update_players():
    Player.objects.all().delete()
    