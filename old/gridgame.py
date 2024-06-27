import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (400, 400)
GRID_SIZE = 10
CELL_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Grid Game")

# Player position
player_pos = [GRID_SIZE // 2, GRID_SIZE // 2]

# Main game loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and player_pos[1] < GRID_SIZE - 1:
                    player_pos[1] += 1
                elif event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE - 1:
                    player_pos[0] += 1

        # Clear the screen
        screen.fill(BLACK)

        # Draw the grid
        for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_SIZE[1]))
        for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WINDOW_SIZE[0], y))

        # Draw the player
        pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()