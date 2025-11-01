"""Specific ghost AI implementations"""
from src.entities.ghost import Ghost
from src.config import *

class Blinky(Ghost):
    """Red ghost - Aggressive chaser"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, NEON_PINK, "Blinky", maze)

    def update_ai(self, player):
        """Chase player directly"""
        if self.state == "chase":
            self.target = (player.x, player.y)
        elif self.state == "scatter":
            self.target = (MAZE_WIDTH * TILE_SIZE, 0)  # Top right corner
        elif self.state == "eaten":
            self.target = (self.start_x, self.start_y)

class Pinky(Ghost):
    """Pink ghost - Ambusher"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, NEON_PINK, "Pinky", maze)

    def update_ai(self, player):
        """Target ahead of player"""
        if self.state == "chase":
            # Target 4 tiles ahead of player
            ahead_x = player.x + player.direction[0] * TILE_SIZE * 4
            ahead_y = player.y + player.direction[1] * TILE_SIZE * 4
            self.target = (ahead_x, ahead_y)
        elif self.state == "scatter":
            self.target = (0, 0)  # Top left corner
        elif self.state == "eaten":
            self.target = (self.start_x, self.start_y)

class Inky(Ghost):
    """Cyan ghost - Strategic"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, NEON_BLUE, "Inky", maze)

    def update_ai(self, player):
        """Complex targeting based on player position"""
        if self.state == "chase":
            # Target 2 tiles ahead of player
            ahead_x = player.x + player.direction[0] * TILE_SIZE * 2
            ahead_y = player.y + player.direction[1] * TILE_SIZE * 2
            self.target = (ahead_x, ahead_y)
        elif self.state == "scatter":
            self.target = (MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE)  # Bottom right
        elif self.state == "eaten":
            self.target = (self.start_x, self.start_y)

class Clyde(Ghost):
    """Orange ghost - Random/Shy"""
    def __init__(self, x, y, maze):
        super().__init__(x, y, NEON_ORANGE, "Clyde", maze)

    def update_ai(self, player):
        """Chase when far, scatter when close"""
        if self.state == "chase":
            dist = ((self.x - player.x)**2 + (self.y - player.y)**2)**0.5

            if dist > TILE_SIZE * 8:
                # Chase player when far away
                self.target = (player.x, player.y)
            else:
                # Scatter when close
                self.target = (0, MAZE_HEIGHT * TILE_SIZE)  # Bottom left
        elif self.state == "scatter":
            self.target = (0, MAZE_HEIGHT * TILE_SIZE)  # Bottom left
        elif self.state == "eaten":
            self.target = (self.start_x, self.start_y)
