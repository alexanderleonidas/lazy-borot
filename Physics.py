import numpy as np
import pygame
import math

class Physics:
    def __init__(self, dt, v_l, v_r, theta, radius, position:pygame.Vector2) -> None:
        self.v_l = v_l # Left wheel velocity
        self.v_r = v_r # Right wheel velocity
        self.theta = theta # Angle with x axis
        self.radius = radius # Radius of Borot
        self.position = position # Borot position
        self.dt = dt #  Time step

    def calculate_r(self, radius, v_l, v_r):
        return (radius) * ((v_l + v_r) / (v_r - v_l))

    def calculate_omega(self, radius, v_l, v_r):
        return (v_r - v_l) / (radius * 2)

    def calculate_icc(self, r):
        return self.position.x - r * math.sin(self.theta),self.position.y + r * math.cos(self.theta)

    def motion(self, w, icc):
        a = np.array([[np.cos(w * self.dt), -np.sin(w * self.dt), 0],
                        [np.sin(w * self.dt), np.cos(w * self.dt), 0],
                            [0, 0, 1]])
        b = np.array([self.position.x - icc[0], self.position.y - icc[1], self.theta])
        c = np.array([icc[0], icc[1], w * self.dt])
        return np.matmul(a,b) + c.transpose()


    def apply(self):
        if(self.v_l == self.v_r):
            # No rotation
            pass
        elif(self.v_l == -self.v_r):
            # Rotation in place
            pass
        elif(self.v_l == 0 or self.v_r == 0):
            # Rotation about left or right wheel
            pass
        else:
            r = self.calculate_r(self.radius,self.v_l,self.v_r)
            w = self.calculate_omega(self.radius, self.v_l, self.v_r)
            icc = self.calculate_icc(r)
            d_pos = self.motion(w,icc)
            self.position.x += d_pos[0]
            self.position.y += d_pos[1]
            self.theta += d_pos[2]

        