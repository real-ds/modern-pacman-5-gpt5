"""Player power-up items"""
import pygame
import random
from src.config import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type  # "speed", "shield", "freeze"
        self.duration = 5000  # milliseconds
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10000  # disappears after 10 seconds

    def check_collision(self, player):
        """Check if player collected power-up"""
        dist = ((self.x - player.x)**2 + (self.y - player.y)**2)**0.5
        return dist < (player.radius + 10)

    def apply_effect(self, player):
        """Apply power-up effect to player"""
        if self.type == "speed":
            player.original_speed = player.speed
            player.speed = PLAYER_SPEED * 1.5
            player.powerup_type = "speed"
        elif self.type == "shield":
            player.has_shield = True
            player.powerup_type = "shield"
        elif self.type == "freeze":
            player.freeze_active = True
            player.powerup_type = "freeze"

        player.powerup_timer = self.duration
        self.collected = True

    def is_expired(self):
        """Check if power-up has expired"""
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def render(self, screen, offset_x=0, offset_y=0):
        """Render power-up"""
        if self.collected:
            return

        px = offset_x + int(self.x)
        py = offset_y + int(self.y)

        # Choose color and symbol based on type
        if self.type == "speed":
            color = NEON_GREEN
            symbol = "S"
        elif self.type == "shield":
            color = NEON_BLUE
            symbol = "D"  # D for Defense
        elif self.type == "freeze":
            color = NEON_PURPLE
            symbol = "F"

        # Draw power-up with pulsing effect
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 to 1 and back
        size = int(12 + pulse * 3)

        pygame.draw.circle(screen, color, (px, py), size)
        pygame.draw.circle(screen, WHITE, (px, py), size, 2)

        # Draw symbol
        font = pygame.font.Font(None, 24)
        text = font.render(symbol, True, BLACK)
        text_rect = text.get_rect(center=(px, py))
        screen.blit(text, text_rect)

class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_interval = 15000  # Spawn every 15 seconds

    def update(self, dt, maze, player, ghosts):
        """Update power-up system"""
        self.spawn_timer += dt * 1000

        # Spawn new power-up
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_random_powerup(maze)
            self.spawn_timer = 0

        # Update existing power-ups
        for powerup in self.powerups[:]:
            if powerup.is_expired():
                self.powerups.remove(powerup)
            elif powerup.check_collision(player):
                powerup.apply_effect(player)
                self.powerups.remove(powerup)

        # Update player power-up effects
        if hasattr(player, 'powerup_timer') and hasattr(player, 'powerup_type') and player.powerup_type:
            player.powerup_timer -= dt * 1000

            if player.powerup_timer <= 0:
                self.remove_powerup_effect(player, ghosts)

        # Apply freeze effect to ghosts
        if hasattr(player, 'freeze_active') and player.freeze_active:
            for ghost in ghosts:
                if ghost.state not in ["eaten"]:
                    ghost.speed = GHOST_SPEED * 0.3  # 70% slower

    def spawn_random_powerup(self, maze):
        """Spawn a random power-up in valid location"""
        powerup_types = ["speed", "shield", "freeze"]
        powerup_type = random.choice(powerup_types)

        # Find valid spawn location
        attempts = 0
        while attempts < 50:  # Limit attempts to avoid infinite loop
            x = random.randint(2, MAZE_WIDTH - 2) * TILE_SIZE + TILE_SIZE // 2
            y = random.randint(2, MAZE_HEIGHT - 2) * TILE_SIZE + TILE_SIZE // 2

            grid_x = int(x / TILE_SIZE)
            grid_y = int(y / TILE_SIZE)

            if maze.is_walkable(grid_x, grid_y):
                self.powerups.append(PowerUp(x, y, powerup_type))
                break
            attempts += 1

    def remove_powerup_effect(self, player, ghosts):
        """Remove power-up effect from player"""
        if hasattr(player, 'powerup_type') and player.powerup_type:
            if player.powerup_type == "speed":
                if hasattr(player, 'original_speed'):
                    player.speed = player.original_speed
                else:
                    player.speed = PLAYER_SPEED
            elif player.powerup_type == "shield":
                player.has_shield = False
            elif player.powerup_type == "freeze":
                player.freeze_active = False
                # Restore ghost speeds
                for ghost in ghosts:
                    if ghost.state != "frightened":
                        ghost.speed = GHOST_SPEED

            player.powerup_type = None

    def render(self, screen, offset_x=0, offset_y=0):
        """Render all power-ups"""
        for powerup in self.powerups:
            powerup.render(screen, offset_x, offset_y)
