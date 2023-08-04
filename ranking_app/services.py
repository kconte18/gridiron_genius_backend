import pandas as pd
from datetime import date
from django.http import HttpResponseBadRequest

from . import helpers
from . import serializers

from ranking_app.models import Player
from ranking_app.models import RankingSource
from ranking_app.models import Ranking

def get_rankings_by_score_and_position(score_type, position):
    if not((score_type == 'ppr' or score_type == 'standard') and (position == 'overall' or position == 'qb' or position == 'rb' or position == 'wr' or position == 'te' or position == 'def' or position == 'k')):
        raise HttpResponseBadRequest("Bad query parameters")
    ranking_sources = RankingSource.objects.filter(scoring_type= score_type.upper(), position_ranking_type= position.upper())
    rankings = Ranking.objects.filter(ranking_src__id__in= ranking_sources.all())
    serializer = serializers.RankingSerializer(rankings, many=True)
    return serializer

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
    update_rankings_avg()

def update_players():
    Player.objects.all().delete()
    player_df = pd.read_csv('ranking_app/data/players_2023.csv')
    player_list = player_df.values.tolist()
    for player in player_list:
        new_player = Player(id= player[0], player_name= player[1], team= player[2], position=player[3], bye_week=player[4])
        new_player.save()

# This is called in the update_rankings service method
def update_rankings_avg():
    score_type_list = ['STANDARD', 'PPR']
    position_type_list = ['OVERALL', 'QB', 'RB', 'WR', 'TE']
    for score_type in score_type_list:
        for position_type in position_type_list:
            ranking_sources = RankingSource.objects.filter(scoring_type= score_type, position_ranking_type= position_type)
            rankings = Ranking.objects.filter(ranking_src__id__in= ranking_sources.all())
            rankings_avg = helpers.find_ranking_averages(rankings)
            avg_ranking_src = RankingSource(
                ranking_src_name= 'AVERAGE',
                ranking_src_url= 'N/A',
                date= date.today(),
                scoring_type= score_type,
                position_ranking_type= position_type
            )
            avg_ranking_src.save()
            for key, value in rankings_avg.items():
                player = Player.objects.get(pk= key)
                new_ranking_avg =  Ranking(ranking_src= avg_ranking_src, player= player, rank= value['rank_avg'])
                new_ranking_avg.save()