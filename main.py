# main.py
import pygame
import sys
import random
from constants import INITIAL_WINDOW_SIZE, MOVE_DELAY, MAP_SIZE
from game_map import GameMap
from player import Player
from rendering import get_camera_offset, draw_game, add_message
from keymap import MOVE_DIRECTIONS, WAIT
from map_handler import MapHandler
from items import HealthPotion, Weapon, Armor

def get_safe_start_position(game_map):
    if game_map.room_centers:
        return game_map.room_centers[0]
    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            if not game_map.is_wall(x, y):
                return (x, y)
    return (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2)

def change_map(player, current_map, direction):
    # Save current map
    MapHandler.save_map(current_map, f"map_level_{current_map.level}.json")

    if direction == "up":
        new_level = current_map.level + 1
    else:
        new_level = current_map.level - 1

    try:
        new_map = GameMap.load_from_file(f"map_level_{new_level}.json")
    except FileNotFoundError:
        new_map = GameMap()  # Generate a new map if file doesn't exist
    
    new_map.level = new_level
    
    # Place player at appropriate stairs or a safe position
    if direction == "up":
        if new_map.stairs_down:
            player.pos = list(new_map.stairs_down)
        else:
            player.pos = list(get_safe_start_position(new_map))
    else:
        if new_map.stairs_up:
            player.pos = list(new_map.stairs_up)
        else:
            player.pos = list(get_safe_start_position(new_map))
    
    return new_map

def spawn_items(game_map, num_items=5):
    for _ in range(num_items):
        x, y = game_map.get_random_empty_cell()
        item_type = random.choice([HealthPotion, Weapon, Armor])
        if item_type == HealthPotion:
            item = HealthPotion(heal_amount=random.randint(10, 30))
        elif item_type == Weapon:
            item = Weapon("Sword", "A sharp sword.", attack_bonus=random.randint(1, 5))
        else:
            item = Armor("Chainmail", "Protective chainmail armor.", defense_bonus=random.randint(1, 3))
        game_map.items.append((x, y, item))

def handle_combat(player, game_map):
    for npc in game_map.npcs:
        if abs(npc.x - player.pos[0]) <= 1 and abs(npc.y - player.pos[1]) <= 1:
            player_damage = player.attack(npc)
            add_message(f"You hit the {type(npc).__name__} for {player_damage} damage!")
            
            if not npc.is_alive():
                add_message(f"You defeated the {type(npc).__name__}!")
                game_map.npcs.remove(npc)
            else:
                npc_damage = npc.attack(player)
                add_message(f"The {type(npc).__name__} hits you for {npc_damage} damage!")
                
                if not player.is_alive():
                    add_message("Game Over! You have been defeated.")
                    return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Claudelike")

    # Clear the map folder at the start of the game
    MapHandler.clear_map_folder()

    current_map = GameMap()
    current_map.level = 0
    current_map.spawn_npcs()
    spawn_items(current_map)
    
    start_pos = get_safe_start_position(current_map)
    player = Player(start_pos)

    clock = pygame.time.Clock()
    
    last_move_time = 0
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # Handle movement and waiting
        keys = pygame.key.get_pressed()
        moved = False
        
        if current_time - last_move_time >= MOVE_DELAY:
            if keys[WAIT]:
                current_map.update_npcs()
                moved = True
                last_move_time = current_time
            else:
                for key, direction in MOVE_DIRECTIONS.items():
                    if keys[key]:
                        old_pos = player.pos.copy()
                        player.move(*direction, current_map)
                        current_map.update_npcs()
                        if player.pos != old_pos:
                            moved = True
                            if current_map.is_stairs(player.pos[0], player.pos[1]):
                                stairs_char = current_map.get_stairs_char(player.pos[0], player.pos[1])
                                if stairs_char == '<':
                                    add_message("You climb up the stairs...")
                                    current_map = change_map(player, current_map, "up")
                                elif stairs_char == '>':
                                    add_message("You descend down the stairs...")
                                    current_map = change_map(player, current_map, "down")
                        
                        last_move_time = current_time
                        break

        # Handle item pickup
        if player.pos in [(x, y) for x, y, _ in current_map.items]:
            item_index = [(x, y) for x, y, _ in current_map.items].index(tuple(player.pos))
            _, _, item = current_map.items.pop(item_index)
            if player.add_to_inventory(item):
                add_message(f"You picked up {item.name}!")
            else:
                add_message("Your inventory is full. You can't pick up the item.")
                current_map.items.append((player.pos[0], player.pos[1], item))

        # Handle inventory display
        if keys[pygame.K_i]:
            add_message("Inventory:")
            for i, item in enumerate(player.inventory):
                add_message(f"{i + 1}. {item.name}")

        if moved:
            if not handle_combat(player, current_map):
                add_message("Game Over! You have been defeated.")
                pygame.time.wait(2000)  # Wait for 2 seconds before quitting
                break
        
        camera_offset = get_camera_offset(player.pos, screen.get_size())
        draw_game(screen, current_map, player, camera_offset)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()