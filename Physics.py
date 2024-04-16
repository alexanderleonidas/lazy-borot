import numpy as np
import pygame
import math

class Physics:
    def __init__(self, theta, radius, position:pygame.Vector2, direction:pygame.Vector2) -> None:
        self.theta = theta # Angle with x axis
        self.radius = radius # Radius of Borot
        self.position = position # Borot position
        self.direction = direction

    def calculate_r(self, v_l, v_r):
        return (self.radius) * ((v_l + v_r) / (v_r - v_l))

    def calculate_omega(self, v_l, v_r):
        return (v_r - v_l) / (self.radius * 2)

    def calculate_icc(self, r):
        return self.position.x - r * math.sin(self.theta),self.position.y + r * math.cos(self.theta)

    def motion(self,dt,  w, icc):
        a = np.array([[np.cos(w * dt), -np.sin(w * dt), 0],
                        [np.sin(w * dt), np.cos(w * dt), 0],
                            [0, 0, 1]])
        b = np.array([self.position.x - icc[0], self.position.y - icc[1], self.theta])
        c = np.array([icc[0], icc[1], w * dt])
        return np.matmul(a,b) + c.transpose()


    def apply(self, dt, v_l, v_r):
        if (v_l == 0 and v_r ==0):
            # Stationary
            return
        elif (v_l == v_r):
            # lateral movement
            self.position += self.direction * v_l * dt
        # elif (v_l == - v_r or - v_l == v_r):
        #     # Rotation in place
        #     pass
        # elif ((v_l == 0 and v_r != 0) or (v_r == 0 and v_l != 0)):
        #     # Rotation about left or right wheel
        #     pass
        else:
            r = self.calculate_r(v_l, v_r)
            w = self.calculate_omega(v_l, v_r)
            icc = self.calculate_icc(r)
            d_pos = self.motion(dt, w,icc)
            self.position.x = d_pos[0]
            self.position.y = d_pos[1]
            self.theta = d_pos[2]
            self.direction.rotate_ip(self.theta)

        