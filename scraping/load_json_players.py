import json

def read_json():
    with open('C:\\Users\\Patryk\\python\\nba_players\data\json_files\\active_nba_players.json', encoding='utf-8') as fh:
        player_names_json = json.load(fh)
    return player_names_json