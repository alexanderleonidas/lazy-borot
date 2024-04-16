import pygame

from Borot import Borot
from Picasso import Picasso
from Physics import Physics

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
WALL_THICKNESS = 15
BACKGROUND_COLOR = (255, 255, 255)  # White background
OBSTACLE_COLOR = (0, 0, 0)  # Black obstacles
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 40
N_OBSTACLES = 45

# Initialize Pygame
pygame.init()
# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Randomized Obstacle Course")
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
font = pygame.font.SysFont('Comic Sans MS', 10)

def main():
    picasso = Picasso(surface)
    picasso.draw()
    borot = Borot(0)
    borot.find_initial_borot_position(picasso.space,SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        borot.handle_keys()  # Handle key inputs
        borot.collision_detection(picasso.space)  # Detect collisions
        borot.draw(screen, font)
        screen.blit(surface, (0, 0))  # Copy the obstacle surface onto the main window
        
        
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()