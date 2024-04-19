from __future__ import annotations

from copy import deepcopy

from models.action import Action
from models.borot import Borot
from models.world import World
from utils import galilei
from utils.utils import intersects


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

        new_state.borot().compute_sensor_distances(current_state.obstacles())

        if not any(intersects(new_state.borot().position_with_body(), obstacle) for obstacle in self.obstacles()):
            return new_state

        # The Robot Crashed and its velocity is 0 again. Theta remains as is.
        collision_state = deepcopy(self)
        collision_state.borot().crash()
        return collision_state
