# game_map.py
import random
from constants import MAP_SIZE
from npc import Slime, Goblin, Ghost
from map_handler import MapHandler

class GameMap:
    def __init__(self, map_data=None):
        if map_data is None:
            self.map = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]
            self._create_outer_walls()
            self.room_centers = self._create_rooms()
            self._create_corridors()
            self._place_stairs()
        else:
            self.map = map_data["walls"]
            self.stairs_up = tuple(map_data["stairs_up"]) if map_data["stairs_up"] else None
            self.stairs_down = tuple(map_data["stairs_down"]) if map_data["stairs_down"] else None
            self.room_centers = [tuple(center) for center in map_data["room_centers"]]

        self.npcs = []
        self.items = []
        self.level = 0

    def _create_outer_walls(self):
        for x in range(MAP_SIZE[0]):
            self.map[x][0] = 1
            self.map[x][MAP_SIZE[1]-1] = 1
        for y in range(MAP_SIZE[1]):
            self.map[0][y] = 1
            self.map[MAP_SIZE[0]-1][y] = 1

    def _create_rooms(self):
        room_centers = []
        for _ in range(10):  # Create 10 rooms
            room_width = random.randint(5, 15)
            room_height = random.randint(5, 15)
            x = random.randint(1, MAP_SIZE[0] - room_width - 1)
            y = random.randint(1, MAP_SIZE[1] - room_height - 1)
            
            # Check if the room overlaps with existing rooms
            overlap = any(
                abs(x - cx) < room_width and abs(y - cy) < room_height
                for cx, cy in room_centers
            )
            
            if not overlap:
                for i in range(x, x + room_width):
                    for j in range(y, y + room_height):
                        if i == x or i == x + room_width - 1 or j == y or j == y + room_height - 1:
                            self.map[i][j] = 1  # Wall
                        else:
                            self.map[i][j] = 0  # Floor
                room_centers.append((x + room_width // 2, y + room_height // 2))
        
        return room_centers

    def _create_corridors(self):
        for i in range(len(self.room_centers) - 1):
            x1, y1 = self.room_centers[i]
            x2, y2 = self.room_centers[i + 1]
            
            # Horizontal corridor
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.map[x][y1] = 0
            
            # Vertical corridor
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.map[x2][y] = 0

    def _place_stairs(self):
        empty_cells = [(x, y) for x in range(MAP_SIZE[0]) for y in range(MAP_SIZE[1]) 
                       if self.map[x][y] == 0 and (x, y) not in self.room_centers]
        
        if empty_cells:
            self.stairs_up = random.choice(empty_cells)
            empty_cells.remove(self.stairs_up)
            if empty_cells:
                self.stairs_down = random.choice(empty_cells)
            else:
                self.stairs_down = self.stairs_up  # Fallback if no other empty cells
        else:
            # Fallback if no empty cells at all
            self.stairs_up = self.stairs_down = self.room_centers[0]

    def spawn_npcs(self, num_slimes=5, num_goblins=3, num_ghosts=2):
        empty_cells = self.get_empty_cells()
        
        for _ in range(num_slimes):
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.npcs.append(Slime(x, y))
                empty_cells.remove((x, y))
        
        for _ in range(num_goblins):
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.npcs.append(Goblin(x, y))
                empty_cells.remove((x, y))
        
        for _ in range(num_ghosts):
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.npcs.append(Ghost(x, y))
                empty_cells.remove((x, y))

    def update_npcs(self):
        for npc in self.npcs:
            npc.update(self)

    def is_wall(self, x, y):
        return self.map[x][y] == 1

    def is_stairs(self, x, y):
        return (x, y) == self.stairs_up or (x, y) == self.stairs_down

    def get_stairs_char(self, x, y):
        if (x, y) == self.stairs_up:
            return '<'
        elif (x, y) == self.stairs_down:
            return '>'
        return None

    def save_to_file(self, filename):
        MapHandler.save_map(self, filename)

    @classmethod
    def load_from_file(cls, filename):
        map_data = MapHandler.load_map(filename)
        return cls(map_data)

    def get_empty_cells(self):
        return [(x, y) for x in range(MAP_SIZE[0]) for y in range(MAP_SIZE[1]) 
                if self.map[x][y] == 0 and not self.is_stairs(x, y) and 
                (x, y) not in [(npc.x, npc.y) for npc in self.npcs] and
                (x, y) not in [(item[0], item[1]) for item in self.items]]

    def get_random_empty_cell(self):
        empty_cells = self.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else None