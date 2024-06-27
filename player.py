# player.py
from constants import MAP_SIZE

class Player:
    def __init__(self, start_pos):
        self.pos = list(start_pos)
        self.char = '@'
        self.color = (255, 255, 255)  # White color for the player
        self.hitpoints = 100
        self.max_hitpoints = 100
        self.attack_power = 10

    def move(self, dx, dy, game_map):
        new_pos = [self.pos[0] + dx, self.pos[1] + dy]
        if (0 <= new_pos[0] < MAP_SIZE[0] and 
            0 <= new_pos[1] < MAP_SIZE[1] and 
            not game_map.is_wall(new_pos[0], new_pos[1])):
            self.pos = new_pos

    def take_damage(self, damage):
        self.hitpoints = max(0, self.hitpoints - damage)

    def is_alive(self):
        return self.hitpoints > 0