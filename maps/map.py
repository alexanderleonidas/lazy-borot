import random
from abc import ABC

from models.world import World


class Map(ABC):
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__world = World(width, height)

    def build(self) -> World:
        pass

    def width(self) -> int:
        return self.__width

    def height(self) -> int:
        return self.__height

    def world(self) -> World:
        return self.__world

    def dust(self) -> World:
        pass
