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
GREEN = (0, 255, 0)
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

# Camera offset
camera_offset = [0, 0]

def draw_grid(surface, offset_x, offset_y, width, height):
    # Draw vertical lines
    for x in range(MAP_SIZE[0] + 1):
        pygame.draw.line(surface, WHITE, 
                         (x * GRID_CELL_SIZE + offset_x, offset_y), 
                         (x * GRID_CELL_SIZE + offset_x, MAP_SIZE[1] * GRID_CELL_SIZE + offset_y))
    
    # Draw horizontal lines
    for y in range(MAP_SIZE[1] + 1):
        pygame.draw.line(surface, WHITE, 
                         (offset_x, y * GRID_CELL_SIZE + offset_y), 
                         (MAP_SIZE[0] * GRID_CELL_SIZE + offset_x, y * GRID_CELL_SIZE + offset_y))

def update_camera(window_size):
    map_pixel_width = MAP_SIZE[0] * GRID_CELL_SIZE
    map_pixel_height = MAP_SIZE[1] * GRID_CELL_SIZE

    if window_size[0] >= map_pixel_width:
        camera_offset[0] = (window_size[0] - map_pixel_width) // 2
    else:
        camera_offset[0] = max(0, min(player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2, map_pixel_width - window_size[0]))

    if window_size[1] >= map_pixel_height:
        camera_offset[1] = (window_size[1] - map_pixel_height) // 2
    else:
        camera_offset[1] = max(0, min(player_pos[1] * GRID_CELL_SIZE - window_size[1] // 2, map_pixel_height - window_size[1]))

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

        # Update camera position
        update_camera(screen.get_size())

        # Clear the screen
        screen.fill(BLACK)

        # Draw the grid
        draw_grid(screen, camera_offset[0], camera_offset[1], *screen.get_size())

        # Draw the walls and structures
        for x in range(MAP_SIZE[0]):
            for y in range(MAP_SIZE[1]):
                if game_map[x][y] == 1:
                    pygame.draw.rect(screen, BLUE, (
                        x * GRID_CELL_SIZE + camera_offset[0],
                        y * GRID_CELL_SIZE + camera_offset[1],
                        GRID_CELL_SIZE, GRID_CELL_SIZE
                    ))

        # Draw the player
        pygame.draw.rect(screen, RED, (
            player_pos[0] * GRID_CELL_SIZE + camera_offset[0],
            player_pos[1] * GRID_CELL_SIZE + camera_offset[1],
            GRID_CELL_SIZE, GRID_CELL_SIZE
        ))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()