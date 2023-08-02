from strsimpy.levenshtein import Levenshtein

from .web_scrape import fantasypros, fftoday, footballguys, thescore


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


def search_with_levenshtein(players_dict, player):
    player_dict_distance = {"player_dict": players_dict[0], "distance": 20}
    levenshtein = Levenshtein()

    for player_dict in players_dict:
        player_dict_name = player_dict["player_name"]
        distance = levenshtein.distance(player_dict_name, player[0])

        if distance < player_dict_distance["distance"]:
            player_dict_distance = {"player_dict": player_dict, "distance": distance}

    return player_dict_distance["player_dict"]["id"]


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


def web_scrape(players_dict):
    rankings = {}
    try:
        fantasypros_rankings = fantasypros.web_scrape(players_dict)
        rankings["FantasyPros"] = fantasypros_rankings
    except Exception as error:
        print("Fantasy Pros Failed: ")
        print(error)
    try:
        footballguys_rankings = fftoday.web_scrape(players_dict)
        rankings["FFToday"] = footballguys_rankings
    except Exception as error:
        print("FFToday Failed: ")
        print(error)
    try:
        footballguys_rankings = footballguys.web_scrape(players_dict)
        rankings["FootballGuys"] = footballguys_rankings
    except Exception as error:
        print("FootballGuys Failed: ")
        print(error)
    try:
        thescore_rankings = thescore.web_scrape(players_dict)
        rankings["TheScore"] = thescore_rankings
    except Exception as error:
        print("TheScore Failed: ")
        print(error)

    return rankings
