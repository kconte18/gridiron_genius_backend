import numpy as np
import pandas as pd
from datetime import date

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

from .web_scrape import cbs, fantasypros, fftoday, footballguys, thescore

def web_scrap_to_db():
    Ranking.objects.all().delete()
    RankingSource.objects.all().delete()
    players_dict = Player.objects.all().values()
    try:
        cbs_rankings = cbs.web_scrape(players_dict)

    except Exception as error:
        print("CBS Failed: ")
        print(error)

    try:
        fantasypros_rankings = fantasypros.web_scrape(players_dict)
        # print(fantasypros_rankings)
        for ranking in fantasypros_rankings:
            ranking_src_url = ranking['url']
            scoring_type = ranking['scoring_type']
            position_ranking_type = ranking['position_ranking_type']
            new_ranking_source = RankingSource(ranking_src_name='Fantasy Pros', ranking_src_url=ranking_src_url, scoring_type=scoring_type, position_ranking_type=position_ranking_type, date=date.today())
            new_ranking_source.save()
            for df_list_item in ranking['df_list']:
                df_list_item_player = Player.objects.get(pk= df_list_item['player_id'])
                new_player_ranking = Ranking(ranking_src= new_ranking_source, player= df_list_item_player, rank=df_list_item['rank'])
                new_player_ranking.save()
    except Exception as error:
        print("Fantasy Pros Failed: ")
        print(error)

def update_players():
    Player.objects.all().delete()
    player_df = pd.read_csv('ranking_app/data/players_2023.csv')
    player_list = player_df.values.tolist()
    for player in player_list:
        new_player = Player(id= player[0], player_name= player[1], team= player[2], position=player[3], bye_week=player[4])
        new_player.save()