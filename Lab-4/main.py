
"""Entry point for the Brick Breaker game."""

import pygame

from game.game_engine import GameEngine


def main():
    """Initialize Pygame and run the main game loop."""
    pygame.init()

    width, height = 640, 560
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Brick Breaker - Pygame Version")

    clock = pygame.time.Clock()
    fps = 60

    engine = GameEngine(width, height)

    running = True

    try:
        while running:
            for event in pygame.event.get():
                engine.handle_event(event)

                if engine.should_quit:
                    running = False

            if not running:
                break

            engine.handle_input()
            engine.update()
            engine.render(screen)

            pygame.display.flip()
            clock.tick(fps)

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
