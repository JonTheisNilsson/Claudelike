import pygame
import sys

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

# Create the game window (resizable)
screen = pygame.display.set_mode(INITIAL_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Grid Game")

# Player position (in grid coordinates)
player_pos = [MAP_SIZE[0] // 2, MAP_SIZE[1] // 2]

# Camera offset
camera_offset = [0, 0]

def draw_grid(surface, offset_x, offset_y, width, height):
    # Draw vertical lines
    for x in range(0, MAP_SIZE[0] * GRID_CELL_SIZE, GRID_CELL_SIZE):
        pygame.draw.line(surface, WHITE, 
                         (x - offset_x, 0), 
                         (x - offset_x, height))
    
    # Draw horizontal lines
    for y in range(0, MAP_SIZE[1] * GRID_CELL_SIZE, GRID_CELL_SIZE):
        pygame.draw.line(surface, WHITE, 
                         (0, y - offset_y), 
                         (width, y - offset_y))

def update_camera(window_size):
    camera_offset[0] = player_pos[0] * GRID_CELL_SIZE - window_size[0] // 2
    camera_offset[1] = player_pos[1] * GRID_CELL_SIZE - window_size[1] // 2

def main():
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
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and player_pos[1] < MAP_SIZE[1] - 1:
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[0] < MAP_SIZE[0] - 1:
                    player_pos[0] += 1

        # Update camera position
        update_camera(screen.get_size())

        # Clear the screen
        screen.fill(BLACK)

        # Draw the grid
        draw_grid(screen, camera_offset[0], camera_offset[1], *screen.get_size())

        # Draw the player
        pygame.draw.rect(screen, RED, (
            player_pos[0] * GRID_CELL_SIZE - camera_offset[0],
            player_pos[1] * GRID_CELL_SIZE - camera_offset[1],
            GRID_CELL_SIZE, GRID_CELL_SIZE
        ))

        # Draw map boundaries
        pygame.draw.rect(screen, GREEN, (
            0 - camera_offset[0],
            0 - camera_offset[1],
            MAP_SIZE[0] * GRID_CELL_SIZE,
            MAP_SIZE[1] * GRID_CELL_SIZE
        ), 2)  # 2 is the line thickness

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()