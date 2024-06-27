import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
INITIAL_WINDOW_SIZE = (800, 600)
GRID_CELL_SIZE = 50  # Fixed size of each grid cell
MAP_SIZE = (30, 30)  # Larger map size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the game window (resizable)
screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Grid Game")

# Create the game map
game_map = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]

# Create walls around the map
for x in range(MAP_SIZE[0]):
    game_map[x][0] = 1
    game_map[x][MAP_SIZE[1]-1] = 1
for y in range(MAP_SIZE[1]):
    game_map[0][y] = 1
    game_map[MAP_SIZE[0]-1][y] = 1

# Add some random structures
for _ in range(50):  # Add 50 random wall tiles
    x = random.randint(1, MAP_SIZE[0]-2)
    y = random.randint(1, MAP_SIZE[1]-2)
    game_map[x][y] = 1

# Player position (in grid coordinates)
player_pos = [MAP_SIZE[0] // 2, MAP_SIZE[1] // 2]
# Ensure the player doesn't start on a wall
while game_map[player_pos[0]][player_pos[1]] == 1:
    player_pos = [random.randint(1, MAP_SIZE[0]-2), random.randint(1, MAP_SIZE[1]-2)]

def get_camera_offset(window_size):
    # Calculate the offset to center the player on the screen
    offset_x = player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2
    offset_y = player_pos[1] * GRID_CELL_SIZE - window_size[1] // 2

    # Clamp the camera offset to prevent showing areas outside the map
    offset_x = max(0, min(offset_x, MAP_SIZE[0] * GRID_CELL_SIZE - window_size[0]))
    offset_y = max(0, min(offset_y, MAP_SIZE[1] * GRID_CELL_SIZE - window_size[1]))

    return offset_x, offset_y

def draw_game(surface, camera_offset):
    # Clear the screen
    surface.fill(BLACK)

    # Calculate the visible range of the grid
    start_x = max(0, camera_offset[0] // GRID_CELL_SIZE)
    end_x = min(MAP_SIZE[0], (camera_offset[0] + surface.get_width()) // GRID_CELL_SIZE + 1)
    start_y = max(0, camera_offset[1] // GRID_CELL_SIZE)
    end_y = min(MAP_SIZE[1], (camera_offset[1] + surface.get_height()) // GRID_CELL_SIZE + 1)

    # Draw the grid
    for x in range(start_x, end_x + 1):
        pygame.draw.line(surface, WHITE, 
                         (x * GRID_CELL_SIZE - camera_offset[0], 0), 
                         (x * GRID_CELL_SIZE - camera_offset[0], surface.get_height()))
    for y in range(start_y, end_y + 1):
        pygame.draw.line(surface, WHITE, 
                         (0, y * GRID_CELL_SIZE - camera_offset[1]), 
                         (surface.get_width(), y * GRID_CELL_SIZE - camera_offset[1]))

    # Draw the walls and structures
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if game_map[x][y] == 1:
                pygame.draw.rect(surface, BLUE, (
                    x * GRID_CELL_SIZE - camera_offset[0],
                    y * GRID_CELL_SIZE - camera_offset[1],
                    GRID_CELL_SIZE, GRID_CELL_SIZE
                ))

    # Draw the player
    pygame.draw.rect(surface, RED, (
        player_pos[0] * GRID_CELL_SIZE - camera_offset[0],
        player_pos[1] * GRID_CELL_SIZE - camera_offset[1],
        GRID_CELL_SIZE, GRID_CELL_SIZE
    ))

def main():
    global screen  # Declare screen as global
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen object with the new size
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
                
                # Check if the new position is valid (within bounds and not a wall)
                if (0 <= new_pos[0] < MAP_SIZE[0] and 
                    0 <= new_pos[1] < MAP_SIZE[1] and 
                    game_map[new_pos[0]][new_pos[1]] == 0):
                    player_pos[:] = new_pos

        # Get camera offset
        camera_offset = get_camera_offset(screen.get_size())

        # Draw the game
        draw_game(screen, camera_offset)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()