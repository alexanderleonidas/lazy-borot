from __future__ import annotations

import math
from copy import deepcopy

from models.action import Action
from models.borot import Borot
from models.world import World
from utils import galilei
from utils.utils import intersects, intersects_and_closest_point


class State:
    def __init__(self, time_step: int, world: World):
        self.__time_step = time_step
        self.__world = world

    def time_step(self) -> int:
        return self.__time_step

    def world(self) -> World:
        return self.__world

    def borot(self) -> Borot:
        return self.world().borot()

    def obstacles(self) -> list:
        return self.world().obstacles()

    def next(self, action: Action, dt) -> State:
        current_state = deepcopy(self)
        new_state = State(current_state.time_step() + 1, current_state.world())
        new_state.borot().move(action)

        x_prime, y_prime, theta_prime = galilei.apply(new_state, dt)

        new_state.borot().update_position((x_prime, y_prime))
        new_state.borot().update_theta(theta_prime)

        new_state.borot().compute_sensor_distances(new_state.obstacles())
        new_state.borot().add_trace(new_state.borot().position())

        # If there are no collisions return the next state
        if not any(intersects(new_state.borot().position_with_body(), obstacle) for obstacle in self.obstacles()):
            return new_state

        return self.collision_handling(new_state, dt)

    def collision_handling(self, new_state, dt):
        # The robot has collided with an obstacle and it should move along the tangent of the obstacle
        collision_state = deepcopy(self)
        collision_state.borot().update_theta(new_state.borot().theta())
        new_speed = new_state.borot().speed()
        collision_state.borot().update_speed(new_speed[0], new_speed[1])

        for obstacle in new_state.obstacles():
            robot_position = new_state.borot().position_with_body()
            found = intersects_and_closest_point(robot_position, obstacle)
            if found:
                escape_position = collision_state.borot().position()

                horizontal_overlap, vertical_overlap = found

                if abs(horizontal_overlap) < abs(vertical_overlap):
                    escape_vector = (-horizontal_overlap if robot_position[0] < obstacle[0] else horizontal_overlap, 0)
                else:
                    escape_vector = (0, -vertical_overlap if robot_position[1] < obstacle[1] else vertical_overlap)

                new_pos_x = escape_position[0] + escape_vector[0] * dt
                new_pos_y = escape_position[1] + escape_vector[1] * dt
                collision_state.borot().update_position((new_pos_x, new_pos_y))
                break

        collision_state.borot().compute_sensor_distances(collision_state.obstacles())
        collision_state.borot().add_trace(collision_state.borot().position())

        return collision_state
