import random
from typing import Tuple

from models.borot import Borot

WALL_SIZE = 20


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.borot = Borot("Borot", self)

    def add_wall(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int]):
        self.walls.append(Wall(top_left, bottom_right))

    def build_boundary_walls(self):
        self.add_wall((0, 0), (self.width, WALL_SIZE))
        self.add_wall((0, self.height - WALL_SIZE), (self.width, self.height))
        self.add_wall((0, 0), (WALL_SIZE, self.height))
        self.add_wall((self.width - WALL_SIZE, 0), (self.width, self.height))

    def build_map(self, num_walls=5):
        self.build_boundary_walls()

        # TODO: Generate Random Walls
        self.add_wall((0, 100), (700, WALL_SIZE))
        self.add_wall((900, 100), (self.width, WALL_SIZE))
        self.add_wall((100, 200), (self.width, WALL_SIZE))
        self.add_wall((100, 200), (WALL_SIZE, 300))
        self.add_wall((100, 400), (800, WALL_SIZE))
        self.add_wall((500, 400), (WALL_SIZE, 250))
        self.add_wall((800, 500), (WALL_SIZE, 250))
        self.add_wall((1100, 300), (WALL_SIZE, 325))

    def spawn(self):
        self.borot.position = (50, 50)



class Wall:

    def __init__(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int]):
        self.top_left = top_left
        self.bottom_right = bottom_right
