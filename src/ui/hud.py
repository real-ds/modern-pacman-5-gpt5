"""Heads-up display"""
import pygame
from src.config import *

class HUD:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def render(self, screen, player, level=1, combo=1):
        """Render all HUD elements"""
        # Score
        score_text = self.font_large.render(f"SCORE: {player.score}", True, WHITE)
        screen.blit(score_text, (20, 10))

        # Lives
        lives_text = self.font_medium.render(f"LIVES:", True, WHITE)
        screen.blit(lives_text, (20, 60))
        for i in range(player.lives):
            pygame.draw.circle(screen, NEON_YELLOW, (120 + i * 30, 75), 10)

        # Level
        level_text = self.font_medium.render(f"LEVEL: {level}", True, NEON_BLUE)
        screen.blit(level_text, (self.width - 200, 10))

        # Combo multiplier
        if combo > 1:
            combo_text = self.font_large.render(f"x{combo} COMBO!", True, NEON_GREEN)
            text_rect = combo_text.get_rect(center=(self.width // 2, 50))
            screen.blit(combo_text, text_rect)

        # Power-up timer
        if player.powered_up:
            timer_width = 200
            timer_height = 20
            timer_x = (self.width - timer_width) // 2
            timer_y = self.height - 40

            # Background
            pygame.draw.rect(screen, GRAY, (timer_x, timer_y, timer_width, timer_height))

            # Fill based on remaining time
            fill_width = int((player.power_timer / POWER_PELLET_DURATION) * timer_width)
            pygame.draw.rect(screen, NEON_YELLOW, (timer_x, timer_y, fill_width, timer_height))

            # Border
            pygame.draw.rect(screen, WHITE, (timer_x, timer_y, timer_width, timer_height), 2)

            # Text
            power_text = self.font_small.render("POWER MODE!", True, WHITE)
            text_rect = power_text.get_rect(center=(self.width // 2, timer_y - 15))
            screen.blit(power_text, text_rect)
