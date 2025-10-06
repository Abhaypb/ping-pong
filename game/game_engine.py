import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # Default target score

        # State management
        self.game_running = True 
        self.winner = None

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)

    def handle_input(self):
        # Only process player paddle input if the game is actively running
        if self.game_running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        if not self.game_running:
            return  # Stop all game updates if the game is over

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Check for scoring and update scores
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        
        # Check for Game Over condition
        if self.player_score >= self.winning_score:
            self.game_running = False
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_running = False
            self.winner = "AI"

    def reset_game(self, new_winning_score):
        """Resets the game state and sets a new winning score."""
        self.winning_score = new_winning_score
        self.player_score = 0
        self.ai_score = 0
        self.winner = None
        self.game_running = True
        self.ball.reset() # Reset the ball position and direction

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        
        # Only draw the ball if the game is running
        if self.game_running:
            pygame.draw.rect(screen, WHITE, self.ball.rect())

        # Draw centerline (dashed)
        for i in range(0, self.height, 20):
            pygame.draw.rect(screen, WHITE, (self.width // 2 - 2, i, 4, 10))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width(), 20))

        # Draw Game Over message and Replay Options
        if not self.game_running and self.winner:
            message = f"{self.winner} Wins! (Best of {self.winning_score})"
            text_surface = self.game_over_font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)
            
            # Replay options menu
            menu_options = [
                "Press '3' for Best of 3",
                "Press '5' for Best of 5",
                "Press '7' for Best of 7",
                "Press 'ESC' to Exit"
            ]
            y_offset = 0
            for option in menu_options:
                sub_text_surface = self.font.render(option, True, WHITE)
                sub_text_rect = sub_text_surface.get_rect(center=(self.width // 2, self.height // 2 + 50 + y_offset))
                screen.blit(sub_text_surface, sub_text_rect)
                y_offset += 40