import pygame

from models.world import World
from utils.picasso import Picasso
from utils.sensors import Sensors

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
        self.map.build_map(obstacles=100, obstacle_width=40, obstacle_height=40)
        self.sensors = Sensors(self.map.borot.position, self.screen)

    def run(self):
        running = True
        self.map.spawn()

        frames_per_second = 60
        dt = frames_per_second

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            key = [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_o], keys[pygame.K_l],
                   keys[pygame.K_t], keys[pygame.K_g], keys[pygame.K_x]]

            self.map.borot.moving_keys(key, dt, self.screen, self.map.borot.radius)
            self.sensors.cast_rays()

            self.canvas.draw_map()
            self.canvas.draw_robot(self.map.borot.position, self.map.borot.radius, self.map.borot.rotation)

            self.screen.blit(self.canvas.map_surface, (0, 0))
            pygame.display.flip()
            dt = self.clock.tick(frames_per_second) / 1000
