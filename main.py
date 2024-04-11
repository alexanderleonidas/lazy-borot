import pygame
import sys

from utils.picasso import Picasso

# Initialize the game
dimensions = (25,31)
gfx = Picasso(dimensions)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(gfx.screen.get_width() / 2, gfx.screen.get_height() / 2)


# self.create_maze(dimensions[1], dimensions[0])
gfx.create_obstacle_course(dimensions[1])
[center, radius] = gfx.initial_position()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    gfx.screen.fill(gfx.WHITE)

    # graphics.draw_maze()
    gfx.draw_obstacle_course()
    gfx.draw_robot(center,radius)
    gfx.screen.blit(gfx.map_surface, (0, 0))
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000