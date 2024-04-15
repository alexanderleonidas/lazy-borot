import pygame
import math
import random


SENSOR_LENGTH = 100  # Length of each sensor
SENSOR_COUNT = 12  # Number of sensors
RED = (255, 0, 0) 
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Borot:
    def __init__(self, theta):
        self.position = pygame.math.Vector2
        self.radius = 10
        self.theta = theta  # in degrees
        self.direction = pygame.math.Vector2(math.cos(math.radians(theta)), math.sin(math.radians(theta)))
        self.sensor_directions = [self.direction.rotate(i * 360 / SENSOR_COUNT) for i in range(SENSOR_COUNT)]
        self.sensor_endpoints = []

    def draw(self, surface):
        self.draw_sensors(surface)
        pygame.draw.circle(surface, RED, (int(self.position.x), int(self.position.y)), self.radius)
        end_pos = self.position + self.direction * self.radius
        pygame.draw.line(surface, BLACK, self.position, end_pos, 2)

    def draw_sensors(self, surface):
        for sensor_endpoint in self.sensor_endpoints:
            pygame.draw.line(surface, GREEN, self.position, sensor_endpoint, 1)
            pygame.draw.circle(surface, BLUE, sensor_endpoint, 1)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.position += self.direction * 2  # Move 5 pixels forward
        if keys[pygame.K_LEFT]:
            self.direction.rotate_ip(-2)
        if keys[pygame.K_RIGHT]:
            self.direction.rotate_ip(2)
            
        # Update sensor positions to move with the robots front direction
        self.sensor_directions = [self.direction.rotate(i * 360 / SENSOR_COUNT) for i in range(SENSOR_COUNT)]

    def collision_detection(self, obstacles):
        self.sensor_endpoints.clear()
        for sensor_direction in self.sensor_directions:
            sensor_end = self.position + sensor_direction * SENSOR_LENGTH
            min_distance = SENSOR_LENGTH
            closest_intersection = sensor_end
            for obstacle in obstacles:
                if intersect := obstacle.clipline(self.position, sensor_end):
                    intersection_point = pygame.math.Vector2(*intersect[1])
                    distance = (self.position - intersection_point).length()
                    if distance < min_distance:
                        min_distance = distance
                        closest_intersection = intersection_point
            self.sensor_endpoints.append(closest_intersection)
    
    def find_initial_borot_position(self, obstacles, screen_width, screen_height):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(self.radius, screen_width - self.radius)
            y = random.randint(self.radius, screen_height - self.radius)
            pos = pygame.Rect(x - self.radius, y - self.radius, 2 * self.radius, 2 * self.radius)
            if pos.collidelist(obstacles) == -1:  # Check if the circle does not collide with any obstacles
                self.position = pygame.math.Vector2(x, y)  # Return the position as a Vector2 for consistency
                break