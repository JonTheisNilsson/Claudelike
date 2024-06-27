from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, player):
        pass

class HealthPotion(Item):
    def __init__(self, heal_amount):
        super().__init__("Health Potion", "Restores some health when consumed.")
        self.heal_amount = heal_amount

    def use(self, player):
        player.heal(self.heal_amount)
        return f"You drink the Health Potion and restore {self.heal_amount} HP."

class Weapon(Item):
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description)
        self.attack_bonus = attack_bonus

    def use(self, player):
        old_weapon = player.equipped_weapon
        player.equip_weapon(self)
        return f"You equip the {self.name}. Attack power increased by {self.attack_bonus}."

class Armor(Item):
    def __init__(self, name, description, defense_bonus):
        super().__init__(name, description)
        self.defense_bonus = defense_bonus

    def use(self, player):
        old_armor = player.equipped_armor
        player.equip_armor(self)
        return f"You equip the {self.name}. Defense increased by {self.defense_bonus}."