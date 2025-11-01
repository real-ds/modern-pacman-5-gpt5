"""Main game class and loop"""
import pygame
import sys
from src.config import *
from src.levels.maze import Maze
from src.entities.player import Player

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
        self.player.handle_input()
        self.player.update(self.dt)

    def render(self):
        """Render game"""
        self.screen.fill(BLACK)

        # Render maze
        self.maze.render(self.screen, self.offset_x, self.offset_y)

        # Render player
        self.player.render(self.screen, self.offset_x, self.offset_y)

        # Render HUD info (basic for now)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"SCORE: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (20, 10))

        lives_text = font.render(f"LIVES: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()

    def quit(self):
        """Clean up and quit"""
        pygame.quit()
        sys.exit()
