import pygame

from models.world import World
from utils.picasso import Picasso

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lazy Borot")
        self.clock = pygame.time.Clock()

        self.map = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.canvas = Picasso(self.map)
        self.map.build_map()

    def run(self):
        running = True
        self.map.spawn()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.canvas.draw_map()
            self.canvas.draw_robot(self.map.borot.position, self.map.borot.radius, self.map.borot.rotation)

            self.screen.blit(self.canvas.map_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
