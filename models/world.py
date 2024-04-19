import random

from models.borot import Borot
from utils.utils import intersects


class World:
    def __init__(self, width: int, height: int, n_obstacles: int, obstacle_size: tuple, wall_thickness: int) -> None:
        self.__obstacles = []
        self.__borot = Borot()

        self.__width = width
        self.__height = height
        self.__n_obstacles = n_obstacles
        self.__obstacle_size = obstacle_size
        self.__wall_thickness = wall_thickness

    def obstacles(self) -> list:
        return self.__obstacles

    def borot(self) -> Borot:
        return self.__borot

    def add_obstacle(self, obstacle: tuple) -> None:
        self.__obstacles.append(obstacle)

    def width(self) -> int:
        return self.__width

    def height(self) -> int:
        return self.__height

    def spawn(self):
        max_attempts = 100

        for _ in range(max_attempts):
            radius = self.borot().radius()
            x = random.randint(radius, self.width() - radius)
            y = random.randint(radius, self.__height - radius)
            position = (x - radius, y - radius, radius * 2, radius * 2)

            if not any(intersects(position, obstacle) for obstacle in self.obstacles()):
                self.borot().birth((x, y))
                break
