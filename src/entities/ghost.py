"""Base ghost class"""
import pygame
import random
from src.config import *

class Ghost:
    def __init__(self, x, y, color, name, maze):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.color = color
        self.name = name
        self.maze = maze
        self.speed = GHOST_SPEED
        self.direction = (0, 0)
        self.state = "scatter"  # scatter, chase, frightened, eaten
        self.frightened_timer = 0
        self.radius = GHOST_RADIUS
        self.target = (0, 0)
        self.mode_timer = 0
        self.mode_duration = 7000  # Switch modes every 7 seconds

    def update(self, dt, player):
        """Update ghost behavior"""
        # Update mode timer (switch between scatter and chase)
        if self.state in ["scatter", "chase"]:
            self.mode_timer += dt * 1000
            if self.mode_timer >= self.mode_duration:
                self.mode_timer = 0
                self.state = "chase" if self.state == "scatter" else "scatter"

        # Update frightened timer
        if self.state == "frightened":
            self.frightened_timer -= dt * 1000
            if self.frightened_timer <= 0:
                self.state = "scatter"
                self.speed = GHOST_SPEED

        # Update AI behavior
        self.update_ai(player)

        # Move ghost
        self.move()

    def update_ai(self, player):
        """Override in subclasses for unique behaviors"""
        pass

    def move(self):
        """Move ghost towards target"""
        # Check if at intersection (tile center)
        grid_x = int(self.x / TILE_SIZE)
        grid_y = int(self.y / TILE_SIZE)
        tile_center_x = grid_x * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = grid_y * TILE_SIZE + TILE_SIZE // 2

        # Allow direction change at intersections
        dist_to_center = abs(self.x - tile_center_x) + abs(self.y - tile_center_y)
        if dist_to_center < 3:  # Close enough to center
            self.choose_direction()

        # Move in current direction
        if self.can_move(self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
        else:
            # Stuck, choose new direction immediately
            self.choose_direction()

        # Wrap around edges
        self.x = self.x % (MAZE_WIDTH * TILE_SIZE)

    def can_move(self, direction):
        """Check if movement is valid"""
        if direction == (0, 0):
            return False

        next_x = self.x + direction[0] * (self.radius + 2)
        next_y = self.y + direction[1] * (self.radius + 2)

        grid_x = int(next_x / TILE_SIZE)
        grid_y = int(next_y / TILE_SIZE)

        return self.maze.is_walkable(grid_x, grid_y)

    def choose_direction(self):
        """Choose next direction"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        valid_dirs = [d for d in directions if self.can_move(d) and d != self.reverse_direction()]

        if not valid_dirs:
            # If no valid direction except reverse, allow reverse
            valid_dirs = [d for d in directions if self.can_move(d)]

        if valid_dirs:
            if self.state == "frightened":
                self.direction = random.choice(valid_dirs)
            else:
                # Choose direction closest to target
                best_dir = valid_dirs[0]
                best_dist = float('inf')

                for d in valid_dirs:
                    next_x = self.x + d[0] * TILE_SIZE
                    next_y = self.y + d[1] * TILE_SIZE
                    dist = ((next_x - self.target[0])**2 + (next_y - self.target[1])**2)**0.5

                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d

                self.direction = best_dir

    def reverse_direction(self):
        """Get reverse of current direction"""
        return (-self.direction[0], -self.direction[1])

    def set_frightened(self, duration):
        """Set ghost to frightened mode"""
        if self.state != "eaten":
            self.state = "frightened"
            self.frightened_timer = duration
            self.speed = GHOST_FRIGHTENED_SPEED
            self.direction = self.reverse_direction()

    def reset_position(self):
        """Reset ghost to starting position"""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = (0, 0)
        self.state = "scatter"
        self.speed = GHOST_SPEED
        self.mode_timer = 0

    def render(self, screen, offset_x=0, offset_y=0):
        """Render the ghost"""
        px = offset_x + int(self.x)
        py = offset_y + int(self.y)

        # Change color based on state
        color = self.color
        if self.state == "frightened":
            # Flash between blue and white when frightened
            if self.frightened_timer < 2000:  # Flash faster near end
                flash = int(self.frightened_timer / 100) % 2
            else:
                flash = int(self.frightened_timer / 200) % 2
            color = NEON_BLUE if flash else WHITE
        elif self.state == "eaten":
            color = GRAY

        # Draw ghost body
        pygame.draw.circle(screen, color, (px, py), self.radius)

        # Draw eyes (unless eaten)
        if self.state != "eaten":
            eye_offset = 3
            eye_size = 2 if self.state != "frightened" else 1
            pygame.draw.circle(screen, WHITE if self.state != "frightened" else BLACK,
                             (px - eye_offset, py - 2), eye_size)
            pygame.draw.circle(screen, WHITE if self.state != "frightened" else BLACK,
                             (px + eye_offset, py - 2), eye_size)
