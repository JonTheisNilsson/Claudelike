# rendering.py
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
            elif game_map.is_stairs(x, y):
                stairs_char = game_map.get_stairs_char(x, y)
                color = (255, 255, 0)  # Yellow color for stairs
                if stairs_char == '<':
                    pygame.draw.polygon(surface, color, [
                        ((x + 0.5) * GRID_CELL_SIZE - camera_offset[0], (y + 0.2) * GRID_CELL_SIZE - camera_offset[1]),
                        ((x + 0.2) * GRID_CELL_SIZE - camera_offset[0], (y + 0.8) * GRID_CELL_SIZE - camera_offset[1]),
                        ((x + 0.8) * GRID_CELL_SIZE - camera_offset[0], (y + 0.8) * GRID_CELL_SIZE - camera_offset[1])
                    ])
                elif stairs_char == '>':
                    pygame.draw.polygon(surface, color, [
                        ((x + 0.5) * GRID_CELL_SIZE - camera_offset[0], (y + 0.8) * GRID_CELL_SIZE - camera_offset[1]),
                        ((x + 0.2) * GRID_CELL_SIZE - camera_offset[0], (y + 0.2) * GRID_CELL_SIZE - camera_offset[1]),
                        ((x + 0.8) * GRID_CELL_SIZE - camera_offset[0], (y + 0.2) * GRID_CELL_SIZE - camera_offset[1])
                    ])

    # Draw NPCs
    for npc in game_map.npcs:
        pygame.draw.rect(surface, npc.color, (
            npc.x * GRID_CELL_SIZE - camera_offset[0],
            npc.y * GRID_CELL_SIZE - camera_offset[1],
            GRID_CELL_SIZE, GRID_CELL_SIZE
        ))
        # Draw NPC character
        font = pygame.font.Font(None, 24)
        text = font.render(npc.char, True, BLACK)  # Black text for contrast
        text_rect = text.get_rect(center=(
            npc.x * GRID_CELL_SIZE - camera_offset[0] + GRID_CELL_SIZE // 2,
            npc.y * GRID_CELL_SIZE - camera_offset[1] + GRID_CELL_SIZE // 2
        ))
        surface.blit(text, text_rect)

    # Draw player
    font = pygame.font.Font(None, 24)
    player_text = font.render(player.char, True, player.color)
    player_rect = player_text.get_rect(center=(
        player.pos[0] * GRID_CELL_SIZE - camera_offset[0] + GRID_CELL_SIZE // 2,
        player.pos[1] * GRID_CELL_SIZE - camera_offset[1] + GRID_CELL_SIZE // 2
    ))
    surface.blit(player_text, player_rect)

    # Draw player's hitpoints
    hp_text = f"HP: {player.hitpoints}/{player.max_hitpoints}"
    hp_font = pygame.font.Font(None, 32)
    hp_surface = hp_font.render(hp_text, True, (255, 255, 255))  # White text
    surface.blit(hp_surface, (10, 10))  # Position in the top-left corner

    # Draw floor number
    floor_text = f"Floor: {game_map.level}"
    floor_font = pygame.font.Font(None, 32)
    floor_surface = floor_font.render(floor_text, True, (255, 255, 255))  # White text
    floor_rect = floor_surface.get_rect()
    floor_rect.topright = (surface.get_width() - 10, 10)  # Position in the top-right corner
    surface.blit(floor_surface, floor_rect)