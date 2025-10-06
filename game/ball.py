import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Initial velocities
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        # Max ball speed to prevent excessive acceleration
        self.max_speed = 10 

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top/bottom)
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        
        # Check collision with Player (left) paddle
        if ball_rect.colliderect(player.rect()) and self.velocity_x < 0:
            self._handle_paddle_hit(player)
            
        # Check collision with AI (right) paddle
        elif ball_rect.colliderect(ai.rect()) and self.velocity_x > 0:
            self._handle_paddle_hit(ai)

    def _handle_paddle_hit(self, paddle):
        # 1. Reverse X-velocity to bounce the ball
        self.velocity_x *= -1
        
        # 2. Add spin (adjust Y-velocity) based on where the ball hit the paddle
        # Center of the paddle
        paddle_center_y = paddle.y + paddle.height // 2
        # Relative distance from center (-1 to 1)
        relative_hit = (self.y - paddle_center_y) / (paddle.height / 2)
        
        # Max Y-velocity is set to half the initial X-velocity, but capped
        max_spin = abs(self.velocity_x) * 0.5
        
        # Apply spin, ensuring Y-velocity doesn't get too high
        self.velocity_y = relative_hit * max_spin
        
        # 3. Increase ball speed slightly (optional, but makes game harder)
        # We cap the speed using self.max_speed
        if abs(self.velocity_x) < self.max_speed:
            self.velocity_x *= 1.1 
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1 # Ball always switches direction on reset
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)