# map_handler.py
import json
from constants import MAP_SIZE

class MapHandler:
    @staticmethod
    def save_map(game_map, filename):
        map_data = {
            "walls": game_map.map,
            "stairs_up": game_map.stairs_up,
            "stairs_down": game_map.stairs_down,
            "room_centers": game_map.room_centers
        }
        with open(filename, 'w') as f:
            json.dump(map_data, f)

    @staticmethod
    def load_map(filename):
        with open(filename, 'r') as f:
            map_data = json.load(f)
        return map_data

    @staticmethod
    def create_empty_map():
        return {
            "walls": [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])],
            "stairs_up": None,
            "stairs_down": None,
            "room_centers": []
        }