import math

from maps.map import Map
from models.world import World

DUST_RADIUS = 10
DISTANCE = 30
X_MIN = 50
X_MAX = 350
Y_MIN = 50
Y_MAX = 350


class Hallway(Map):
    def __init__(self):
        super().__init__(400, 400)
        self.__name = "Hallway"
        self.wall_thickness = 10

    def build(self) -> World:
        self.world().add_obstacle((self.wall_thickness, 0, self.width() - (2 * self.wall_thickness), self.wall_thickness))  # Top wall
        self.world().add_obstacle((0, 0, self.wall_thickness, self.height()))  # Left wall
        self.world().add_obstacle((self.width() - self.wall_thickness, 0, self.wall_thickness, self.height()))  # Right wall
        self.world().add_obstacle(
            (self.wall_thickness, self.height() - self.wall_thickness, self.width() - (2 * self.wall_thickness), self.wall_thickness))

        self.dust()
        return self.world()

    def dust(self) -> World:
        dusts = []

        x_tiles = math.floor((X_MAX - X_MIN) / DISTANCE)
        y_tiles = math.floor((Y_MAX - Y_MIN) / DISTANCE)

        for i in range(x_tiles):
            for j in range(y_tiles):
                dusts.append((DISTANCE + i * DISTANCE, DISTANCE + j * DISTANCE))

        for dust in dusts:
            obj = (dust[0], dust[1], DUST_RADIUS * 2, DUST_RADIUS * 2)
            self.world().add_dust(obj)

        return self.world()
