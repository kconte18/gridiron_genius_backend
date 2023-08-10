import pandas as pd
import re
import tabula

from ranking_app import helpers
from ..data import rankings_sources

sources = rankings_sources.espn_sources

def web_scrape_pdf(players_dict):
    for source in sources:
        dfs = tabula.read_pdf(source['url'], stream=True, pages='1')
        if source['position_ranking_type'] == 'OVERALL':
            df = overall_clean(dfs)
        # POSITION RANKINGS
        else:
            current_position = source['position_ranking_type']
            df = positional_clean(dfs, current_position)

        source['df_list'] = helpers.swap_name_with_id(df, players_dict)
    return sources

def overall_clean(dfs):
    one_to_eighty_raw = dfs[0]['RANKINGS 1-80'].tolist()
    eightyone_to_hundred_raw = dfs[0]['RANKINGS 81-160'].tolist()
    rankings = []
    rank_num = 1
    for obj in one_to_eighty_raw:
        if(str(obj) == 'nan'):
            continue
        else:
            player_name = re.sub(r'[,]\s\w+', '', str(obj))
            player = {
                'player_name': player_name,
                'rank': rank_num
            }
            rankings.append(player)
            rank_num += 1
    for obj in eightyone_to_hundred_raw:
        if str(obj) == 'nan':
            continue
        else:
            player = set_player(str(obj), rank_num)
            rankings.append(player)
            rank_num += 1
        if rank_num > 100:
            break
    return pd.DataFrame(rankings)

def positional_clean(dfs, current_position):
    rankings = []
    rank_num = 1
    if current_position == 'QB':
        qb_te_list = dfs[0]['Quarterbacks'].tolist()
        for obj in qb_te_list:
            if rank_num > 32:
                break
            if str(obj) == 'nan':
                continue
            player = set_player(str(obj), rank_num)
            rankings.append(player)
            rank_num += 1
    elif current_position == 'TE':
        qb_te_list = dfs[0]['Quarterbacks'].tolist()
        on_qbs = True
        for obj in qb_te_list:
            if str(obj) == 'Tight Ends':
                on_qbs = False
                continue
            if str(obj) == 'nan':
                continue
            if on_qbs:
                continue
            player = set_player(str(obj), rank_num)
            rankings.append(player)
            rank_num += 1
    elif current_position == 'RB':
        rb_list = dfs[0]['Running Backs'].tolist()
        for obj in rb_list:
            if str(obj) == 'nan':
                continue
            if rank_num > 50:
                break
            player = set_player(str(obj), rank_num)
            rankings.append(player)
            rank_num += 1
    elif current_position == 'WR':
        rb_wr_list = dfs[0]['Running Backs (ctn\'d)'].tolist()
        on_rbs = True
        for obj in rb_wr_list:
            if str(obj) == 'Wide Receivers':
                on_rbs = False
                continue
            if str(obj) == 'nan':
                continue
            if on_rbs:
                continue
            if rank_num > 50:
                break
            player = set_player(str(obj), rank_num)
            rankings.append(player)
            rank_num += 1
    return pd.DataFrame(rankings)

# Just cleans up the player string to remove stuff like teams and player value
def set_player(raw_player_name, rank_num):
    player_name = re.sub(r'[,]\s\w+\s*.*', '', raw_player_name)
    player = {
        'player_name': player_name,
        'rank': rank_num
    }
    return player