# map_handler.py
import json
import os
import shutil
from constants import MAP_SIZE

class MapHandler:
    MAP_FOLDER = "map_files"

    @staticmethod
    def ensure_map_folder_exists():
        if not os.path.exists(MapHandler.MAP_FOLDER):
            os.makedirs(MapHandler.MAP_FOLDER)
    
    @staticmethod
    def clear_map_folder():
        if os.path.exists(MapHandler.MAP_FOLDER):
            shutil.rmtree(MapHandler.MAP_FOLDER)
        MapHandler.ensure_map_folder_exists()
    
    @staticmethod
    def save_map(game_map, filename):
        MapHandler.ensure_map_folder_exists()
        full_path = os.path.join(MapHandler.MAP_FOLDER, filename)
        map_data = {
            "walls": game_map.map,
            "stairs_up": game_map.stairs_up,
            "stairs_down": game_map.stairs_down,
            "room_centers": game_map.room_centers
        }
        with open(full_path, 'w') as f:
            json.dump(map_data, f)

    @staticmethod
    def load_map(filename):
        full_path = os.path.join(MapHandler.MAP_FOLDER, filename)
        with open(full_path, 'r') as f:
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