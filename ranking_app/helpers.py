from strsimpy.levenshtein import Levenshtein

def binary_search_for_player(players_dict, low, high, player):
    while low <= high:
        mid = low + (high - low) // 2
        player_dict_name = players_dict[mid]['player_name']

        if player_dict_name.lower() == player.lower():
            return players_dict[mid]['id']
 
        elif player_dict_name < player:
            low = mid + 1
 
        else:
            high = mid - 1
    return search_with_levenshtein(players_dict, player)

def search_with_levenshtein(players_dict, player):
    player_dict_distance= {'player_dict': 'Nothing is related', 'distance': 20}
    for player_dict in players_dict:
        levenshtein = Levenshtein()

        player_dict_name = player_dict['player_name']
        distance = levenshtein.distance(player_dict_name, player)

        if distance < player_dict_distance['distance']:
            player_dict_distance = {'player_dict': player_dict, 'distance': distance}

    return player_dict_distance['player_dict']['id']

def swap_name_with_id(raw_df, players_dict):
        raw_df_list = raw_df.values.tolist()
        sorted_players_dict = sorted(players_dict, key=lambda x: x['player_name'])
        df_list = []
        for item in raw_df_list:
            player_id = binary_search_for_player(sorted_players_dict, 0, len(players_dict)-1, item[0])
            df_list_item = {'player_id': player_id, 'rank':item[1]}
            df_list.append(df_list_item)
        return df_list