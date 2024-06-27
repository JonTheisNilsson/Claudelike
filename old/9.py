import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
INITIAL_WINDOW_SIZE = (800, 600)
GRID_CELL_SIZE = 20  # Smaller cell size
MAP_SIZE = (75, 75)  # Larger map size to accommodate more rooms

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the game window (resizable)
screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Grid Game with Rooms")

# Create the game map
game_map = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]

# Create walls around the map
for x in range(MAP_SIZE[0]):
    game_map[x][0] = 1
    game_map[x][MAP_SIZE[1]-1] = 1
for y in range(MAP_SIZE[1]):
    game_map[0][y] = 1
    game_map[MAP_SIZE[0]-1][y] = 1

# Function to create a room
def create_room(x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            if i == x or i == x + width - 1 or j == y or j == y + height - 1:
                game_map[i][j] = 1
    return (x + width // 2, y + height // 2)  # Return center of the room

# Create rooms
num_rooms = 10
room_centers = []
for _ in range(num_rooms):
    room_width = random.randint(5, 15)
    room_height = random.randint(5, 15)
    x = random.randint(1, MAP_SIZE[0] - room_width - 1)
    y = random.randint(1, MAP_SIZE[1] - room_height - 1)
    center = create_room(x, y, room_width, room_height)
    room_centers.append(center)

# Create corridors to connect rooms
def create_corridor(x1, y1, x2, y2):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map[x][y1] = 0
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map[x2][y] = 0

# Connect rooms with corridors
for i in range(len(room_centers) - 1):
    create_corridor(room_centers[i][0], room_centers[i][1],
                    room_centers[i+1][0], room_centers[i+1][1])

# Player position (in grid coordinates)
player_pos = list(room_centers[0])  # Start in the center of the first room

def get_camera_offset(window_size):
    offset_x = player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2
    offset_y = player_pos[1] * GRID_CELL_SIZE - window_size[1] // 2
    offset_x = max(0, min(offset_x, MAP_SIZE[0] * GRID_CELL_SIZE - window_size[0]))
    offset_y = max(0, min(offset_y, MAP_SIZE[1] * GRID_CELL_SIZE - window_size[1]))
    return offset_x, offset_y

def draw_game(surface, camera_offset):
    surface.fill(BLACK)
    start_x = max(0, camera_offset[0] // GRID_CELL_SIZE)
    end_x = min(MAP_SIZE[0], (camera_offset[0] + surface.get_width()) // GRID_CELL_SIZE + 1)
    start_y = max(0, camera_offset[1] // GRID_CELL_SIZE)
    end_y = min(MAP_SIZE[1], (camera_offset[1] + surface.get_height()) // GRID_CELL_SIZE + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if game_map[x][y] == 1:
                pygame.draw.rect(surface, BLUE, (
                    x * GRID_CELL_SIZE - camera_offset[0],
                    y * GRID_CELL_SIZE - camera_offset[1],
                    GRID_CELL_SIZE, GRID_CELL_SIZE
                ))

    pygame.draw.rect(surface, RED, (
        player_pos[0] * GRID_CELL_SIZE - camera_offset[0],
        player_pos[1] * GRID_CELL_SIZE - camera_offset[1],
        GRID_CELL_SIZE, GRID_CELL_SIZE
    ))

def main():
    global screen
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                new_pos = player_pos.copy()
                if event.key == pygame.K_UP:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1
                elif event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                
                if (0 <= new_pos[0] < MAP_SIZE[0] and 
                    0 <= new_pos[1] < MAP_SIZE[1] and 
                    game_map[new_pos[0]][new_pos[1]] == 0):
                    player_pos[:] = new_pos

        camera_offset = get_camera_offset(screen.get_size())
        draw_game(screen, camera_offset)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()