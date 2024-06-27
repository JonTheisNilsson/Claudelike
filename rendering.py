# rendering.py
import pygame
from constants import GRID_CELL_SIZE, BLUE, RED, BLACK, WHITE, MAP_SIZE

MESSAGE_BOX_HEIGHT = 100  # Define the height of the message box

def get_camera_offset(player_pos, window_size):
    offset_x = player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2
    offset_y = player_pos[1] * GRID_CELL_SIZE - (window_size[1] - MESSAGE_BOX_HEIGHT) // 2
    offset_x = max(0, min(offset_x, MAP_SIZE[0] * GRID_CELL_SIZE - window_size[0]))
    offset_y = max(0, min(offset_y, MAP_SIZE[1] * GRID_CELL_SIZE - (window_size[1] - MESSAGE_BOX_HEIGHT)))
    return offset_x, offset_y

class MessageLog:
    def __init__(self, max_messages=5):
        self.messages = []
        self.max_messages = max_messages

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

message_log = MessageLog()

def draw_message_box(surface, width, height):
    box_height = MESSAGE_BOX_HEIGHT
    box_width = width
    box_x = 0
    box_y = height - box_height

    # Draw the box background
    pygame.draw.rect(surface, (50, 50, 50), (box_x, box_y, box_width, box_height))
    
    # Draw the border
    pygame.draw.rect(surface, WHITE, (box_x, box_y, box_width, box_height), 2)

    # Render the messages
    font = pygame.font.Font(None, 24)
    y_offset = 5
    for message in message_log.messages:
        text_surface = font.render(message, True, WHITE)
        surface.blit(text_surface, (box_x + 10, box_y + y_offset))
        y_offset += 25

def draw_game(surface, game_map, player, camera_offset):
    surface.fill(BLACK)
    start_x = max(0, camera_offset[0] // GRID_CELL_SIZE)
    end_x = min(MAP_SIZE[0], (camera_offset[0] + surface.get_width()) // GRID_CELL_SIZE + 1)
    start_y = max(0, camera_offset[1] // GRID_CELL_SIZE)
    end_y = min(MAP_SIZE[1], (camera_offset[1] + surface.get_height() - MESSAGE_BOX_HEIGHT) // GRID_CELL_SIZE + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            screen_x = x * GRID_CELL_SIZE - camera_offset[0]
            screen_y = y * GRID_CELL_SIZE - camera_offset[1]
            
            if screen_y + GRID_CELL_SIZE > surface.get_height() - MESSAGE_BOX_HEIGHT:
                continue

            if game_map.is_wall(x, y):
                pygame.draw.rect(surface, BLUE, (screen_x, screen_y, GRID_CELL_SIZE, GRID_CELL_SIZE))
            elif game_map.is_stairs(x, y):
                stairs_char = game_map.get_stairs_char(x, y)
                color = (255, 255, 0)  # Yellow color for stairs
                if stairs_char == '<':
                    pygame.draw.polygon(surface, color, [
                        (screen_x + GRID_CELL_SIZE // 2, screen_y + GRID_CELL_SIZE // 5),
                        (screen_x + GRID_CELL_SIZE // 5, screen_y + GRID_CELL_SIZE * 4 // 5),
                        (screen_x + GRID_CELL_SIZE * 4 // 5, screen_y + GRID_CELL_SIZE * 4 // 5)
                    ])
                elif stairs_char == '>':
                    pygame.draw.polygon(surface, color, [
                        (screen_x + GRID_CELL_SIZE // 2, screen_y + GRID_CELL_SIZE * 4 // 5),
                        (screen_x + GRID_CELL_SIZE // 5, screen_y + GRID_CELL_SIZE // 5),
                        (screen_x + GRID_CELL_SIZE * 4 // 5, screen_y + GRID_CELL_SIZE // 5)
                    ])

    # Draw items
    for x, y, item in game_map.items:
        screen_x = x * GRID_CELL_SIZE - camera_offset[0]
        screen_y = y * GRID_CELL_SIZE - camera_offset[1]
        
        if screen_y + GRID_CELL_SIZE > surface.get_height() - MESSAGE_BOX_HEIGHT:
            continue

        item_color = (255, 255, 0)  # Yellow for items
        pygame.draw.rect(surface, item_color, (screen_x, screen_y, GRID_CELL_SIZE, GRID_CELL_SIZE))
        font = pygame.font.Font(None, 24)
        text = font.render('?', True, BLACK)  # Use '?' to represent items
        text_rect = text.get_rect(center=(screen_x + GRID_CELL_SIZE // 2, screen_y + GRID_CELL_SIZE // 2))
        surface.blit(text, text_rect)

    # Draw NPCs
    for npc in game_map.npcs:
        screen_x = npc.x * GRID_CELL_SIZE - camera_offset[0]
        screen_y = npc.y * GRID_CELL_SIZE - camera_offset[1]
        
        if screen_y + GRID_CELL_SIZE > surface.get_height() - MESSAGE_BOX_HEIGHT:
            continue

        pygame.draw.rect(surface, npc.color, (screen_x, screen_y, GRID_CELL_SIZE, GRID_CELL_SIZE))
        # Draw NPC character
        font = pygame.font.Font(None, 24)
        text = font.render(npc.char, True, BLACK)  # Black text for contrast
        text_rect = text.get_rect(center=(screen_x + GRID_CELL_SIZE // 2, screen_y + GRID_CELL_SIZE // 2))
        surface.blit(text, text_rect)

    # Draw player
    player_screen_x = player.pos[0] * GRID_CELL_SIZE - camera_offset[0]
    player_screen_y = player.pos[1] * GRID_CELL_SIZE - camera_offset[1]
    
    if player_screen_y + GRID_CELL_SIZE <= surface.get_height() - MESSAGE_BOX_HEIGHT:
        font = pygame.font.Font(None, 24)
        player_text = font.render(player.char, True, player.color)
        player_rect = player_text.get_rect(center=(player_screen_x + GRID_CELL_SIZE // 2, player_screen_y + GRID_CELL_SIZE // 2))
        surface.blit(player_text, player_rect)

    # Draw player's hitpoints
    hp_text = f"HP: {player.hitpoints}/{player.max_hitpoints}"
    hp_font = pygame.font.Font(None, 32)
    hp_surface = hp_font.render(hp_text, True, WHITE)
    surface.blit(hp_surface, (10, 10))  # Position in the top-left corner

    # Draw floor number
    floor_text = f"Floor: {game_map.level}"
    floor_font = pygame.font.Font(None, 32)
    floor_surface = floor_font.render(floor_text, True, WHITE)
    floor_rect = floor_surface.get_rect()
    floor_rect.topright = (surface.get_width() - 10, 10)  # Position in the top-right corner
    surface.blit(floor_surface, floor_rect)

    # Draw the message box
    draw_message_box(surface, surface.get_width(), surface.get_height())

def add_message(message):
    message_log.add_message(message)