import random
from constants import MAP_SIZE

class GameMap:
    def __init__(self):
        self.map = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]
        self._create_outer_walls()
        self.room_centers = self._create_rooms()
        self._create_corridors()

    def _create_outer_walls(self):
        for x in range(MAP_SIZE[0]):
            self.map[x][0] = 1
            self.map[x][MAP_SIZE[1]-1] = 1
        for y in range(MAP_SIZE[1]):
            self.map[0][y] = 1
            self.map[MAP_SIZE[0]-1][y] = 1

    def _create_room(self, x, y, width, height):
        for i in range(x, x + width):
            for j in range(y, y + height):
                if i == x or i == x + width - 1 or j == y or j == y + height - 1:
                    self.map[i][j] = 1
        return (x + width // 2, y + height // 2)

    def _create_rooms(self):
        room_centers = []
        for _ in range(10):  # Create 10 rooms
            room_width = random.randint(5, 15)
            room_height = random.randint(5, 15)
            x = random.randint(1, MAP_SIZE[0] - room_width - 1)
            y = random.randint(1, MAP_SIZE[1] - room_height - 1)
            center = self._create_room(x, y, room_width, room_height)
            room_centers.append(center)
        return room_centers

    def _create_corridor(self, x1, y1, x2, y2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y1] = 0
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x2][y] = 0

    def _create_corridors(self):
        for i in range(len(self.room_centers) - 1):
            self._create_corridor(self.room_centers[i][0], self.room_centers[i][1],
                                  self.room_centers[i+1][0], self.room_centers[i+1][1])

    def is_wall(self, x, y):
        return self.map[x][y] == 1