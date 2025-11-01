"""Menu screens"""
import pygame
from src.config import *

class MenuManager:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)

    def render_start_menu(self, screen):
        """Render start menu"""
        screen.fill(BLACK)

        # Title
        title = self.font_title.render("PAC-MAN", True, NEON_YELLOW)
        title_rect = title.get_rect(center=(self.width // 2, 200))
        screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.font_medium.render("Retro Futuristic Edition", True, NEON_BLUE)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 280))
        screen.blit(subtitle, subtitle_rect)

        # Instructions
        play_text = self.font_large.render("Press SPACE to Start", True, WHITE)
        play_rect = play_text.get_rect(center=(self.width // 2, 400))
        screen.blit(play_text, play_rect)

        controls = [
            "WASD or Arrow Keys - Move",
            "P - Pause",
            "ESC - Quit"
        ]

        y_offset = 500
        for control in controls:
            text = self.font_medium.render(control, True, GRAY)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

    def render_pause_menu(self, screen):
        """Render pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_title.render("PAUSED", True, NEON_YELLOW)
        pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(pause_text, pause_rect)

        # Resume instruction
        resume_text = self.font_medium.render("Press P to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
        screen.blit(resume_text, resume_rect)

    def render_game_over(self, screen, score, level):
        """Render game over screen"""
        screen.fill(BLACK)

        # Game Over text
        game_over = self.font_title.render("GAME OVER", True, NEON_PINK)
        game_over_rect = game_over.get_rect(center=(self.width // 2, 200))
        screen.blit(game_over, game_over_rect)

        # Final score
        score_text = self.font_large.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.width // 2, 320))
        screen.blit(score_text, score_rect)

        # Level reached
        level_text = self.font_medium.render(f"Level Reached: {level}", True, NEON_BLUE)
        level_rect = level_text.get_rect(center=(self.width // 2, 380))
        screen.blit(level_text, level_rect)

        # Restart instruction
        restart_text = self.font_medium.render("Press SPACE to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(self.width // 2, 500))
        screen.blit(restart_text, restart_rect)

        # Quit instruction
        quit_text = self.font_medium.render("Press ESC to Quit", True, GRAY)
        quit_rect = quit_text.get_rect(center=(self.width // 2, 550))
        screen.blit(quit_text, quit_rect)
