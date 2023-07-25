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