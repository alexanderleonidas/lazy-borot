import pygame
import math
import random
from Physics import Physics

SENSOR_LENGTH = 100  # Length of each sensor
SENSOR_COUNT = 12  # Number of sensors
RED = (255, 0, 0) 
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Borot:
    def __init__(self):
        self.position = pygame.math.Vector2(20,20)
        self.radius = 10
        self.theta = 0  # in radians
        self.direction = pygame.math.Vector2(math.cos(self.theta), math.sin(self.theta))
        self.sensor_directions = [self.direction.rotate(i * 2 * math.pi / SENSOR_COUNT) for i in range(SENSOR_COUNT)]
        self.sensor_endpoints = []
        self.v_l = 0
        self.v_r = 0
        self.max_speed = 20
        self.min_speed = -20
        self.wheel_base = 10
        self.axis_length = 50
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.update_rect() 
        self.physics = Physics(self.theta, self.radius, self.position, self.direction)

        
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

    def find_initial_borot_position(self, obstacles, screen_width, screen_height):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(self.radius, screen_width - self.radius)
            y = random.randint(self.radius, screen_height - self.radius)
            pos = pygame.Rect(x - self.radius, y - self.radius, 2 * self.radius, 2 * self.radius)
            if pos.collidelist(obstacles) == -1:  # Check if the circle does not collide with any obstacles
                self.position = pygame.math.Vector2(x, y)  # Return the position as a Vector2 for consistency
                break

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
            
# ----------------------------------------------- Testing Collision -----------------------------------------------#
    def detect_collision(self, obstacles):
        # Update the robot's bounding rectangle before checking for collisions
        self.update_rect()
        
        collision_info = {
            'collision': False,
            'new_position': self.position.copy(),
            'new_theta': self.theta
        }

        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):  # Use obstacle directly, since it's a pygame.Rect
                collision_info['collision'] = True
                collision_info['obstacle_rect'] = obstacle

                break #break after the first collision

        return collision_info

    def handle_collision(self, collision_info):
        if collision_info['collision']:
            obstacle_rect = collision_info['obstacle_rect']

            # Calculate overlaps in both dimensions
            horizontal_overlap = 0
            if self.rect.centerx < obstacle_rect.centerx:
                # Borot is to the left of the obstacle
                horizontal_overlap = self.rect.right - obstacle_rect.left
            else:
                # Borot is to the right of the obstacle
                horizontal_overlap = obstacle_rect.right - self.rect.left

            vertical_overlap = 0
            if self.rect.centery < obstacle_rect.centery:
                # Borot is above the obstacle
                vertical_overlap = self.rect.bottom - obstacle_rect.top
            else:
                # Borot is below the obstacle
                vertical_overlap = obstacle_rect.bottom - self.rect.top

            # Decide which way to move based on the smallest overlap
            if abs(horizontal_overlap) < abs(vertical_overlap):
                escape_vector = pygame.math.Vector2(-horizontal_overlap if self.rect.centerx < obstacle_rect.centerx else horizontal_overlap, 0)
            else:
                escape_vector = pygame.math.Vector2(0, -vertical_overlap if self.rect.centery < obstacle_rect.centery else vertical_overlap)

            # Apply the escape vector
            self.position += escape_vector
            self.update_rect()  # Update the rect after moving
            print(f"Adjusted position by {escape_vector} to resolve collision.")

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            2 * self.radius,
            2 * self.radius
        )

    def update_after_collision(self, collision_info):
        self.handle_collision(collision_info)
        self.physics.update_position(self.position, self.theta) 

    # ----------------------------------------------- Drawing Methods -----------------------------------------------#
    
    def draw(self, surface, font):
        self.draw_sensors(surface)
        pygame.draw.circle(surface, RED, self.position, self.radius)
        end_pos = self.position + self.direction * self.radius
        pygame.draw.line(surface, BLACK, self.position, end_pos, 2)
        self.draw_motor_speed(surface, font)
        self.draw_sensor_values(surface, font)  # Draw the sensor values
        self.draw_icc(surface) #draw ICC
        self.draw_axes(surface) #draw axes

    def draw_sensors(self, surface):
        for sensor_endpoint in self.sensor_endpoints:
            sensor_end = self.position + sensor_endpoint
            pygame.draw.line(surface, GREEN, self.position, sensor_end, 2)
            pygame.draw.circle(surface, BLUE, sensor_end, 2)

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

    def draw_motor_speed(self, surface,font):
        # Render the left and right motor speeds as text
        rotation_surface = font.render(f'Theta (rads): {self.theta}', False, RED)
        speed_left_surface = font.render(f'Left speed: {self.v_l}', False, RED)
        speed_right_surface = font.render(f'Right speed: {self.v_r}', False, RED)

        # Draw the text on the screen at a fixed position
        surface.blit(rotation_surface, (20, surface.get_height() - 60))
        surface.blit(speed_left_surface, (20, surface.get_height() - 50))  
        surface.blit(speed_right_surface, (20, surface.get_height() - 40)) 
    
    # This method to calculate and draw the ICC
    def draw_icc(self, surface):
        if self.v_r != self.v_l:  
            R = self.wheel_base * (self.v_l + self.v_r) / (2 * (self.v_r - self.v_l))
            ICC_x = self.position.x - R * math.sin(self.theta)
            ICC_y = self.position.y + R * math.cos(self.theta)
            ICC_position = (int(ICC_x), int(ICC_y))

            pygame.draw.circle(surface, YELLOW, ICC_position, 5)  # Draw ICC as a yellow circle
            pygame.draw.line(surface, RED, self.position, ICC_position, 1)

    def draw_axes(self, surface):
        # Calculate end points for the x-axis and y-axis
        end_x_axis = self.position + self.direction * self.axis_length
        normalized_direction = self.direction.normalize()
        end_y_axis = self.position + normalized_direction.rotate(90) * self.axis_length 

        pygame.draw.line(surface, RED, self.position, end_x_axis, 2)
        pygame.draw.line(surface, BLUE, self.position, end_y_axis, 2)
