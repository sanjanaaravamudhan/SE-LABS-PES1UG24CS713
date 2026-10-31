
"""Ball movement and collision geometry for Brick Breaker."""

import pygame


class Ball:
    """Represent the moving ball."""

    def __init__(self, x, y, radius=8):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = 0.0
        self.vy = 0.0

    def move(self):
        """Update the ball's position using its velocity."""
        self.x += self.vx
        self.y += self.vy

    def rect(self):
        """Return the ball's bounding rectangle."""
        diameter = self.radius * 2
        return pygame.Rect(
            round(self.x - self.radius),
            round(self.y - self.radius),
            diameter,
            diameter,
        )
