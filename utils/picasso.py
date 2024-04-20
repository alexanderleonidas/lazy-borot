import math

import pygame
from pygame import Surface

from models.borot import Borot
from models.world import World


class Picasso:
    def __init__(self, surface: Surface, font: pygame.font.Font):
        self.__surface = surface
        self.__font = font

    def font(self) -> pygame.font.Font:
        return self.__font

    def canvas(self) -> Surface:
        return self.__surface

    def draw(self, world: World) -> None:
        self.canvas().fill(self.floor_color())

        for obstacle in world.obstacles():
            self.wall(obstacle)

    def robot(self, borot: Borot) -> None:
        coordinates = borot.position()
        angle = borot.theta()
        radius = borot.radius()

        self.sensors(borot)

        pygame.draw.circle(self.canvas(), self.robot_color(), coordinates, radius)

        # Draw the direction of the robot
        x = coordinates[0] + math.cos(angle) * radius
        y = coordinates[1] + math.sin(angle) * radius
        pygame.draw.line(self.canvas(), self.robot_direction_color(), coordinates, (x, y), 2)

    def wall(self, coordinates: tuple) -> None:
        pygame.draw.rect(self.canvas(), self.obstacle_color(), coordinates)

    def robot_data(self, borot: Borot) -> None:
        v_l, v_r = borot.speed()
        rotation_surface = self.font().render(f'Theta (rads): {int(math.degrees(borot.theta()))}', False,
                                              self.text_color())
        speed_left_surface = self.font().render(f'Left speed: {v_l}', False, self.text_color())
        speed_right_surface = self.font().render(f'Right speed: {v_r}', False, self.text_color())

        # Draw the text on the screen at a fixed position
        self.canvas().blit(rotation_surface, (20, self.canvas().get_height() - 60))
        self.canvas().blit(speed_left_surface, (20, self.canvas().get_height() - 50))
        self.canvas().blit(speed_right_surface, (20, self.canvas().get_height() - 40))

    def sensors(self, borot: Borot) -> None:
        for degree, sensor in borot.sensors():
            pygame.draw.line(self.canvas(), self.sensor_color(), borot.position(), sensor, 2)
            pygame.draw.circle(self.canvas(), self.sensor_endpoint_color(), sensor, 2)

    @staticmethod
    def obstacle_color() -> pygame.Color:
        return pygame.Color('firebrick')

    @staticmethod
    def robot_color() -> pygame.Color:
        return pygame.Color('dodgerblue')

    @staticmethod
    def robot_direction_color() -> pygame.Color:
        return pygame.Color('white')

    @staticmethod
    def floor_color() -> pygame.Color:
        return pygame.Color('aliceblue')

    @staticmethod
    def text_color() -> pygame.Color:
        return pygame.Color('black')

    @staticmethod
    def sensor_color() -> pygame.Color:
        return pygame.Color('green')

    @staticmethod
    def sensor_endpoint_color() -> pygame.Color:
        return pygame.Color('blue')
