from copy import copy, deepcopy

import pygame

from Borot import Borot, SENSOR_LENGTH
from Picasso import Picasso
from Physics import Physics
from Kalman import KalmanFilter
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
pygame.display.set_caption("Left velocity: 'w' for +, 's' for -. Right velocity: 'o' for +, 'k' for -. Space for stop")
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
font = pygame.font.SysFont('Comic Sans MS', 10)



def main():
    picasso = Picasso(surface)
    picasso.draw()
    borot = Borot( )
    borot.find_initial_borot_position(picasso.space,SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    dt = 0
    physics = Physics(borot.theta, borot.radius, borot.position, borot.direction)
    print(picasso.space)
    

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        old_borot = deepcopy(borot)
        if borot.handle_keys() == False:
            running = False
        physics.apply(dt, borot.v_l, borot.v_r)

        # Update Borot's state based on physics calculations
        borot.update_position(physics.position, physics.direction, physics.theta)
        borot.update_sensors(picasso.space)

        # Detect and handle collisions
        collision_info = borot.detect_collision(picasso.space)
        borot.update_after_collision(collision_info)

        screen.blit(surface, (0, 0))  # Copy the obstacle surface onto the main window
        borot.draw(screen, font)
        
        pygame.display.flip()
        dt = clock.tick(50) / 1000  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()