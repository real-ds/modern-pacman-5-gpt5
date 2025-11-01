"""Game configuration and settings"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
FPS = 60

# Colors (Retro-Futuristic palette)
BLACK = (10, 10, 15)
NEON_BLUE = (0, 240, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 140, 0)
NEON_PURPLE = (191, 64, 191)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Maze settings
TILE_SIZE = 25
MAZE_WIDTH = 28  # Classic Pac-Man dimensions
MAZE_HEIGHT = 31

# Player settings
PLAYER_SPEED = 2.5
PLAYER_RADIUS = 10

# Ghost settings
GHOST_SPEED = 2.0
GHOST_FRIGHTENED_SPEED = 1.5
GHOST_RADIUS = 10

# Game mechanics
POWER_PELLET_DURATION = 8000  # milliseconds
INVINCIBILITY_FLASH_SPEED = 100  # milliseconds
LEVEL_CLEAR_DELAY = 2000  # milliseconds
