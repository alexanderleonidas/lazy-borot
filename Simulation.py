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
pygame.display.set_caption("Left velocity: 'w' for +, 's' for -. Right velocity: 'o' for +, 'k' for -. Space for stop")
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
font = pygame.font.SysFont('Comic Sans MS', 10)


def handle_collision(circle_center, circle_radius, rect):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(rect.left, min(circle_center.x, rect.right))
    closest_y = max(rect.top, min(circle_center.y, rect.bottom))

    # Calculate the distance from the closest point to the circle's center
    distance_x = circle_center.x - closest_x
    distance_y = circle_center.y - closest_y
    distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

    # Collision occurs 
    if distance < circle_radius:
        # Calculate the normal at the collision point
        normal_vector = pygame.math.Vector2(circle_center.x - closest_x, circle_center.y - closest_y)
        if normal_vector.length_squared() == 0:
            normal = pygame.math.Vector2(1, 0)
        else:
            normal = normal_vector.normalize()

        collision_point = pygame.math.Vector2(closest_x, closest_y)
        return True, collision_point, normal
    return False, None, None


def main():
    picasso = Picasso(surface)
    picasso.draw()
    borot = Borot( )
    borot.find_initial_borot_position(picasso.space,SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    dt = 0
    physics = Physics(borot.theta, borot.radius, borot.position, borot.direction)


    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        old_borot = deepcopy(borot)
        if borot.handle_keys() == False:
            running = False

        physics.apply(dt, borot.v_l, borot.v_r)
        borot.update(physics.position, physics.direction, physics.theta)
        borot.collision_detection(picasso.space)
        # Check for collisions
        for obstacle in picasso.space:
            collision, collision_point, normal = handle_collision(physics.position, borot.radius, obstacle)
            if collision:
                # Handle collision by stopping the borot or implementing some bounce logic
                physics.handle_collision(normal)
                break

        # Update the robot's position
        movement_vector = borot.direction * (borot.v_l + borot.v_r) / 2
        borot.position += movement_vector * dt



        borot.collision_detection(picasso.space)  # Detect collisions
        screen.blit(surface, (0, 0))  # Copy the obstacle surface onto the main window
        borot.draw(screen, font)


        pygame.display.flip()
        dt = clock.tick(50) / 1000  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()