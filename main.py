import pygame
import sys
from pygame import Vector2

from models.world import World
from utils.picasso import Picasso

dimensions = (25, 31)
world = World(dimensions)
canvas = Picasso(world)

clock = pygame.time.Clock()
running = True
dt = 0

world.build()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    canvas.screen.fill(canvas.WHITE)
    canvas.draw_obstacle_course()
    canvas.draw_robot(world.borot.position, world.radius, world.borot.rotation)
    canvas.screen.blit(canvas.map_surface, (0, 0))
    pygame.display.flip()

    dt = clock.tick(60) / 1000

