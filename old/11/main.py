import pygame
import sys
from constants import INITIAL_WINDOW_SIZE, MAP_SIZE, MOVE_DELAY
from game_map import GameMap
from player import Player
from rendering import get_camera_offset, draw_game

def main():
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Grid Game with Rooms")

    game_map = GameMap()
    player = Player(game_map.room_centers[0])

    clock = pygame.time.Clock()
    
    move_directions = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }
    
    last_move_time = 0
    continuous_move = False
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key in move_directions:
                    player.move(*move_directions[event.key], game_map)
                    last_move_time = current_time
                    continuous_move = True
            elif event.type == pygame.KEYUP:
                if event.key in move_directions:
                    continuous_move = False
        
        # Handle continuous movement
        keys = pygame.key.get_pressed()
        if continuous_move and current_time - last_move_time >= MOVE_DELAY:
            for key, direction in move_directions.items():
                if keys[key]:
                    player.move(*direction, game_map)
                    last_move_time = current_time
                    break  # Only move in one direction if multiple keys are pressed
        
        camera_offset = get_camera_offset(player.pos, screen.get_size(), MAP_SIZE)
        draw_game(screen, game_map, player, camera_offset)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()