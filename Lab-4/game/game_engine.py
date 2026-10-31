
"""Core game engine for the Brick Breaker game."""

import io
import math
import struct
import wave

import pygame

from .paddle import Paddle
from .ball import Ball
from .brick import Brick


WHITE = (255, 255, 255)
BG = (15, 15, 25)
BRICK_COLORS = [
    (200, 60, 60),
    (200, 140, 60),
    (200, 200, 60),
    (80, 180, 80),
    (80, 140, 200),
]

DIFFICULTIES = {
    "Easy": {"ball_speed": 3.5, "paddle_width": 130, "paddle_speed": 8},
    "Medium": {"ball_speed": 4.5, "paddle_width": 100, "paddle_speed": 7},
    "Hard": {"ball_speed": 6.0, "paddle_width": 80, "paddle_speed": 7},
}


class GameEngine:
    """Manage game objects, physics, sound, and game states."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.should_quit = False
        self.game_over = False
        self.result = None
        self.difficulty = "Medium"

        self._init_sounds()
        self._start_game(self.difficulty)

    def _init_sounds(self):
        """Create simple sound effects without external audio files."""
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                )

            self.sounds = {
                "wall": self._make_tone(550, 0.07),
                "paddle": self._make_tone(750, 0.09),
                "brick": self._make_tone(950, 0.12),
                "win": self._make_tone(1200, 0.30),
                "lose": self._make_tone(220, 0.35),
            }
        except pygame.error:
            # The game remains playable if audio is unavailable.
            self.sounds = {}

    @staticmethod
    def _make_tone(frequency, duration):
        """Generate a short WAV sound using a sine wave."""
        sample_rate = 22050
        sample_count = int(sample_rate * duration)
        samples = bytearray()

        for index in range(sample_count):
            fade = 1 - index / sample_count
            value = int(
                10000
                * fade
                * math.sin(2 * math.pi * frequency * index / sample_rate)
            )
            samples.extend(struct.pack("<h", value))

        audio = io.BytesIO()

        with wave.open(audio, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(bytes(samples))

        audio.seek(0)
        return pygame.mixer.Sound(file=audio)

    def _play_sound(self, name):
        """Play a sound effect when audio is available."""
        sound = self.sounds.get(name)
        if sound:
            sound.play()

    def _start_game(self, difficulty):
        """Reset the game using the selected difficulty."""
        self.difficulty = difficulty
        settings = DIFFICULTIES[difficulty]

        paddle_width = settings["paddle_width"]
        self.paddle = Paddle(
            self.width // 2 - paddle_width // 2,
            self.height - 30,
            paddle_width,
            14,
        )
        self.paddle.speed = settings["paddle_speed"]

        self.ball = Ball(
            self.width // 2,
            self.height - 50,
            radius=8,
        )
        self.ball.vx = settings["ball_speed"]
        self.ball.vy = -settings["ball_speed"]

        self.rows, self.cols = 5, 8
        self.bricks = self._build_bricks(self.rows, self.cols)

        self.lives = 3
        self.score = 0
        self.game_over = False
        self.result = None

    def _build_bricks(self, rows, cols):
        """Create the grid of destructible bricks."""
        bricks = []
        margin, gap, top = 30, 6, 60

        brick_width = (
            self.width - margin * 2 - gap * (cols - 1)
        ) // cols
        brick_height = 22

        for row in range(rows):
            for col in range(cols):
                x = margin + col * (brick_width + gap)
                y = top + row * (brick_height + gap)
                bricks.append(
                    Brick(x, y, brick_width, brick_height)
                )

        return bricks

    def handle_event(self, event):
        """Handle window events and game-over menu selections."""
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.should_quit = True
            return

        if not self.game_over:
            return

        difficulty_keys = {
            pygame.K_1: "Easy",
            pygame.K_2: "Medium",
            pygame.K_3: "Hard",
        }

        if event.key in difficulty_keys:
            self._start_game(difficulty_keys[event.key])
        elif event.key in (pygame.K_q, pygame.K_x):
            self.should_quit = True

    def handle_input(self):
        """Move the paddle using arrow keys or A/D."""
        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move(-self.paddle.speed, self.width)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move(self.paddle.speed, self.width)

    def _resolve_collision(self, target, previous_x, previous_y):
        """Resolve a collision according to the side that was hit."""
        ball_rect = self.ball.rect()
        target_rect = target.rect()

        overlap_x = min(
            ball_rect.right, target_rect.right
        ) - max(ball_rect.left, target_rect.left)

        overlap_y = min(
            ball_rect.bottom, target_rect.bottom
        ) - max(ball_rect.top, target_rect.top)

        previous_left = previous_x - self.ball.radius
        previous_right = previous_x + self.ball.radius
        previous_top = previous_y - self.ball.radius
        previous_bottom = previous_y + self.ball.radius

        # Ball entered from above.
        if previous_bottom <= target_rect.top:
            self.ball.y = target_rect.top - self.ball.radius
            self.ball.vy = -abs(self.ball.vy)
            return "vertical"

        # Ball entered from below.
        if previous_top >= target_rect.bottom:
            self.ball.y = target_rect.bottom + self.ball.radius
            self.ball.vy = abs(self.ball.vy)
            return "vertical"

        # Ball entered from the left.
        if previous_right <= target_rect.left:
            self.ball.x = target_rect.left - self.ball.radius
            self.ball.vx = -abs(self.ball.vx)
            return "horizontal"

        # Ball entered from the right.
        if previous_left >= target_rect.right:
            self.ball.x = target_rect.right + self.ball.radius
            self.ball.vx = abs(self.ball.vx)
            return "horizontal"

        # Fallback for overlapping or corner collisions.
        if overlap_x < overlap_y:
            if self.ball.x < target_rect.centerx:
                self.ball.x = target_rect.left - self.ball.radius
                self.ball.vx = -abs(self.ball.vx)
            else:
                self.ball.x = target_rect.right + self.ball.radius
                self.ball.vx = abs(self.ball.vx)
            return "horizontal"

        if self.ball.y < target_rect.centery:
            self.ball.y = target_rect.top - self.ball.radius
            self.ball.vy = -abs(self.ball.vy)
        else:
            self.ball.y = target_rect.bottom + self.ball.radius
            self.ball.vy = abs(self.ball.vy)

        return "vertical"

    def update(self):
        """Update ball movement, collisions, score, and lives."""
        if self.game_over:
            return

        previous_x = self.ball.x
        previous_y = self.ball.y

        self.ball.move()

        # Left and right wall collisions.
        if self.ball.x - self.ball.radius <= 0:
            self.ball.x = self.ball.radius
            self.ball.vx = abs(self.ball.vx)
            self._play_sound("wall")

        elif self.ball.x + self.ball.radius >= self.width:
            self.ball.x = self.width - self.ball.radius
            self.ball.vx = -abs(self.ball.vx)
            self._play_sound("wall")

        # Top wall collision.
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.vy = abs(self.ball.vy)
            self._play_sound("wall")

        # Paddle collision: only when the ball is travelling downward.
        if (
            self.ball.vy > 0
            and self.ball.rect().colliderect(self.paddle.rect())
        ):
            self._resolve_collision(
                self.paddle, previous_x, previous_y
            )

            if self.ball.vy < 0:
                hit_position = (
                    self.ball.x - self.paddle.rect().centerx
                ) / (self.paddle.width / 2)

                self.ball.vx += hit_position * 1.5
                self.ball.vx = max(-7, min(7, self.ball.vx))
                self._play_sound("paddle")

        # Brick collision: destroy one brick and resolve its impact side.
        for brick in self.bricks:
            if (
                brick.alive
                and self.ball.rect().colliderect(brick.rect())
            ):
                self._resolve_collision(
                    brick, previous_x, previous_y
                )
                brick.alive = False
                self.score += 1
                self._play_sound("brick")
                break

        # Ball has fallen below the screen.
        if self.ball.y - self.ball.radius > self.height:
            self.lives -= 1

            if self.lives <= 0:
                self._finish_game("lose")
            else:
                self._reset_ball()

        # All bricks destroyed means the player wins.
        if not self.game_over and all(
            not brick.alive for brick in self.bricks
        ):
            self._finish_game("win")

    def _reset_ball(self):
        """Reset the ball position after losing a life."""
        settings = DIFFICULTIES[self.difficulty]

        self.ball.x = self.width // 2
        self.ball.y = self.height - 50
        self.ball.vx = settings["ball_speed"]
        self.ball.vy = -settings["ball_speed"]

    def _finish_game(self, result):
        """Set the final game result and play the appropriate sound."""
        self.game_over = True
        self.result = result
        self._play_sound(result)

    def _draw_centered(self, screen, text, font, color, y):
        """Draw text horizontally centered on the screen."""
        rendered = font.render(text, True, color)
        x = (self.width - rendered.get_width()) // 2
        screen.blit(rendered, (x, y))

    def _render_game_over(self, screen):
        """Display the win/loss screen and replay instructions."""
        overlay = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 205))
        screen.blit(overlay, (0, 0))

        if self.result == "win":
            heading = "YOU WIN!"
            heading_color = (100, 255, 130)
        else:
            heading = "GAME OVER"
            heading_color = (255, 100, 100)

        self._draw_centered(
            screen, heading, self.title_font, heading_color, 125
        )
        self._draw_centered(
            screen,
            f"Final Score: {self.score}",
            self.font,
            WHITE,
            190,
        )
        self._draw_centered(
            screen,
            f"Difficulty: {self.difficulty}",
            self.small_font,
            WHITE,
            230,
        )

        self._draw_centered(
            screen, "PLAY AGAIN - SELECT DIFFICULTY",
            self.font, WHITE, 290
        )
        self._draw_centered(
            screen, "1 - EASY", self.small_font, (100, 255, 130), 345
        )
        self._draw_centered(
            screen, "2 - MEDIUM", self.small_font, (255, 220, 100), 380
        )
        self._draw_centered(
            screen, "3 - HARD", self.small_font, (255, 120, 120), 415
        )
        self._draw_centered(
            screen, "Q - EXIT     ESC - EXIT",
            self.small_font,
            WHITE,
            475,
        )

    def render(self, screen):
        """Draw the game and its current state."""
        screen.fill(BG)

        pygame.draw.rect(screen, WHITE, self.paddle.rect())

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.ball.x), int(self.ball.y)),
            self.ball.radius,
        )

        for index, brick in enumerate(self.bricks):
            if brick.alive:
                row = index // self.cols
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                pygame.draw.rect(screen, color, brick.rect())

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        lives_text = self.font.render(
            f"Lives: {self.lives}", True, WHITE
        )
        screen.blit(lives_text, (self.width - 130, 10))

        difficulty_text = self.small_font.render(
            f"Difficulty: {self.difficulty}", True, WHITE
        )
        screen.blit(difficulty_text, (10, self.height - 27))

        if self.game_over:
            self._render_game_over(screen)
