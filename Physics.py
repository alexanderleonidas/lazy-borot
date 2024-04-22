import numpy as np
import pygame
import math

class Physics:
    def __init__(self, theta, radius, position, direction):
        self.theta = theta  # Angle with x-axis in radians
        self.radius = radius  # Radius of the robot
        self.position = position  # Position of the robot as a pygame.Vector2
        self.direction = direction  # Direction vector of the robot as a pygame.Vector2

    def calculate_r(self, v_l, v_r):
        if v_r == v_l:
            return float('inf')  # Straight movement, infinite radius
        return (self.radius * (v_l + v_r)) / (v_r - v_l)

    def calculate_omega(self, v_l, v_r):
        return (v_r - v_l) / (2 * self.radius)

    def calculate_icc(self, r):
        dx = -r * math.sin(self.theta)
        dy = r * math.cos(self.theta)
        return self.position.x + dx, self.position.y + dy

    def motion(self, dt, w, icc, v):
        if w == 0:  # Movement is straight
            self.position += self.direction * v * dt
        else:
            # Calculate the new position and orientation
            rotation_matrix = np.array([
                [np.cos(w * dt), -np.sin(w * dt), 0],
                [np.sin(w * dt), np.cos(w * dt), 0],
                [0, 0, 1]
            ])
            transform_vector = np.array([
                self.position.x - icc[0],
                self.position.y - icc[1],
                self.theta
            ])
            new_position = rotation_matrix.dot(transform_vector)
            new_position += np.array([icc[0], icc[1], w * dt])
            self.position.x, self.position.y, self.theta = new_position
            self.direction = pygame.math.Vector2(math.cos(self.theta), math.sin(self.theta))

    def apply(self, dt, v_l, v_r):
        if v_l == v_r:
            # Straight movement or stationary
            self.position += self.direction * v_l * dt
        elif v_l == -v_r:
            # Rotation in place
            self.theta += self.calculate_omega(v_l, v_r) * dt
            self.direction = pygame.math.Vector2(math.cos(self.theta), math.sin(self.theta))
        else:
            r = self.calculate_r(v_l, v_r)
            w = self.calculate_omega(v_l, v_r)
            icc = self.calculate_icc(r)
            self.motion(dt, w, icc, (v_l + v_r)/2 )
    
 # ----------------------------------------------- Testing Collision -----------------------------------------------#   
    def update_position(self, position, theta):
        self.position = position
        self.theta = theta
        
    '''def handle_collision(self, tangential_velocity):
        if tangential_velocity.length() > 0:
            self.direction = tangential_velocity.normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)  # Stop any movement if no tangential component
        
        # Update position with the new direction and speed
        self.position += self.direction * tangential_velocity.length()
        # Update theta to face along the direction of movement
        self.theta = self.direction.angle_to(pygame.math.Vector2(1, 0))'''
    






