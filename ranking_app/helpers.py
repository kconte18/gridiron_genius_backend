from strsimpy.levenshtein import Levenshtein

from .web_scrape import fantasypros, fftoday, thescore, walters, espn

# SEARCH FOR PLAYERS WITH BINARY
def binary_search_for_player(players_dict, low, high, player):
    player_name = player[0]
    while low <= high:
        mid = low + (high - low) // 2
        player_dict_name = players_dict[mid]["player_name"]
        if player_dict_name.lower() == player_name.lower():
            return players_dict[mid]["id"]

        elif player_dict_name < player_name:
            low = mid + 1

        else:
            high = mid - 1
    return search_with_levenshtein(players_dict, player)

# IF CAN'T FIND PLAYERS WITH BINARY, SEARCH PLAYERS WITH LEVENSHTEIN
def search_with_levenshtein(players_dict, player):
    player_dict_distance = {"player_dict": players_dict[0], "distance": 20}
    levenshtein = Levenshtein()

    for player_dict in players_dict:
        player_dict_name = player_dict["player_name"]
        distance = levenshtein.distance(player_dict_name, player[0])

        if distance < player_dict_distance["distance"]:
            player_dict_distance = {"player_dict": player_dict, "distance": distance}

    return player_dict_distance["player_dict"]["id"]

# FINDS EACH PLAYER AND CALCULATES WITH OCCURENCE AND WITH ALL THE RANKS
def find_ranking_averages(rankings):
    rankings_avg = {}
    for ranking in rankings:
        if ranking.player.id in rankings_avg.keys():
            rankings_avg[ranking.player.id]['occurrence'] = rankings_avg[ranking.player.id]['occurrence'] + 1
            rankings_avg[ranking.player.id]['rank_total'] = rankings_avg[ranking.player.id]['rank_total'] + ranking.rank
        else:
            rankings_avg[ranking.player.id] = {
                'occurrence': 1,
                'rank_total': ranking.rank
            }
    for key, value in rankings_avg.items():
        rank_avg = value['rank_total'] / value['occurrence']
        value['rank_avg'] = rank_avg
        del value['rank_total']
        del value['occurrence']
    return rankings_avg

# SWAPPING THE PLAYERS NAME WITH THEIR ID
def swap_name_with_id(raw_df, players_dict):
    raw_df_list = raw_df.values.tolist()
    sorted_players_dict = sorted(players_dict, key=lambda x: x["player_name"])
    df_list = []
    for player in raw_df_list:
        player_id = binary_search_for_player(
            sorted_players_dict, 0, len(players_dict) - 1, player
        )
        df_list_item = {"player_id": player_id, "rank": player[1]}
        df_list.append(df_list_item)
    return df_list

# WEB SCRAPES EACH WEBSITE
def web_scrape(players_dict):
    rankings = {}
    error_logs = []
    try:
        espn_rankings = espn.web_scrape_pdf(players_dict)
        rankings["ESPN"] = espn_rankings
    except Exception as error:
        print("ESPN Failed: ")
        print(error)
        log_error = {
            'Error Caused in': 'ESPN',
            'Reason for error': error
        }
        error_logs.append(log_error)
    try:
        fantasypros_rankings = fantasypros.web_scrape(players_dict)
        rankings["FantasyPros"] = fantasypros_rankings
    except Exception as error:
        print("Fantasy Pros Failed: ")
        print(error)
        log_error = {
            'Error Caused in': 'Fantasy Pros',
            'Reason for error': error
        }
        error_logs.append(log_error)
    try:
        footballguys_rankings = fftoday.web_scrape(players_dict)
        rankings["FfToday"] = footballguys_rankings
    except Exception as error:
        print("FFToday Failed: ")
        print(error)
        log_error = {
            'Error Caused in': 'FFToday',
            'Reason for error': error
        }
        error_logs.append(log_error)
    try:
        thescore_rankings = thescore.web_scrape(players_dict)
        rankings["TheScore"] = thescore_rankings
    except Exception as error:
        print("TheScore Failed: ")
        print(error)
        log_error = {
            'Error Caused in': 'TheScore',
            'Reason for error': error
        }
        error_logs.append(log_error)
    try:
        walters_rankings = walters.web_scrape(players_dict)
        rankings['WalterFootball'] = walters_rankings
    except Exception as error:
        print("Walter Football Failed: ")
        print(error)
        log_error = {
            'Error Caused in': 'Walter Football',
            'Reason for error': error
        }
        error_logs.append(log_error)
    if len(error_logs) > 0:
        raise Exception(error_logs)
    else:
        return rankings

def test():
    print('test')