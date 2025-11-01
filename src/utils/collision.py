"""Collision detection utilities"""
import math

def circle_collision(x1, y1, r1, x2, y2, r2):
    """Check collision between two circles"""
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist < (r1 + r2)

def check_ghost_collision(player, ghosts):
    """Check collisions between player and ghosts"""
    for ghost in ghosts:
        if circle_collision(player.x, player.y, player.radius,
                          ghost.x, ghost.y, ghost.radius):
            if ghost.state == "frightened":
                # Player eats ghost
                ghost.state = "eaten"
                ghost.reset_position()
                player.score += 200
            elif ghost.state not in ["eaten"]:
                # Ghost catches player
                return ghost
    return None
