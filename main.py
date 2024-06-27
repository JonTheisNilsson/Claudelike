# main.py
import pygame
import sys
from constants import INITIAL_WINDOW_SIZE, MOVE_DELAY, MAP_SIZE
from game_map import GameMap
from player import Player
from rendering import get_camera_offset, draw_game
from keymap import MOVE_DIRECTIONS, WAIT
from map_handler import MapHandler

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
    current_map.save_to_file(f"map_level_{current_map.level}.json")

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

def main():
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Claudelike")  # Set the new game title

    current_map = GameMap()
    current_map.level = 0  # Set the starting floor to 0
    current_map.spawn_npcs()
    
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
                                    print("You climb up the stairs...")
                                    current_map = change_map(player, current_map, "up")
                                elif stairs_char == '>':
                                    print("You descend down the stairs...")
                                    current_map = change_map(player, current_map, "down")
                        
                        last_move_time = current_time
                        break
        
        camera_offset = get_camera_offset(player.pos, screen.get_size())
        draw_game(screen, current_map, player, camera_offset)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()