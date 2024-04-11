from typing import Tuple
import numpy as np
import pygame, math

import numpy as np

BOROT_SIZE = 10

class Borot:
    def __init__(self, name, world) -> None:
        self.name = name
        self.position: Tuple[int, int] = (0, 0)
        self.radius = BOROT_SIZE
        self.world = world
        self.rotation = 0
        self.icc: Tuple[float, float] = (0, 0)  # Instantaneous Center of Curvature
        self.Vl = 0  # left velocity
        self.Vr = 0  # right velocity
        self.theta = 0
        self.speed = 5

    def get_position(self) -> Tuple[int, int]:
        return self.position

    def moving_keys(self, keys, dt, screen, player):
        self.screen = screen
        self.x = self.position[0]  # starting x
        self.y = self.position[1]  # starting y
        self.radius = player

        # keys = [w, s, o, l, x, t, g]
        # TODO: Check if this is correct and as expected
        if keys[0] == 1 or keys[5] == 1:
            self.Vr += self.speed
            print(self.Vr)
        elif keys[1] == 1 or keys[6] == 1:
            self.Vr -= self.speed
        elif keys[2] == 1 or keys[5] == 1:
            self.Vl += self.speed
        elif keys[3] == 1 or keys[6] == 1:
            self.Vl -= self.speed
        elif keys[4] == 1:
            self.Vl = 0
            self.Vr = 0

        # If it's moving
        if self.Vr != 0 or self.Vl != 0:

            # Make sure not to get a division by zero when velocities are the same
            if self.Vr == self.Vl:
                next_x = self.x + ((self.Vl + self.Vr) / 2) * np.cos(self.theta) * dt
                next_y = self.y - ((self.Vl + self.Vr) / 2) * np.sin(self.theta) * dt
                new_theta = self.theta + (self.Vr - self.Vl) / (2 * self.radius) * dt
                self.position = (next_x, next_y)
            else:
                R = self.radius * (self.Vl + self.Vr) / (self.Vr - self.Vl)
                w = (self.Vr - self.Vl) / (self.radius * 2)
                # Compute ICC
                ICC = [self.x - R * np.sin(-self.theta), self.y + R * np.cos(self.theta)]
                result = np.transpose(np.matmul(
                    np.array([[np.cos(w * dt), -np.sin(w * dt), 0],
                              [np.sin(w * dt), np.cos(w * dt), 0],
                              [0, 0, 1]]),
                    np.transpose(np.array([self.x - ICC[0], self.y - ICC[1], self.theta]))) + np.array(
                    [ICC[0], ICC[1], w * dt])).transpose()
                next_x, next_y, new_theta = result[0], result[1], result[2]  # info for updateding the sensors
                self.position = (next_x, next_y)
