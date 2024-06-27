# npc.py
import random
from constants import MAP_SIZE

class NPC:
    def __init__(self, x, y, char='N', color=(255, 255, 0), hitpoints=20, attack_power=5):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.hitpoints = hitpoints
        self.max_hitpoints = hitpoints
        self.attack_power = attack_power
        self.movement_counter = 0
        self.direction = self.get_random_direction()

    def get_random_direction(self):
        return random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def move(self, game_map):
        self.movement_counter += 1
        if self.movement_counter >= 3:  # Change direction every 3 moves
            self.direction = self.get_random_direction()
            self.movement_counter = 0

        new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
        if (0 <= new_x < MAP_SIZE[0] and 
            0 <= new_y < MAP_SIZE[1] and 
            not game_map.is_wall(new_x, new_y)):
            self.x, self.y = new_x, new_y
        else:
            # If blocked, try a random direction
            self.direction = self.get_random_direction()

    def update(self, game_map):
        self.move(game_map)

    def take_damage(self, damage):
        self.hitpoints = max(0, self.hitpoints - damage)

    def is_alive(self):
        return self.hitpoints > 0

class Slime(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, char='S', color=(0, 255, 0), hitpoints=15, attack_power=3)

class Goblin(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, char='G', color=(255, 0, 0), hitpoints=25, attack_power=7)
    
    def move(self, game_map):
        # Goblins move twice as fast
        for _ in range(2):
            super().move(game_map)

class Ghost(NPC):
    def __init__(self, x, y):
        super().__init__(x, y, char='H', color=(200, 200, 200), hitpoints=20, attack_power=5)
    
    def move(self, game_map):
        self.movement_counter += 1
        if self.movement_counter >= 5:  # Ghosts change direction less frequently
            self.direction = self.get_random_direction()
            self.movement_counter = 0

        new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
        if 0 <= new_x < MAP_SIZE[0] and 0 <= new_y < MAP_SIZE[1]:
            self.x, self.y = new_x, new_y  # Ghosts can move through walls