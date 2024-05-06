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
        self.find_beacon(world.borot().get_landmark_sensors(), world.borot())

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
            if degree == 'Landmark':  # Draw the sensor line to the landmark as it is the first element in the list
                #pygame.draw.line(self.canvas(), self.landmark_sensor_color(), borot.position(), sensor, 2)
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
            rotated_ellipse = pygame.transform.rotate(pygame.Surface((2 * x_radius, 2 * y_radius), pygame.SRCALPHA),
                                                      -angle)
            pygame.draw.ellipse(rotated_ellipse, self.ellipses_color(), pygame.Rect(0, 0, 2 * x_radius, 2 * y_radius))
            self.canvas().blit(rotated_ellipse, ellipse_rect.topleft)

    def draw_landmark(self, landmarks: list) -> None:
        for landmark in landmarks:
            pygame.draw.circle(self.canvas(), self.landmark_color(), landmark, 2)

    def find_beacon(self, beacons, borot: Borot):
        screen = self.canvas()
        sensor_range = 100
        sensor_x = borot.position()[0]
        sensor_y = borot.position()[1]

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

        if len(beacons_in_proximity) == 2:
            x0 = beacons_in_proximity[0][0]
            y0 = beacons_in_proximity[0][1]
            r0 = beacons_in_proximity[0][2]
            f0 = beacons_in_proximity[0][3]
            x1 = beacons_in_proximity[1][0]
            y1 = beacons_in_proximity[1][1]
            r1 = beacons_in_proximity[1][2]
            f1 = beacons_in_proximity[1][3]
            # print(x0, y0, r0)
            # print(x1, y1, r1)
            # print("FI-1 by detection ", beacons_in_proximity[0][3])
            # print("FI-2 by detection ", beacons_in_proximity[1][3])
            # print("Theta ", player_robot.theta)

            p1, p2, fipos1, fipos2 = self.circle_intersection(x0, y0, r0, x1, y1, r1)

            # print("REAL POS", (f0, f1))
            # print("POT POS 1", fipos1)
            # print("POT POS 2", fipos2)

            if f0 - 0.2 <= fipos1[0] <= f0 + 0.2 and f1 - 0.2 <= fipos1[1] <= f1 + 0.2:
                # pygame.draw.circle(screen, (100, 10, 50), (p1[0], p1[1]), 5)
                return (p1[0], p1[1], borot.theta())
            else:
                # pygame.draw.circle(screen, (100, 10, 50), (p2[0], p2[1]), 5)
                return (p2[0], p2[1], borot.theta())

        elif len(beacons_in_proximity) > 2:
            x0 = beacons_in_proximity[0][0]
            y0 = beacons_in_proximity[0][1]
            r0 = beacons_in_proximity[0][2]
            f0 = beacons_in_proximity[0][3]
            x1 = beacons_in_proximity[1][0]
            y1 = beacons_in_proximity[1][1]
            r1 = beacons_in_proximity[1][2]
            f1 = beacons_in_proximity[1][3]
            x2 = beacons_in_proximity[2][0]
            y2 = beacons_in_proximity[2][1]
            r2 = beacons_in_proximity[2][2]
            f2 = beacons_in_proximity[2][3]

            p1, p2, fipos1, fipos2 = self.circle_intersection(x0, y0, r0, x1, y1,
                                                         r1)
            # pygame.draw.circle(screen, (150, 150, 15), (p1[0], p1[1]), 5)
            # pygame.draw.circle(screen, (150, 150, 15), (p2[0], p2[1]), 5)
            p3, p4, fipos3, fipos4 = self.circle_intersection(screen, x0, y0, r0, x2, y2,
                                                         r2)
            # pygame.draw.circle(screen, (50, 150, 150), (p3[0], p3[1]), 5)
            # pygame.draw.circle(screen, (50, 150, 150), (p4[0], p4[1]), 5)
            p5, p6, fipos5, fipos6 = self.circle_intersection(screen, x1, y1, r1, x2, y2,
                                                         r2)
            # pygame.draw.circle(screen, (150, 150, 150), (p5[0], p5[1]), 5)
            # pygame.draw.circle(screen, (150, 150, 150), (p6[0], p6[1]), 5)

            # print("P1, P2 ", p1[0], p1[1], p2[0], p2[1])
            # print("P3, P4 ", p3[0], p3[1], p4[0], p4[1])
            # print("P5, P6 ", p5[0], p5[1], p6[0], p6[1])

            if p1[0] - 5 <= p3[0] <= p1[0] + 5 and p1[1] - 5 <= p3[1] <= p1[1] + 5:
                # if (p1[0] - 3 < p5[0] < p1[0] + 3 and p1[1] - 3 < p5[1] < p1[1] + 3) or (p1[0] - 3 < p6[0] < p1[0] + 3 and p1[1] - 3 < p6[1] < p1[1] + 3):
                # pygame.draw.circle(screen, (150, 150, 15), (p1[0], p1[1]), 5)
                return (p1[0], p1[1], borot.theta())
            elif p1[0] - 5 <= p4[0] <= p1[0] + 5 and p1[1] - 5 <= p4[1] <= p1[1] + 5:
                # pygame.draw.circle(screen, (150, 150, 15), (p1[0], p1[1]), 5)
                return (p1[0], p1[1], borot.theta())
            else:
                # pygame.draw.circle(screen, (150, 150, 15), (p2[0], p2[1]), 5)
                return (p2[0], p2[1], borot.theta())

    @staticmethod
    def circle_intersection(borot, x0, y0, r0, x1, y1, r1):
        d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

        if d > r0 + r1:
            return (0, 0), (0, 0), (0, 0), (0, 0)
        elif d < abs(r0 - r1):
            return (0, 0), (0, 0), (0, 0), (0, 0)
        elif d == 0 and r0 == r1:
            return (0, 0), (0, 0), (0, 0), (0, 0)
        else:
            a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(abs(r0 ** 2 - a ** 2))
            x2 = x0 + a * (x1 - x0) / d
            y2 = y0 + a * (y1 - y0) / d
            x3 = x2 + h * (y1 - y0) / d
            y3 = y2 - h * (x1 - x0) / d

            x4 = x2 - h * (y1 - y0) / d
            y4 = y2 + h * (x1 - x0) / d

            # pygame.draw.circle(screen, circle_color, (x3, y3), 5)
            # pygame.draw.circle(screen, circle_color, (x4, y4), 5)
            # print(x3, y3, x4, y4)
            # print("Fi0 ", fi0)
            # print("Fi1 ", fi1)

            fi03 = math.atan2((y0 - y3),
                              (x0 - x3)) - borot.theta()
            fi13 = math.atan2((y1 - y3),
                              (x1 - x3)) - borot.theta()
            fi04 = math.atan2((y0 - y4),
                              (x0 - x4)) - borot.theta()
            fi14 = math.atan2((y1 - y4),
                              (x1 - x4)) - borot.theta()

            # print("FI pot pos 1 w beacon 1 ", fi03)
            # print("FI pot pos 1 w beacon 2 ", fi13)
            # print("FI pot pos 2 w beacon 1", fi04)
            # print("FI pot pos 2 w beacon 2", fi14)

            return (int(x3), int(y3)), (int(x4), int(y4)), (-fi03, -fi13), (-fi04, -fi14)

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
