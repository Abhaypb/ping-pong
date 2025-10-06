import pygame
import time
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects

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

# Load Sound Effects (PLACEHOLDER NAMES - Ensure these files exist!)
try:
    SOUNDS = {
        'paddle_hit': pygame.mixer.Sound('paddle_hit.wav'),
        'wall_bounce': pygame.mixer.Sound('wall_bounce.wav'),
        'score': pygame.mixer.Sound('score.wav')
    }
except pygame.error as e:
    print(f"Warning: Could not load sound files. Make sure 'paddle_hit.wav', 'wall_bounce.wav', and 'score.wav' are in the correct directory. Error: {e}")
    SOUNDS = None
    
# Game loop
engine = GameEngine(WIDTH, HEIGHT, SOUNDS) # Pass sounds to the engine

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
                    engine.reset_game(3)
                elif event.key == pygame.K_5:
                    engine.reset_game(5)
                elif event.key == pygame.K_7:
                    engine.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        SCREEN.fill(BLACK)
        
        # Game logic (input and update) only runs if engine is active
        engine.handle_input()
        engine.update()
        
        # Render runs always to show the game or the final score/menu
        engine.render(SCREEN) 

        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()