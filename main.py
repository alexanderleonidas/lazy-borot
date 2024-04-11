import pygame
import sys
from pygame import Vector2

from models.world import World
from models.borot import Borot
from utils.picasso import Picasso
from utils.sensors import Sensors

dimensions = (25, 31)
world = World(dimensions)
canvas = Picasso(world)


clock = pygame.time.Clock()
running = True
dt = 50
FPS = 60

world.build()
player_pos = world.borot.position
screen = canvas.screen
sensor=Sensors(player_pos, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # timer
    clock.tick(FPS)
    # activate buttons
    keys = pygame.key.get_pressed()
    key = [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_o], keys[pygame.K_l],
           keys[pygame.K_t], keys[pygame.K_g], keys[pygame.K_x]]

    # run the robot
    print("Old: ", world.borot.position)
    activate = world.borot.moving_keys(key, dt, screen, player)
    print("New: ", world.borot.position)

    canvas.screen.fill(canvas.WHITE)
    canvas.draw_obstacle_course()
    canvas.draw_robot(player_pos, world.radius, world.borot.rotation)
    canvas.screen.blit(canvas.map_surface, (0, 0))
    pygame.display.flip()

    dt = clock.tick(60) / 1000 

