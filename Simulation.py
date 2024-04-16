from copy import copy, deepcopy

import pygame

from Borot import Borot, SENSOR_LENGTH
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


def circle_rect_collision(circle_center, circle_radius, rect):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(rect.left, min(circle_center.x, rect.right))
    closest_y = max(rect.top, min(circle_center.y, rect.bottom))

    # Calculate the distance from the closest point to the circle's center
    distance_x = circle_center.x - closest_x
    distance_y = circle_center.y - closest_y
    distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

    # Collision occurs if the distance is less than the circle's radius
    return distance < circle_radius

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
        old_borot = deepcopy(borot)
        borot.handle_keys()  # Handle key inputs

        # Update the sensor endpoints
        for obstacle in picasso.space:
            rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if circle_rect_collision(pygame.math.Vector2(borot.position.x, borot.position.y), borot.radius, rect):
                borot.position = old_borot.position
                break

        borot.collision_detection(picasso.space)  # Detect collisions
        screen.blit(surface, (0, 0))  # Copy the obstacle surface onto the main window
        borot.draw(screen, font)
        
        
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()