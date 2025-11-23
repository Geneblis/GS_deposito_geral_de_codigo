import json
import os

SAVE_FOLDER = 'saves'
SAVE_FILE = os.path.join(SAVE_FOLDER, 'players.json')


def ensure_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)


def load_saves():
    ensure_save_folder()
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, 'r', encoding='utf-8') as file_handle:
        try:
            data = json.load(file_handle)
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []


def save_player_data(player_data):
    players = load_saves()
    for index in range(len(players)):
        if players[index].get('name', '').lower() == player_data.get('name', '').lower():
            players[index] = player_data
            with open(SAVE_FILE, 'w', encoding='utf-8') as out_file:
                json.dump(players, out_file, ensure_ascii=False, indent=2)
            return
    players.append(player_data)
    with open(SAVE_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(players, out_file, ensure_ascii=False, indent=2)
