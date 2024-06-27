# keymap.py
import pygame

# Movement keys
MOVE_UP = pygame.K_KP8
MOVE_DOWN = pygame.K_KP2
MOVE_LEFT = pygame.K_KP4
MOVE_RIGHT = pygame.K_KP6
MOVE_UP_LEFT = pygame.K_KP7
MOVE_UP_RIGHT = pygame.K_KP9
MOVE_DOWN_LEFT = pygame.K_KP1
MOVE_DOWN_RIGHT = pygame.K_KP3

# Alternative movement keys (arrow keys)
ALT_MOVE_UP = pygame.K_UP
ALT_MOVE_DOWN = pygame.K_DOWN
ALT_MOVE_LEFT = pygame.K_LEFT
ALT_MOVE_RIGHT = pygame.K_RIGHT

# Wait key
WAIT = pygame.K_KP5  # Numpad 5 for wait

MOVE_DIRECTIONS = {
    MOVE_UP: (0, -1),
    MOVE_DOWN: (0, 1),
    MOVE_LEFT: (-1, 0),
    MOVE_RIGHT: (1, 0),
    MOVE_UP_LEFT: (-1, -1),
    MOVE_UP_RIGHT: (1, -1),
    MOVE_DOWN_LEFT: (-1, 1),
    MOVE_DOWN_RIGHT: (1, 1),
    ALT_MOVE_UP: (0, -1),
    ALT_MOVE_DOWN: (0, 1),
    ALT_MOVE_LEFT: (-1, 0),
    ALT_MOVE_RIGHT: (1, 0)
}