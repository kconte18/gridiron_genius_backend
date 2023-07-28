import numpy as np
import pandas as pd
from datetime import date

from . import helpers

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

def update_rankings():
    Ranking.objects.all().delete()
    RankingSource.objects.all().delete()
    players_dict = Player.objects.all().values()
    rankings_src = helpers.web_scrape(players_dict)
    for ranking_src in rankings_src:
        rankings = rankings_src[ranking_src]
        for ranking in rankings:
            ranking_src_url = ranking['url']
            scoring_type = ranking['scoring_type']
            position_ranking_type = ranking['position_ranking_type']
            new_ranking_source = RankingSource(ranking_src_name=ranking_src, ranking_src_url=ranking_src_url, scoring_type=scoring_type, position_ranking_type=position_ranking_type, date=date.today())
            new_ranking_source.save()
            for df_list_item in ranking['df_list']:
                df_list_item_player = Player.objects.get(pk= df_list_item['player_id'])
                new_player_ranking = Ranking(ranking_src= new_ranking_source, player= df_list_item_player, rank=df_list_item['rank'])
                new_player_ranking.save()

def update_players():
    Player.objects.all().delete()
    player_df = pd.read_csv('ranking_app/data/players_2023.csv')
    player_list = player_df.values.tolist()
    for player in player_list:
        new_player = Player(id= player[0], player_name= player[1], team= player[2], position=player[3], bye_week=player[4])
        new_player.save()