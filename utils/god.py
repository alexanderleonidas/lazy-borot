import random
from typing import Optional

import pygame.event

from models.action import Action
from models.state import State
from models.world import World


def build(width: int, height: int, n_obstacles: int, obstacle_size: tuple, wall_thickness: int) -> World:
    world = World(width, height, n_obstacles, obstacle_size, wall_thickness)

    # Draw Walls around the map
    world.add_obstacle((0, 0, width, wall_thickness))
    world.add_obstacle((0, 0, wall_thickness, height))
    world.add_obstacle((width - wall_thickness, 0, wall_thickness, height))
    world.add_obstacle((0, height - wall_thickness, width, wall_thickness))

    # Place Random Obstacles Throughout the World
    for _ in range(n_obstacles):
        lim = 0

        while True:
            x = random.randint(1, (width - obstacle_size[0]) // obstacle_size[0]) * obstacle_size[0]
            y = random.randint(1, (height - obstacle_size[1]) // obstacle_size[1]) * obstacle_size[1]
            obstacle = (x, y, obstacle_size[0], obstacle_size[1])

            # Ensure there's a clear path by avoiding the direct line from start to end
            if obstacle_size[1] < y < height - 2 * obstacle_size[1]:
                world.add_obstacle(obstacle)
                break

            # Break if the loop runs for too long
            if lim > 100:
                break

            lim += 1

    world.spawn()

    return world


def listening(state: State, dt) -> State:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_o:
                return state.next(Action.INCREASE_RIGHT, dt)
            if event.key == pygame.K_k:
                return state.next(Action.DECREASE_RIGHT, dt)
            if event.key == pygame.K_w:
                return state.next(Action.INCREASE_LEFT, dt)
            if event.key == pygame.K_s:
                return state.next(Action.DECREASE_LEFT, dt)
            if event.key == pygame.K_SPACE:
                return state.next(Action.BREAK, dt)

    return state.next(Action.NOTHING, dt)
