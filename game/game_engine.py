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
        # Assuming ball.py has been updated from the previous request with the max_speed and spin logic
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # Set the target score to 5

        # New state variable to control game loop logic
        self.game_running = True 
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.winner = None

    def handle_input(self):
        # Only process input if the game is actively running
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
        
        # Check for Game Over condition after score updates
        if self.player_score >= self.winning_score:
            self.game_running = False
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_running = False
            self.winner = "AI"

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.rect(screen, WHITE, self.ball.rect())

        # Draw centerline (dashed)
        for i in range(0, self.height, 20):
            pygame.draw.rect(screen, WHITE, (self.width // 2 - 2, i, 4, 10))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width(), 20))

        # Draw Game Over message if game has ended
        if not self.game_running and self.winner:
            message = f"{self.winner} Wins!"
            text_surface = self.game_over_font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            
            # Sub-message for exit/replay (Task 3 prep)
            sub_message = "Press ESC to exit..."
            sub_text_surface = self.font.render(sub_message, True, WHITE)
            sub_text_rect = sub_text_surface.get_rect(center=(self.width // 2, self.height // 2 + 70))
            screen.blit(sub_text_surface, sub_text_rect)