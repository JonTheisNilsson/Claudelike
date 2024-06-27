import pygame
from constants import GRID_CELL_SIZE, BLUE, RED, BLACK, MAP_SIZE

def get_camera_offset(player_pos, window_size):
    offset_x = player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2
    offset_y = player_pos[1] * GRID_CELL_SIZE - window_size[1] // 2
    offset_x = max(0, min(offset_x, MAP_SIZE[0] * GRID_CELL_SIZE - window_size[0]))
    offset_y = max(0, min(offset_y, MAP_SIZE[1] * GRID_CELL_SIZE - window_size[1]))
    return offset_x, offset_y

def draw_game(surface, game_map, player, camera_offset):
    surface.fill(BLACK)
    start_x = max(0, camera_offset[0] // GRID_CELL_SIZE)
    end_x = min(MAP_SIZE[0], (camera_offset[0] + surface.get_width()) // GRID_CELL_SIZE + 1)
    start_y = max(0, camera_offset[1] // GRID_CELL_SIZE)
    end_y = min(MAP_SIZE[1], (camera_offset[1] + surface.get_height()) // GRID_CELL_SIZE + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if game_map.is_wall(x, y):
                pygame.draw.rect(surface, BLUE, (
                    x * GRID_CELL_SIZE - camera_offset[0],
                    y * GRID_CELL_SIZE - camera_offset[1],
                    GRID_CELL_SIZE, GRID_CELL_SIZE
                ))

    pygame.draw.rect(surface, RED, (
        player.pos[0] * GRID_CELL_SIZE - camera_offset[0],
        player.pos[1] * GRID_CELL_SIZE - camera_offset[1],
        GRID_CELL_SIZE, GRID_CELL_SIZE
    ))
