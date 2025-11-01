"""Pac-Man player entity"""
import pygame
from src.config import *

class Player:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.speed = PLAYER_SPEED
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.radius = PLAYER_RADIUS
        self.score = 0
        self.lives = 3
        self.powered_up = False
        self.power_timer = 0

    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = (1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = (0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = (0, 1)

    def update(self, dt):
        """Update player position"""
        # Try to change direction
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        # Move in current direction
        if self.can_move(self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed

        # Wrap around edges
        self.x = self.x % (MAZE_WIDTH * TILE_SIZE)

        # Check for pellet collection
        self.check_pellet_collision()

        # Update power-up timer
        if self.powered_up:
            self.power_timer -= dt * 1000
            if self.power_timer <= 0:
                self.powered_up = False

    def can_move(self, direction):
        """Check if movement in direction is valid"""
        if direction == (0, 0):
            return False

        # Calculate next position
        next_x = self.x + direction[0] * (self.radius + 2)
        next_y = self.y + direction[1] * (self.radius + 2)

        # Convert to grid coordinates
        grid_x = int(next_x / TILE_SIZE)
        grid_y = int(next_y / TILE_SIZE)

        return self.maze.is_walkable(grid_x, grid_y)

    def check_pellet_collision(self):
        """Check and handle pellet collisions"""
        grid_x = int(self.x / TILE_SIZE)
        grid_y = int(self.y / TILE_SIZE)

        pellet = self.maze.eat_pellet(grid_x, grid_y)

        if pellet == 1:  # Regular pellet
            self.score += 10
        elif pellet == 2:  # Power pellet
            self.score += 50
            self.powered_up = True
            self.power_timer = POWER_PELLET_DURATION

    def render(self, screen, offset_x=0, offset_y=0):
        """Render the player"""
        px = offset_x + int(self.x)
        py = offset_y + int(self.y)

        # Draw Pac-Man as a circle
        color = NEON_YELLOW if not self.powered_up else NEON_GREEN
        pygame.draw.circle(screen, color, (px, py), self.radius)

        # Draw mouth (simple animation)
        if self.direction != (0, 0):
            mouth_angle = 30  # degrees
            start_angle = 0

            if self.direction == (1, 0):  # Right
                start_angle = mouth_angle
            elif self.direction == (-1, 0):  # Left
                start_angle = 180 + mouth_angle
            elif self.direction == (0, -1):  # Up
                start_angle = 270 + mouth_angle
            elif self.direction == (0, 1):  # Down
                start_angle = 90 + mouth_angle
