import pygame
import sys
from pygame import Vector2

from models.world import World
from utils.picasso import Picasso
from utils.sensors import Sensors

dimensions = (25, 31)
world = World(dimensions)
canvas = Picasso(world)


clock = pygame.time.Clock()
running = True
dt = 0

world.build()
player_pos = world.borot.position
screen = canvas.screen
sensor=Sensors(player_pos, screen)
sensor.cast_rays()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    canvas.screen.fill(canvas.WHITE)
    canvas.draw_obstacle_course()
    canvas.draw_robot(player_pos, world.radius, world.borot.rotation)
    sensor.detect_collisions()
    sensor.draw_sensors()
    
    canvas.screen.blit(canvas.map_surface, (0, 0))
    pygame.display.flip()

    dt = clock.tick(60) / 1000

