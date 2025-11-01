"""Level progression and management"""
from src.config import *
from src.levels.maze import Maze

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.difficulty_multiplier = 1.0

    def get_current_level(self):
        """Get current level number"""
        return self.current_level

    def get_difficulty(self):
        """Get current difficulty multiplier"""
        return self.difficulty_multiplier

    def next_level(self):
        """Advance to next level"""
        self.current_level += 1
        # Increase difficulty by 10% each level
        self.difficulty_multiplier = 1.0 + (self.current_level - 1) * 0.1
        return self.current_level

    def adjust_ghost_difficulty(self, ghosts):
        """Adjust ghost behavior for current level"""
        for ghost in ghosts:
            # Increase ghost speed based on level
            ghost.speed = GHOST_SPEED * self.difficulty_multiplier
            # Decrease mode switch time (more aggressive)
            ghost.mode_duration = max(3000, 7000 - (self.current_level - 1) * 500)

    def reset(self):
        """Reset to level 1"""
        self.current_level = 1
        self.difficulty_multiplier = 1.0
