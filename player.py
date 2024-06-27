# player.py
from constants import MAP_SIZE

class Player:
    def __init__(self, start_pos):
        self.pos = list(start_pos)
        self.char = '@'
        self.color = (255, 255, 255)  # White color for the player
        self.hitpoints = 100
        self.max_hitpoints = 100
        self.base_attack_power = 10
        self.base_defense = 0
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

    def move(self, dx, dy, game_map):
        new_pos = [self.pos[0] + dx, self.pos[1] + dy]
        if (0 <= new_pos[0] < MAP_SIZE[0] and 
            0 <= new_pos[1] < MAP_SIZE[1] and 
            not game_map.is_wall(new_pos[0], new_pos[1])):
            self.pos = new_pos

    @property
    def attack_power(self):
        bonus = self.equipped_weapon.attack_bonus if self.equipped_weapon else 0
        return self.base_attack_power + bonus

    @property
    def defense(self):
        bonus = self.equipped_armor.defense_bonus if self.equipped_armor else 0
        return self.base_defense + bonus

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)  # Ensure at least 1 damage is dealt
        self.hitpoints = max(0, self.hitpoints - actual_damage)
        return actual_damage

    def heal(self, amount):
        self.hitpoints = min(self.hitpoints + amount, self.max_hitpoints)

    def is_alive(self):
        return self.hitpoints > 0

    def attack(self, target):
        damage = self.attack_power
        actual_damage = target.take_damage(damage)
        return actual_damage

    def add_to_inventory(self, item):
        if len(self.inventory) < 10:  # Assuming a max inventory size of 10
            self.inventory.append(item)
            return True
        return False

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def equip_weapon(self, weapon):
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        self.remove_from_inventory(weapon)

    def equip_armor(self, armor):
        if self.equipped_armor:
            self.inventory.append(self.equipped_armor)
        self.equipped_armor = armor
        self.remove_from_inventory(armor)

    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            message = item.use(self)
            self.remove_from_inventory(item)
            return message
        return "Invalid item index."

    def get_inventory_display(self):
        inventory_display = []
        for i, item in enumerate(self.inventory):
            inventory_display.append(f"{i+1}. {item.name}")
        return inventory_display

    def __str__(self):
        return (f"Player(HP: {self.hitpoints}/{self.max_hitpoints}, "
                f"ATK: {self.attack_power}, DEF: {self.defense}, "
                f"Weapon: {self.equipped_weapon.name if self.equipped_weapon else 'None'}, "
                f"Armor: {self.equipped_armor.name if self.equipped_armor else 'None'})")