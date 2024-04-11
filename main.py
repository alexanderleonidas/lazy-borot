from typing import Tuple

import pygame
import sys

from pygame import Vector2

from models.world import World
from utils.picasso import Picasso

# Initialize the game
dimensions = (25, 31)
world = World(dimensions)
gfx = Picasso(world)

clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(gfx.screen.get_width() / 2, gfx.screen.get_height() / 2)
player_vel = pygame.Vector2(0, 0)
player_acc = pygame.Vector2(0, 0)

# self.create_maze(dimensions[1], dimensions[0])
world.generate_obstacle_course(dimensions[1])
[center, radius] = world.initial_position()

print(center)
print(radius)

acceleration_factor = 1000
friction_factor = 0.9
steering_force = 0.5


def move(temp_keys: pygame.key.ScancodeWrapper, local_pos: pygame.Vector2, local_vel: pygame.Vector2,
         delta: float | int) -> \
        tuple[Vector2 | Vector2, Vector2 | Vector2]:
    desired_vel = pygame.Vector2(0, 0)

    if temp_keys[pygame.K_w]:
        desired_vel.y = -acceleration_factor
    if temp_keys[pygame.K_s]:
        desired_vel.y = acceleration_factor
    if temp_keys[pygame.K_a]:
        desired_vel.x = -acceleration_factor
    if temp_keys[pygame.K_d]:
        desired_vel.x = acceleration_factor

    # Adjust current velocity towards desired velocity to simulate steering
    if desired_vel.length() > 0:  # Normalize if there's a desired direction
        desired_vel = desired_vel.normalize() * acceleration_factor

    steering = (desired_vel - local_vel) * steering_force
    local_vel += steering * delta
    local_vel *= friction_factor
    local_pos += local_vel * delta

    return local_pos, local_vel


def get_direction(velocity: pygame.Vector2) -> float:
    # Calculate direction in degrees, 0 being to the right. Adjusting for Pygame's y-axis.
    base_vector = pygame.Vector2(1, 0)  # Right
    if velocity.length() > 0:
        return base_vector.angle_to(velocity)
    return 0  # Default direction when not moving


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player_pos, player_vel = move(keys, player_pos, player_vel, dt)
    player_direction = get_direction(player_vel)

    gfx.screen.fill(gfx.WHITE)

    # graphics.draw_maze()
    gfx.draw_obstacle_course()
    gfx.draw_robot(player_pos, radius, player_direction)
    gfx.screen.blit(gfx.map_surface, (0, 0))
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
