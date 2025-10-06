## 2. `main.py` (Updated for Input Handling)


import pygame
import time
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Check for Replay/Exit input only if the game has ended
            if not engine.game_running and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    engine.reset_game(3) # Best of 3
                elif event.key == pygame.K_5:
                    engine.reset_game(5) # Best of 5
                elif event.key == pygame.K_7:
                    engine.reset_game(7) # Best of 7
                elif event.key == pygame.K_ESCAPE:
                    running = False # Exit loop immediately

        SCREEN.fill(BLACK)
        
        # Game logic (input and update) only runs if engine is active
        engine.handle_input()
        engine.update()
        
        # Render runs always to show the game or the final score/menu
        engine.render(SCREEN) 

        pygame.display.flip()
        clock.tick(FPS)
        
    # Game loop has exited. No delay needed now as the user controls the exit.
    pygame.quit()

if __name__ == "__main__":
    main()