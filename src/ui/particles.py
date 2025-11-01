"""Particle system for visual effects"""
import pygame
import random
from src.config import *

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = color
        self.life = 30  # frames
        self.size = random.randint(2, 4)

    def update(self):
        """Update particle position"""
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size - 0.1)

    def is_dead(self):
        """Check if particle should be removed"""
        return self.life <= 0

    def render(self, screen):
        """Render particle"""
        if self.life > 0:
            alpha = int(255 * (self.life / 30))
            # Pygame doesn't support per-pixel alpha easily, so we'll just draw the particle
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=5):
        """Emit particles"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)

    def render(self, screen):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen)
