import math

import pygame
from pygame import Surface

from models.borot import Borot, SENSOR_LENGTH
from models.world import World


class Picasso:
    def __init__(self, surface: Surface, font: pygame.font.Font):
        self.__surface = surface
        self.__font = font
        self.__ellipses = []

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

        for i in range(len(borot.filter().history)):
            self.draw_ellipses(borot.filter().history[i][0], borot.filter().history[i][1], borot.filter().history[i][2], borot.filter().location[i])
        self.draw_robot_trace(borot)
        self.draw_robot_trace_prediction(borot)
        coordinates = borot.position()
        angle = borot.theta()
        radius = borot.radius()

        self.sensors(borot)

        pygame.draw.circle(self.canvas(), self.robot_color(), coordinates, radius)

        # Draw the direction of the robot
        x = coordinates[0] + math.cos(angle) * radius
        y = coordinates[1] + math.sin(angle) * radius
        pygame.draw.line(self.canvas(), self.robot_direction_color(), coordinates, (x, y), 2)
        self.draw_beacons(borot)

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
            if degree == 'Landmark':  # Draw the sensor line to the landmark as it is the first element in the list
                #pygame.draw.line(self.canvas(), self.landmark_sensor_color(), borot.position(), sensor, 2)
                # distance_value = self.font().render(f'{int(distance)}', True, self.text_color())
                # self.canvas().blit(distance_value, sensor)
                # first = False
                pass
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
                if i % 10 == 0:
                    start_pos = borot.filter().predictiontrack[i - 1]
                    end_pos = borot.filter().predictiontrack[i]
                    start_pos = (int(start_pos[0]), int(start_pos[1]))
                    end_pos = (int(end_pos[0]), int(end_pos[1]))
                    pygame.draw.line(self.canvas(), self.predicted_trace_color(), start_pos, end_pos, 1)
    
    def draw_ellipses(self, width, height, angle, location):
            width = width
            height = height
            angle = angle
            x, y = location
            # transparent surface
            surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            size = (50 - width, 50 - height, width * 10, height * 10)
            pygame.draw.ellipse(surface, (253, 203, 113), size, 2)
            rotate = pygame.transform.rotate(surface, angle)
            self.canvas().blit(rotate, (x - rotate.get_rect().center[0], y - rotate.get_rect().center[1]))

    def get_ellipses(self):
        return self.__ellipses

    def draw_landmark(self, landmarks: list) -> None:
        for landmark in landmarks:
            pygame.draw.circle(self.canvas(), self.landmark_color(), landmark, 2)

    def draw_beacons(self, borot):
        screen = self.canvas()
        sensor_range = SENSOR_LENGTH
        sensor_x = borot.position()[0]
        sensor_y = borot.position()[1]
        beacons = borot.get_landmark_sensors()

        beacons_in_proximity = []
        collision_offset = 0
        fi = None

        for bc in range(len(beacons)):
            dist = (math.sqrt(
                (beacons[bc][1] - sensor_y) ** 2 + (beacons[bc][0] - sensor_x) ** 2)) - collision_offset
            if dist < sensor_range:
                pygame.draw.line(screen, (0, 255, 0), (sensor_x,
                                                       sensor_y), (beacons[bc][0], beacons[bc][1]), 3)
                # Calc fix
                fi = math.atan2((beacons[bc][1] - sensor_y),
                                (beacons[bc][0] - sensor_x)) - borot.theta()
                beacons_in_proximity.append(
                    (beacons[bc][0], beacons[bc][1], dist + collision_offset, -fi))
                # print(beacons[bc].x, beacons[bc].y, dist+collision_offset)
                pygame.draw.circle(screen, (25, 70, 150),
                                   (beacons[bc][0], beacons[bc][1]), dist + collision_offset, 2)

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
