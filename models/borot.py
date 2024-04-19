import math

from models.action import Action
from utils.utils import intersects, intersects_closest_point, distance_between_points, clipline, vector_length_squared

CHANGE_BY = 5
N_SENSORS = 1
SENSOR_DEGREES = [
    0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330
]

SENSOR_LENGTH = 50


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
        self.compute_sensor_distances([])

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

    def compute_sensor_distances(self, obstacles: list) -> None:
        current_degree = 0
        relative_increase = 360 / N_SENSORS

        sensors = []

        robot_position = self.position()
        robot_x = robot_position[0]
        robot_y = robot_position[1]

        for _ in range(N_SENSORS):
            x = self.__position[0] + math.cos(math.radians(current_degree)) * SENSOR_LENGTH
            y = self.__position[1] + math.sin(math.radians(current_degree)) * SENSOR_LENGTH

            closest_point = (x, y)
            min_distance = SENSOR_LENGTH

            has_intersections = None

            for obstacle in obstacles:
                intersections = clipline((robot_x, robot_y, x, y), obstacle)

                if intersections is None:
                    print("No intersection")
                    continue

                if intersects := intersections:
                    for point in intersects:

                        intersection_point = point

                        distance = vector_length_squared(((self.position()[0] - intersection_point[0]), (self.position()[1] - intersection_point[1])))

                        print(distance)
                        if distance < min_distance:
                            min_distance = distance
                            closest_point = intersection_point

            sensors.append(closest_point)
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

    def speed(self) -> tuple:
        return self.__v_l, self.__v_r

    def sensors(self) -> list:
        return self.__sensors

    def crash(self) -> None:
        self.__v_l = 0
        self.__v_r = 0
