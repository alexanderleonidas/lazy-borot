import numpy as np
import math


class KalmanFilter:

    def __init__(self, dt, state, sigma_mov, sigma_rot, sigma_ser_mov, sigma_ser_rot):
        # state = [x,y,theta]
        self.state = state
        self.theta = state[2]

        # prediction/transition matrix
        self.A = np.eye(3)

        # control matrix
        self.B = [[dt * np.cos(self.theta), 0],
                  [dt * np.sin(self.theta), 0], [0, dt]]
        
        # sensor information
        self.C = np.eye(3)

        # sensor noise, initialize with small value
        self.Q = np.dot(np.eye(3), 1) * np.array([sigma_ser_mov, sigma_ser_mov, sigma_ser_rot])  

        # process noise, initialize with small values
        self.R = np.dot(np.eye(3), 1) * np.array([sigma_mov, sigma_mov, sigma_rot])

        # previous coveriance, #initialize with small values
        self.S = np.eye(3) * 0.001

        # get z and C from the sensors
        self.predictiontrack = [(state[0], state[1])]

        self.m = self.state

        # ellipses stuff
        self.history = []
        self.location = []
        self.counter = 0

    def localization(self, z, v, w, m):

        # -----prediction-----
        self.m = m

        # -----covariance prediction-----
        self.S = np.matmul(np.matmul(self.A, self.S), np.transpose(self.A)) + self.R

        # ------correction-----
        a = np.matmul(np.matmul(self.C, self.S), np.transpose(self.C)) + self.Q
        a1 = np.linalg.inv(a)
        K = np.matmul(np.matmul(self.S, np.transpose(self.C)), a1)

        # draw every 20 step
        self.counter += 1
        if self.counter % 30 == 0:
            self.history.append(self.ellipses())
            self.location.append((self.state[0], self.state[1]))

        # new state
        if z == None:
            m = self.m
            self.predictiontrack.append([m[0], m[1], m[2]])

            self.state = m
            return 0
        else:
            m = self.m + np.matmul(K, (z - np.matmul(self.C, self.m)))
            S = np.matmul(self.A - np.matmul(K, self.C), self.S)
            self.predictiontrack.append([m[0], m[1], m[2]])

            self.state = m
            self.S = S
            self.m = m
            return 1
        
    def ellipses(self):
        # ------visualize-----
        a = self.S[0][0]
        b = self.S[0][1]
        c = self.S[1][1]
        l1 = (a + c) / 2 + np.sqrt(((a - c) / 2) ** 2 + b ** 2)
        l2 = (a + c) / 2 - np.sqrt(((a - c) / 2) ** 2 + b ** 2)
        if b == 0 and a >= c:
            theta = 0
        if b == 0 and a < c:
            theta = np.pi / 2
        else:
            theta = math.atan2(l1 - a, b)
        x = np.sqrt(abs(l1))
        y = np.sqrt(abs(l2))
        ellipse = (x, y, math.degrees(theta))
        return ellipse







