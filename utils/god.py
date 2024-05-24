import random
from typing import Optional

import pygame.event

from maps.hallway import Hallway
from maps.maze import Maze
from models.action import Action
from models.state import State
from models.world import World
from utils.utils import intersects


random.seed(42)

def build(width: int, height: int, n_obstacles: int, obstacle_size: tuple, wall_thickness: int, maze: int = 1):
    if maze == 1:
        world = Maze().build()
        world.spawn((75, 85))
    elif maze == 2:
        world = Hallway().build()
        world.spawn((20, 20))
    else:
        world = build_random(width, height, n_obstacles, obstacle_size, wall_thickness)
        world.spawn()
    
    make_dusty(width, height, num_particles=1000, dust_radius=10, world=world)

    return world


def build_random(width: int, height: int, n_obstacles: int, obstacle_size: tuple, wall_thickness: int):
    world = World(width, height)

    # Draw Walls around the map
    world.add_obstacle((wall_thickness, 0, width - (2 * wall_thickness), wall_thickness))  # Top wall
    world.add_obstacle((0, 0, wall_thickness, height))  # Left wall
    world.add_obstacle((width - wall_thickness, 0, wall_thickness, height))  # Right wall
    world.add_obstacle((wall_thickness, height - wall_thickness, width - (2 * wall_thickness), wall_thickness))  # Bottom wall

    # List to store existing obstacles to check for overlaps
    obstacles = []

    # Place Random Obstacles Throughout the World, ensuring they do not overlap or touch walls
    for _ in range(n_obstacles):
        lim = 0

        while True:
            x = random.randint(wall_thickness + 1, width - wall_thickness - obstacle_size[0] - 1)
            y = random.randint(wall_thickness + 1, height - wall_thickness - obstacle_size[1] - 1)
            new_obstacle = (x, y, obstacle_size[0], obstacle_size[1])
            overlaps = False

            # Check new obstacle against all previously placed obstacles to ensure no overlap
            for existing_obstacle in world.obstacles():
                # Create rectangles for overlap checking
                existing_rect = pygame.Rect(existing_obstacle)
                new_rect = pygame.Rect(new_obstacle)
                if existing_rect.colliderect(new_rect):
                    overlaps = True
                    break

            # Add the obstacle if it doesn't overlap and is properly placed
            if not overlaps:
                world.add_obstacle(new_obstacle)
                obstacles.append(new_obstacle)
                break

            # Break if the loop runs for too long to avoid infinite loop
            if lim > 100:
                print("Unable to place all obstacles without overlap after multiple attempts.")
                break

            lim += 1

    return world


def make_dusty(width: int, height: int, num_particles: int, dust_radius: int, world: World):
    iteration = 0
    while iteration < num_particles:
        x = random.randint(0, width - dust_radius)
        y = random.randint(0, height - dust_radius)
        dust = (x, y, dust_radius*2, dust_radius*2)

        if not any(intersects(dust, obstacle) for obstacle in world.obstacles()):
            world.add_dust(dust)
        iteration += 1


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
        # Quit Game
        if event.type == pygame.QUIT:
            pygame.quit()

    return state.next(Action.NOTHING, dt)
