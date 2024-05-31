import math

import numpy as np
import pygame

from models.action import Action
from models.filter import KalmanFilter

CHANGE_BY = 5
N_SENSORS = 12

SENSOR_LENGTH = 40

SIGMA_MOV = 0.1
SIGMA_ROT = 0.1
SIGMA_SER_MOV = 0.01
SIGMA_SER_ROT = 0.01


class Borot:
    def __init__(self):
        self.__position = (0, 0)
        self.__radius = 10
        self.__max_forward_speed = 20
        self.__max_backwards_speed = -20
        self.__theta = 0
        self.__v_l = 0
        self.__v_r = 0
        self.__sensors = []

        self.__trace = []
        self.__filter = KalmanFilter([self.position()[0], self.position()[1], self.theta()], SIGMA_MOV, SIGMA_ROT,
                                     SIGMA_SER_MOV, SIGMA_SER_ROT)
        self.__predicted_position = (0, 0, 0)

        self.init_sensors()

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
        
        # Ensure wheel speeds do not go negative
        self.__v_l = max(self.__v_l, 0)
        self.__v_r = max(self.__v_r, 0)

        # Debugging output
        # print(f'Action: {action}, Left Wheel Speed: {self.__v_l}, Right Wheel Speed: {self.__v_r}')


    def get_sensor_endpoint(self, degree: int) -> tuple:
        robot_x, robot_y = self.position()
        x = robot_x + math.cos(math.radians(degree)) * SENSOR_LENGTH
        y = robot_y + math.sin(math.radians(degree)) * SENSOR_LENGTH
        return x, y

    def get_sensor_line(self, degree: int) -> tuple:
        x, y = self.get_sensor_endpoint(degree)
        robot_x, robot_y = self.position()
        return robot_x, robot_y, x, y

    def init_sensors(self):
        sensors = []

        for degree in range(0, 360, 30):
            x, y = self.get_sensor_endpoint(degree)
            sensors.append((degree, (x, y), SENSOR_LENGTH))

        self.__sensors = sensors

    def compute_sensor_distances(self, obstacles: list, landmarks: list) -> None:
        current_degree = 0
        relative_increase = 360 / N_SENSORS

        sensors = []

        robot_position = self.position()
        robot_x = robot_position[0]
        robot_y = robot_position[1]
        robot_vec2 = pygame.math.Vector2(robot_x, robot_y)

        # Initial closest landmark determination
        closest_landmark = None
        min_landmark_distance = SENSOR_LENGTH  # Only consider landmarks within sensor length

        for landmark in landmarks:
            landmark_position = pygame.math.Vector2(landmark)
            distance_to_landmark = (robot_vec2 - landmark_position).length()

             # Check if the landmark is within the sensor's range
            if distance_to_landmark <= SENSOR_LENGTH:
                can_see = True
                for obstacle in obstacles:
                    obstacle_vec2 = pygame.Rect(obstacle)

                    lm_x = landmark[0]
                    lm_y = landmark[1]

                    if landmark[0] > robot_x:
                        lm_x -= 1
                    else:
                        lm_x += 1

                    if landmark[1] > robot_y:
                        lm_y -= 1
                    else:
                        lm_y += 1

                    sensor_vec2 = pygame.math.Vector2(lm_x, lm_y)

                    intersections = obstacle_vec2.clipline(robot_vec2, sensor_vec2)

                    if intersects := intersections:
                        for point in intersects:
                            can_see = False
                            break

                        if not can_see:
                            break

                if can_see:
                    # Append the landmark and its distance to the list, adjusting for the robot's radius
                    sensors.append(('Landmark', landmark, distance_to_landmark - self.radius()))

        for _ in range(N_SENSORS):
            x, y = self.get_sensor_endpoint(current_degree)

            closest_point = (x, y)
            min_distance = None

            for obstacle in obstacles:
                obstacle_vec2 = pygame.Rect(obstacle)
                sensor_vec2 = pygame.math.Vector2(x, y)

                intersections = obstacle_vec2.clipline(robot_vec2, sensor_vec2)
                if intersects := intersections:
                    for point in intersects:
                        intersection_point = pygame.math.Vector2(point)
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

    def get_landmark_sensors(self):
        return [sensor[1] for sensor in self.__sensors if sensor[0] == 'Landmark']

    def get_obstacle_sensors(self):
        return [sensor for sensor in self.__sensors if sensor[0] != 'Landmark']

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

    def find_beacons(self):
        beacons = self.get_landmark_sensors()
        sensor_range = SENSOR_LENGTH
        sensor_x = self.position()[0]
        sensor_y = self.position()[1]

        beacons_in_proximity = []
        collision_offset = 0

        for bc in range(len(beacons)):
            dist = (math.sqrt(
                (beacons[bc][1] - sensor_y) ** 2 + (beacons[bc][0] - sensor_x) ** 2)) - collision_offset
            if dist < sensor_range:
                fi = math.atan2((beacons[bc][1] - sensor_y),
                                (beacons[bc][0] - sensor_x)) - self.theta()
                beacons_in_proximity.append(
                    (beacons[bc][0], beacons[bc][1], dist + collision_offset, -fi))

        if len(beacons_in_proximity) == 2:
            x0 = beacons_in_proximity[0][0]
            y0 = beacons_in_proximity[0][1]
            r0 = beacons_in_proximity[0][2]
            f0 = beacons_in_proximity[0][3]
            x1 = beacons_in_proximity[1][0]
            y1 = beacons_in_proximity[1][1]
            r1 = beacons_in_proximity[1][2]
            f1 = beacons_in_proximity[1][3]

            p1, p2, fipos1, fipos2 = self.circle_intersection(x0, y0, r0, x1, y1, r1)

            if f0 - 0.2 <= fipos1[0] <= f0 + 0.2 and f1 - 0.2 <= fipos1[1] <= f1 + 0.2:
                return (p1[0], p1[1], self.theta())
            else:
                return (p2[0], p2[1], self.theta())

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

            p1, p2, fipos1, fipos2 = self.circle_intersection(x0, y0, r0, x1, y1, r1)
            p3, p4, fipos3, fipos4 = self.circle_intersection(x0, y0, r0, x2, y2, r2)
            p5, p6, fipos5, fipos6 = self.circle_intersection(x1, y1, r1, x2, y2, r2)

            if p1[0] - 5 <= p3[0] <= p1[0] + 5 and p1[1] - 5 <= p3[1] <= p1[1] + 5:
                return (p1[0], p1[1], self.theta())
            elif p1[0] - 5 <= p4[0] <= p1[0] + 5 and p1[1] - 5 <= p4[1] <= p1[1] + 5:
                return (p1[0], p1[1], self.theta())
            else:
                return (p2[0], p2[1], self.theta())

    def predicted_position(self):
        return self.__predicted_position

    def set_predicted_position(self, predicted_position: tuple) -> None:
        self.__predicted_position = predicted_position

    def circle_intersection(self, x0, y0, r0, x1, y1, r1):
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

            fi03 = math.atan2((y0 - y3),
                              (x0 - x3)) - self.theta()
            fi13 = math.atan2((y1 - y3),
                              (x1 - x3)) - self.theta()
            fi04 = math.atan2((y0 - y4),
                              (x0 - x4)) - self.theta()
            fi14 = math.atan2((y1 - y4),
                              (x1 - x4)) - self.theta()

            return (int(x3), int(y3)), (int(x4), int(y4)), (-fi03, -fi13), (-fi04, -fi14)
