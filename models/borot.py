import math

import numpy as np
import pygame

from models.action import Action
from models.filter import KalmanFilter
from utils.utils import distance_between_points, clipline

CHANGE_BY = 5
N_SENSORS = 12

SENSOR_LENGTH = 110

SIGMA_MOV = 0.1
SIGMA_ROT = 0.1
SIGMA_SER_MOV = 0.01
SIGMA_SER_ROT = 0.01


class Borot:
    def __init__(self):
        self.__position = (0, 0)
        self.__radius = 10
        self.__max_forward_speed = 40
        self.__max_backwards_speed = -40
        self.__theta = 0
        self.__v_l = 0
        self.__v_r = 0
        self.__sensors = []

        self.__trace = []
        self.__filter = KalmanFilter([self.position()[0], self.position()[1], self.theta()], SIGMA_MOV, SIGMA_ROT,
                                     SIGMA_SER_MOV, SIGMA_SER_ROT)

    def move(self, action: Action) -> None:
        if action == Action.INCREASE_RIGHT:
            self.__v_r = min(self.__v_r + CHANGE_BY, self.__max_forward_speed)
        elif action == Action.DECREASE_RIGHT:
            self.__v_r = max(self.__v_r - CHANGE_BY, self.__max_backwards_speed)
        elif action == Action.INCREASE_LEFT:
            self.__v_l = min(self.__v_l + CHANGE_BY, self.__max_forward_speed)
        elif action == Action.DECREASE_LEFT:
            self.__v_l = max(self.__v_l - CHANGE_BY, self.__max_backwards_speed)
        elif action == Action.BREAK:
            self.__v_l = 0
            self.__v_r = 0
        elif action == Action.NOTHING:
            pass

    def get_sensor_endpoint(self, degree: int) -> tuple:
        robot_x, robot_y = self.position()
        x = robot_x + math.cos(math.radians(degree)) * SENSOR_LENGTH
        y = robot_y + math.sin(math.radians(degree)) * SENSOR_LENGTH
        return x, y

    def get_sensor_line(self, degree: int) -> tuple:
        x, y = self.get_sensor_endpoint(degree)
        robot_x, robot_y = self.position()
        return robot_x, robot_y, x, y

    # TODO: Change Sensor Logic to use a continuous radius (radar-like) instead of a laser-like sensor
    def compute_sensor_distances(self, obstacles: list) -> None:
        current_degree = 0
        relative_increase = 360 / N_SENSORS

        sensors = []

        robot_position = self.position()
        robot_x = robot_position[0]
        robot_y = robot_position[1]

        for _ in range(N_SENSORS):
            x, y = self.get_sensor_endpoint(current_degree)

            closest_point = (x, y)
            min_distance = None

            for obstacle in obstacles:
                obstacle_vec2 = pygame.Rect(obstacle)
                robot_vec2 = pygame.math.Vector2(robot_x, robot_y)
                sensor_vec2 = pygame.math.Vector2(x, y)

                intersections = obstacle_vec2.clipline(robot_vec2, sensor_vec2)
                # intersections = clipline(obstacle, (robot_x, robot_y), (x, y))

                if intersects := intersections:
                    for point in intersects:
                        intersection_point = pygame.math.Vector2(point)
                        # distance = distance_between_points((x, y), point)
                        distance = (robot_vec2 - intersection_point).length()

                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                            closest_point = intersection_point

            if min_distance is None:
                min_distance = SENSOR_LENGTH

            min_distance = min_distance - self.radius()

            sensors.append((current_degree, closest_point, min_distance))
            current_degree += relative_increase

        self.__sensors = sensors

    def position(self) -> tuple:
        return self.__position

    def position_with_body(self) -> tuple:
        x, y = self.__position
        return x - self.__radius, y - self.__radius, self.__radius * 2, self.__radius * 2

    def update_position(self, new_position: tuple) -> None:
        self.__position = new_position

    def radius(self) -> int:
        return self.__radius

    def birth(self, location: tuple) -> None:
        self.__position = location

    def theta(self) -> float:
        return self.__theta

    def update_theta(self, new_theta: float) -> None:
        self.__theta = new_theta

    def update_speed(self, v_l: int, v_r: int) -> None:
        self.__v_l = v_l
        self.__v_r = v_r

    def speed(self) -> tuple:
        return self.__v_l, self.__v_r

    def sensors(self) -> list:
        return self.__sensors

    def crash(self) -> None:
        self.__v_l = 0
        self.__v_r = 0

    def trace(self) -> list:
        return self.__trace

    def add_trace(self, position: tuple) -> None:
        if len(self.__trace) > 1000:
            self.__trace.pop(0)

        self.__trace.append(position)

    def filter(self):
        return self.__filter


