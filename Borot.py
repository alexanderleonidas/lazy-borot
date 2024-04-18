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
    def __init__(self):
        self.position = pygame.math.Vector2
        self.radius = 10
        self.theta = 0  # in radians
        self.direction = pygame.math.Vector2(math.cos(self.theta), math.sin(self.theta))
        self.sensor_directions = [self.direction.rotate(i * 2 * math.pi / SENSOR_COUNT) for i in range(SENSOR_COUNT)]
        self.sensor_endpoints = []
        self.v_l = 0
        self.v_r = 0
        self.max_speed = 20
        self.min_speed = -20

    def update(self, new_pos, new_direction, new_theta):
        self.position = new_pos
        self.direction = new_direction
        self.theta = new_theta
        
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    self.v_r = min(self.v_r + 2, self.max_speed)
                if event.key == pygame.K_k:
                    self.v_r = max(self.v_r - 2, self.min_speed)
                if event.key == pygame.K_w:
                    self.v_l = min(self.v_l + 2, self.max_speed)
                if event.key == pygame.K_s:
                    self.v_l = max(self.v_l - 2, self.min_speed)
                if event.key == pygame.K_SPACE:
                    self.v_l = 0
                    self.v_r = 0
            # Quit Game
            if event.type == pygame.QUIT:
                return False
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

    # ----------------------------------------------- Drawing Methods -----------------------------------------------#
    
    def draw(self, surface,font):
        self.draw_sensors(surface)
        pygame.draw.circle(surface, RED, self.position, self.radius)
        end_pos = self.position + self.direction * self.radius
        pygame.draw.line(surface, BLACK, self.position, end_pos, 2)
        self.draw_motor_speed(surface, font)
        self.draw_sensor_values(surface, font)  # Draw the sensor values

    def draw_sensors(self, surface):
        for sensor_endpoint in self.sensor_endpoints:
            sensor_end = self.position + sensor_endpoint
            pygame.draw.line(surface, GREEN, self.position, sensor_end, 2)
            pygame.draw.circle(surface, BLUE, sensor_end, 2)

    def draw_sensor_values(self, surface, font):
        for i, sensor_endpoint in enumerate(self.sensor_endpoints):
            sensor_distance = sensor_endpoint.length() - self.radius
            textsurface = font.render(f'{sensor_distance:.1f}', False, RED)

            # Calculate and adjust the text position only if the vector is not zero-length
            if sensor_endpoint.length_squared() != 0:
                text_direction = sensor_endpoint.normalize()
                offset_distance = sensor_distance + 5  # Move the text a bit away from the sensor
                text_pos = self.position + text_direction * offset_distance
            else:
                # If the vector is zero-length, no offset is needed; use the current position
                text_pos = self.position

            # Ensure the text is within the screen bounds
            text_pos.x = max(min(text_pos.x, surface.get_width() - textsurface.get_width()), 0)
            text_pos.y = max(min(text_pos.y, surface.get_height() - textsurface.get_height()), 0)

            # Draw the text at the calculated position
            surface.blit(textsurface, text_pos)



    def draw_motor_speed(self, surface,font):
        # Render the left and right motor speeds as text
        rotation_surface = font.render(f'Theta (rads): {self.theta}', False, RED)
        speed_left_surface = font.render(f'Left speed: {self.v_l}', False, RED)
        speed_right_surface = font.render(f'Right speed: {self.v_r}', False, RED)

        # Draw the text on the screen at a fixed position
        surface.blit(rotation_surface, (20, surface.get_height() - 60))
        surface.blit(speed_left_surface, (20, surface.get_height() - 50))  
        surface.blit(speed_right_surface, (20, surface.get_height() - 40)) 

