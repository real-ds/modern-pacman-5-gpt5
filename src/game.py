"""Main game class and loop"""
import pygame
import sys
from src.config import *
from src.levels.maze import Maze
from src.entities.player import Player
from src.entities.ghost_ai import Blinky, Pinky, Inky, Clyde
from src.utils.collision import check_ghost_collision
from src.ui.hud import HUD
from src.ui.menus import MenuManager
from src.ui.particles import ParticleSystem
from src.levels.level_manager import LevelManager
from src.entities.powerup import PowerUpManager

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

        # UI Components
        self.hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.menu_manager = MenuManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particles = ParticleSystem()

        # Game systems
        self.level_manager = LevelManager()
        self.powerup_manager = PowerUpManager()

        # Game state
        self.state = "menu"  # menu, playing, paused, game_over
        self.combo = 1
        self.death_timer = 0
        self.respawn_delay = 2000  # 2 seconds
        self.level_complete_timer = 0

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
                    if self.state == "menu":
                        self.running = False
                    elif self.state == "game_over":
                        self.running = False
                    else:
                        self.state = "menu"

                elif event.key == pygame.K_SPACE:
                    if self.state == "menu":
                        self.start_game()
                    elif self.state == "game_over":
                        self.restart_game()

                elif event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"

    def start_game(self):
        """Start a new game"""
        self.state = "playing"

    def restart_game(self):
        """Restart game after game over"""
        # Reset everything
        self.maze = Maze()
        player_start_x = 14 * TILE_SIZE
        player_start_y = 23 * TILE_SIZE
        self.player = Player(player_start_x, player_start_y, self.maze)

        ghost_house_y = 14 * TILE_SIZE
        self.ghosts = [
            Blinky(13 * TILE_SIZE, ghost_house_y, self.maze),
            Pinky(14 * TILE_SIZE, ghost_house_y, self.maze),
            Inky(15 * TILE_SIZE, ghost_house_y, self.maze),
            Clyde(16 * TILE_SIZE, ghost_house_y, self.maze)
        ]

        self.level_manager.reset()
        self.powerup_manager = PowerUpManager()
        self.combo = 1
        self.death_timer = 0
        self.level_complete_timer = 0
        self.particles = ParticleSystem()
        self.state = "playing"

    def update(self):
        """Update game state"""
        # Only update game when playing
        if self.state != "playing":
            return

        # Update particles
        self.particles.update()

        # Handle death timer
        if self.death_timer > 0:
            self.death_timer -= self.dt * 1000
            if self.death_timer <= 0:
                self.respawn_player()
            return

        # Track previous score for particle effects
        prev_score = self.player.score

        self.player.handle_input()
        self.player.update(self.dt)

        # Emit particles on score change
        if self.player.score > prev_score:
            self.particles.emit(
                self.offset_x + self.player.x,
                self.offset_y + self.player.y,
                NEON_YELLOW if not self.player.powered_up else NEON_GREEN,
                count=3
            )

        # Update power-ups
        self.powerup_manager.update(self.dt, self.maze, self.player, self.ghosts)

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
            # Check if player has shield
            if hasattr(self.player, 'has_shield') and self.player.has_shield:
                # Shield protects player
                self.player.has_shield = False
                self.powerup_manager.remove_powerup_effect(self.player, self.ghosts)
                # Emit shield break particles
                self.particles.emit(
                    self.offset_x + self.player.x,
                    self.offset_y + self.player.y,
                    NEON_BLUE,
                    count=15
                )
            else:
                # Player takes damage
                self.player.lives -= 1
                if self.player.lives > 0:
                    self.death_timer = self.respawn_delay
                    # Emit death particles
                    self.particles.emit(
                        self.offset_x + self.player.x,
                        self.offset_y + self.player.y,
                        NEON_PINK,
                        count=10
                    )
                else:
                    self.state = "game_over"

        # Check level completion
        pellets_remaining = sum(row.count(1) + row.count(2) for row in self.maze.layout)
        if pellets_remaining == 0:
            self.level_complete()

    def level_complete(self):
        """Handle level completion"""
        # Award bonus points
        self.player.score += 1000

        # Advance level
        self.level_manager.next_level()

        # Create new maze
        self.maze = Maze()

        # Reset player position
        player_start_x = 14 * TILE_SIZE
        player_start_y = 23 * TILE_SIZE
        self.player.x = player_start_x
        self.player.y = player_start_y
        self.player.direction = (0, 0)
        self.player.next_direction = (0, 0)
        self.player.powered_up = False
        self.player.power_timer = 0

        # Reset ghosts with increased difficulty
        ghost_house_y = 14 * TILE_SIZE
        self.ghosts = [
            Blinky(13 * TILE_SIZE, ghost_house_y, self.maze),
            Pinky(14 * TILE_SIZE, ghost_house_y, self.maze),
            Inky(15 * TILE_SIZE, ghost_house_y, self.maze),
            Clyde(16 * TILE_SIZE, ghost_house_y, self.maze)
        ]
        self.level_manager.adjust_ghost_difficulty(self.ghosts)

        # Reset power-ups
        self.powerup_manager = PowerUpManager()

        # Emit celebration particles
        for i in range(20):
            self.particles.emit(
                self.offset_x + self.player.x + (i - 10) * 20,
                self.offset_y + self.player.y,
                NEON_GREEN if i % 2 == 0 else NEON_YELLOW,
                count=5
            )

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
        if self.state == "menu":
            self.menu_manager.render_start_menu(self.screen)
        elif self.state == "game_over":
            self.menu_manager.render_game_over(self.screen, self.player.score, self.level_manager.get_current_level())
        else:
            # Render game (playing or paused)
            self.screen.fill(BLACK)

            # Render maze
            self.maze.render(self.screen, self.offset_x, self.offset_y)

            # Render power-ups
            self.powerup_manager.render(self.screen, self.offset_x, self.offset_y)

            # Render ghosts
            for ghost in self.ghosts:
                ghost.render(self.screen, self.offset_x, self.offset_y)

            # Render player
            self.player.render(self.screen, self.offset_x, self.offset_y)

            # Render particles
            self.particles.render(self.screen)

            # Render HUD
            self.hud.render(self.screen, self.player, self.level_manager.get_current_level(), self.combo)

            # Render power-up indicator if active
            if hasattr(self.player, 'powerup_type') and self.player.powerup_type:
                font = pygame.font.Font(None, 24)
                powerup_name = self.player.powerup_type.upper()
                text = font.render(f"POWERUP: {powerup_name}", True, NEON_GREEN)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 80, 850))

            # Render pause overlay if paused
            if self.state == "paused":
                self.menu_manager.render_pause_menu(self.screen)

        pygame.display.flip()

    def quit(self):
        """Clean up and quit"""
        pygame.quit()
        sys.exit()
