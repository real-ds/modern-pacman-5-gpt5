"""Main game class and loop"""
import pygame
import sys
from src.config import *
from src.levels.maze import Maze
from src.entities.player import Player
from src.entities.ghost_ai import Blinky, Pinky, Inky, Clyde
from src.utils.collision import check_ghost_collision

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PAC-MAN - Retro Futuristic Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        # Calculate maze offset to center it
        maze_pixel_width = MAZE_WIDTH * TILE_SIZE
        maze_pixel_height = MAZE_HEIGHT * TILE_SIZE
        self.offset_x = (SCREEN_WIDTH - maze_pixel_width) // 2
        self.offset_y = (SCREEN_HEIGHT - maze_pixel_height) // 2 + 50  # Extra space for HUD

        # Initialize game objects
        self.maze = Maze()

        # Spawn player in center-bottom area
        player_start_x = 14 * TILE_SIZE  # Center of maze
        player_start_y = 23 * TILE_SIZE  # Bottom area
        self.player = Player(player_start_x, player_start_y, self.maze)

        # Spawn ghosts in ghost house (center area)
        ghost_house_y = 14 * TILE_SIZE
        self.ghosts = [
            Blinky(13 * TILE_SIZE, ghost_house_y, self.maze),
            Pinky(14 * TILE_SIZE, ghost_house_y, self.maze),
            Inky(15 * TILE_SIZE, ghost_house_y, self.maze),
            Clyde(16 * TILE_SIZE, ghost_house_y, self.maze)
        ]

        # Game state
        self.death_timer = 0
        self.respawn_delay = 2000  # 2 seconds

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.dt = self.clock.tick(FPS) / 1000.0

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game state"""
        # Handle death timer
        if self.death_timer > 0:
            self.death_timer -= self.dt * 1000
            if self.death_timer <= 0:
                self.respawn_player()
            return

        self.player.handle_input()
        self.player.update(self.dt)

        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.dt, self.player)

        # Check if player collected power pellet
        if self.player.powered_up:
            for ghost in self.ghosts:
                if ghost.state not in ["frightened", "eaten"]:
                    ghost.set_frightened(self.player.power_timer)

        # Check ghost collisions
        collision_ghost = check_ghost_collision(self.player, self.ghosts)
        if collision_ghost:
            self.player.lives -= 1
            if self.player.lives > 0:
                self.death_timer = self.respawn_delay
            else:
                self.running = False  # Game over

    def respawn_player(self):
        """Respawn player after death"""
        player_start_x = 14 * TILE_SIZE
        player_start_y = 23 * TILE_SIZE
        self.player.x = player_start_x
        self.player.y = player_start_y
        self.player.direction = (0, 0)
        self.player.next_direction = (0, 0)
        self.player.powered_up = False
        self.player.power_timer = 0

        # Reset ghosts
        for ghost in self.ghosts:
            ghost.reset_position()

    def render(self):
        """Render game"""
        self.screen.fill(BLACK)

        # Render maze
        self.maze.render(self.screen, self.offset_x, self.offset_y)

        # Render ghosts
        for ghost in self.ghosts:
            ghost.render(self.screen, self.offset_x, self.offset_y)

        # Render player
        self.player.render(self.screen, self.offset_x, self.offset_y)

        # Render HUD info (basic for now)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"SCORE: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (20, 10))

        lives_text = font.render(f"LIVES: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

        # Show power-up status
        if self.player.powered_up:
            power_text = font.render(f"POWER: {int(self.player.power_timer / 1000)}s", True, NEON_YELLOW)
            self.screen.blit(power_text, (SCREEN_WIDTH // 2 - 80, 10))

        pygame.display.flip()

    def quit(self):
        """Clean up and quit"""
        pygame.quit()
        sys.exit()
