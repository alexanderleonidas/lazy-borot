import random

from models.borot import Borot
from utils.utils import intersects


class World:
    def __init__(self, width: int, height: int) -> None:
        self.__obstacles = []
        self.__landmarks = []
        self.__dust = []
        self.__borot = Borot()

        self.__width = width
        self.__height = height

    def obstacles(self) -> list:
        return self.__obstacles

    def borot(self) -> Borot:
        return self.__borot

    def landmarks(self) -> list:
        return self.__landmarks
    
    def dust(self) -> list:
        return self.__dust

    def add_landmark(self, landmark: tuple) -> None:
        if landmark not in self.__landmarks:
            self.__landmarks.append(landmark)
            return

        # Check if the landmark is connected to another landmark, then remove the connection
        for i, other in enumerate(self.__landmarks):
            if other == landmark:
                self.__landmarks.pop(i)
                break

    def add_obstacle(self, obstacle: tuple) -> None:
        if obstacle not in self.__obstacles:
            self.__obstacles.append(obstacle)
    
    def add_dust(self, dust: tuple):
        if dust not in self.__dust:
            self.__dust.append(dust)

    def width(self) -> int:
        return self.__width

    def height(self) -> int:
        return self.__height

    def find_landmarks(self):
        for obstacle in self.obstacles():
            x, y, w, h = obstacle

            if x > 0 and y > 0:
                self.add_landmark((x, y))

            if x + w < self.width() and y > 0:
                self.add_landmark((x + w, y))

            if x > 0 and y + h < self.height():
                self.add_landmark((x, y + h))

            if x + w < self.width() and y + h < self.height():
                self.add_landmark((x + w, y + h))

    def spawn(self, position: tuple = None):
        if position:
            self.borot().birth(position)
            return

        max_attempts = 100

        for _ in range(max_attempts):
            radius = self.borot().radius()
            x = random.randint(radius, self.width() - radius)
            y = random.randint(radius, self.__height - radius)
            position = (x - radius, y - radius, radius * 2, radius * 2)

            if not any(intersects(position, obstacle) for obstacle in self.obstacles()):
                self.borot().birth((x, y))
                break
