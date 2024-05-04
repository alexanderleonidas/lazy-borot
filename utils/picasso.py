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

        self.draw_landmark(world.landmarks())

    def robot(self, borot: Borot) -> None:
        # self.draw_robot_trace(borot)
        self.draw_robot_trace_prediction(borot)
        self.draw_ellipses(borot)

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
        rotation_surface = self.font().render(f'Theta (rads): {int(math.degrees(borot.theta()))}', True,
                                              self.text_color())
        speed_left_surface = self.font().render(f'Left speed: {v_l}', True, self.text_color())
        speed_right_surface = self.font().render(f'Right speed: {v_r}', True, self.text_color())

        # Draw the text on the screen at a fixed position
        self.canvas().blit(rotation_surface, (20, self.canvas().get_height() - 60))
        self.canvas().blit(speed_left_surface, (20, self.canvas().get_height() - 50))
        self.canvas().blit(speed_right_surface, (20, self.canvas().get_height() - 40))

    def sensors(self, borot: Borot) -> None:
        first = True
        for degree, sensor, distance in borot.sensors():
            if first: # Draw the sensor line to the landmark as it is the first element in the list
                pygame.draw.line(self.canvas(), self.landmark_sensor_color(), borot.position(), sensor, 2)
                distance_value = self.font().render(f'{int(distance)}', True, self.text_color())
                self.canvas().blit(distance_value, sensor)
                first = False
            else:
                pygame.draw.line(self.canvas(), self.sensor_color(), borot.position(), sensor, 2)
                pygame.draw.circle(self.canvas(), self.sensor_endpoint_color(), sensor, 2)
                distance_value = self.font().render(f'{int(distance)}', True, self.text_color())
                self.canvas().blit(distance_value, sensor)

    def draw_robot_trace(self, borot: Borot) -> None:
        if len(borot.trace()) > 1:
            pygame.draw.lines(self.canvas(), self.trace_color(), False, borot.trace(), 1)

    def draw_robot_trace_prediction(self, borot: Borot) -> None:
        if len(borot.filter().predictiontrack) > 1:
            for i in range(1, len(borot.filter().predictiontrack)):
                if i % 20 == 0:
                    start_pos = borot.filter().predictiontrack[i - 1]
                    end_pos = borot.filter().predictiontrack[i]
                    start_pos = (int(start_pos[0]), int(start_pos[1]))
                    end_pos = (int(end_pos[0]), int(end_pos[1]))
                    pygame.draw.line(self.canvas(), self.predicted_trace_color(), start_pos, end_pos, 1)

    def draw_ellipses(self, borot: Borot) -> None:
        for data in borot.filter().history:
            # TODO: Keep an eye out for the radius, it might be wrong
            #  (as of 2024/04/30 it is giving extremely small values e.g. 0.3....)
            x_radius, y_radius, angle = data
            center = (int(borot.position()[0]), int(borot.position()[1]))
            ellipse_rect = pygame.Rect(center[0] - x_radius, center[1] - y_radius, x_radius * 2, y_radius * 2)
            rotated_ellipse = pygame.transform.rotate(pygame.Surface((2*x_radius, 2*y_radius), pygame.SRCALPHA), -angle)
            pygame.draw.ellipse(rotated_ellipse, self.ellipses_color(), pygame.Rect(0, 0, 2*x_radius, 2*y_radius))
            self.canvas().blit(rotated_ellipse, ellipse_rect.topleft)

    def draw_landmark(self, landmarks: list) -> None:
        for landmark in landmarks:
            pygame.draw.circle(self.canvas(), self.landmark_color(), landmark, 2)

    @staticmethod
    def landmark_color():
        return pygame.Color('black')

    @staticmethod
    def ellipses_color():
        return pygame.Color('gold')

    @staticmethod
    def predicted_trace_color():
        return pygame.Color('fuchsia')

    @staticmethod
    def trace_color() -> pygame.Color:
        return pygame.Color('dodgerblue2')

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
        return pygame.Color('goldenrod4')
    
    @staticmethod
    def landmark_sensor_color() -> pygame.Color:
        return pygame.Color('chartreuse2')

    @staticmethod
    def sensor_endpoint_color() -> pygame.Color:
        return pygame.Color('blue')
