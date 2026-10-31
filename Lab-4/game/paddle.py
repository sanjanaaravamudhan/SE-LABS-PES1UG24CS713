
"""Player-controlled paddle for Brick Breaker."""


import pygame


class Paddle:
    """Represent and control the player's paddle."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dx, screen_width):
        """Move the paddle while keeping it inside the screen."""
        self.x += dx
        self.x = max(0, min(self.x, screen_width - self.width))

    def rect(self):
        """Return the paddle's collision rectangle."""
        return pygame.Rect(
            round(self.x),
            round(self.y),
            self.width,
            self.height,
        )
