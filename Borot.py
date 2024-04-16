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
        
    def draw(self, surface,font):
        self.draw_sensors(surface)
        pygame.draw.circle(surface, RED, self.position, self.radius)
        end_pos = self.position + self.direction * self.radius
        pygame.draw.line(surface, BLACK, self.position, end_pos, 2)
        self.draw_motor_speed(surface, font, v_l=0, v_r=0)
        self.draw_sensor_values(surface, font)  # Draw the sensor values

    def draw_sensors(self, surface):
        for sensor_endpoint in self.sensor_endpoints:
            sensor_end = self.position + sensor_endpoint
            pygame.draw.line(surface, GREEN, self.position, sensor_end, 2)
            pygame.draw.circle(surface, BLUE, sensor_end, 2)


    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.position += self.direction * 2  # Move 5 pixels forward
            v_r = 2
        if keys[pygame.K_DOWN]:
            v_r = 2
        if keys[pygame.K_LEFT]:
            self.direction.rotate_ip(-2)
            v_l = 2
        if keys[pygame.K_RIGHT]:
            self.direction.rotate_ip(2)
            
        # Update sensor positions to move with the robots front direction
        self.sensor_directions = [self.direction.rotate(i * 360 / SENSOR_COUNT) for i in range(SENSOR_COUNT)]

    def collision_detection(self, obstacles):
        self.sensor_endpoints.clear()
        for sensor_direction in self.sensor_directions:
            sensor_end = self.position + sensor_direction * SENSOR_LENGTH
            closest_point = sensor_end
            min_distance = SENSOR_LENGTH
            for obstacle in obstacles:
                # Check for intersection with each obstacle
                if intersects := obstacle.clipline(self.position, sensor_end):
                    for point in intersects:
                        intersection_point = pygame.math.Vector2(*point)
                        distance = (self.position - intersection_point).length()
                        if distance < min_distance:
                            min_distance = distance
                            closest_point = intersection_point
            # Store the vector from circle's center to the closest intersection or sensor end
            self.sensor_endpoints.append(closest_point - self.position)

    
    def find_initial_borot_position(self, obstacles, screen_width, screen_height):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(self.radius, screen_width - self.radius)
            y = random.randint(self.radius, screen_height - self.radius)
            pos = pygame.Rect(x - self.radius, y - self.radius, 2 * self.radius, 2 * self.radius)
            if pos.collidelist(obstacles) == -1:  # Check if the circle does not collide with any obstacles
                self.position = pygame.math.Vector2(x, y)  # Return the position as a Vector2 for consistency
                break

    def draw_sensor_values(self, surface,font):
        for i, sensor_endpoint in enumerate(self.sensor_endpoints):
            sensor_distance = sensor_endpoint.length() - self.radius  # Get the length of the vector
            textsurface = font.render(f'{sensor_distance:.1f}', False, RED)
            offset_distance = sensor_distance + 5 # Move the text a bit away from the sensor

            # Calculate and adjust the text position
            text_direction = sensor_endpoint.normalize() if sensor_distance != 0 else pygame.math.Vector2()
            text_pos = self.position + text_direction * offset_distance
            text_pos.x = max(min(text_pos.x, surface.get_width() - textsurface.get_width()), 0)
            text_pos.y = max(min(text_pos.y, surface.get_height() - textsurface.get_height()), 0)

            surface.blit(textsurface, text_pos)

    def draw_motor_speed(self, surface,font, v_l, v_r):
        # Render the left and right motor speeds as text
        speed_left_surface = font.render(f'Left Speed: {v_l}', False, (255, 0, 0))
        speed_right_surface = font.render(f'Right Speed: {v_r}', False, (255, 0, 0))

        # Draw the text on the screen at a fixed position
        surface.blit(speed_left_surface, (20, surface.get_height() - 50))  
        surface.blit(speed_right_surface, (20, surface.get_height() - 40)) 
