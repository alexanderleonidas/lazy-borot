import math
import pygame


class Sensors:
    def __init__(self, player_pos, screen):
        self.player_pos = player_pos
        self.screen = screen
        #self.obstacles = obstacles  # Assume this is a list of obstacle objects
        self.STEP_ANGLE = (math.pi * 2) / 12
        self.SENSORS_FONT = pygame.font.SysFont("comicsans", 15)
        self.sensor_length = 100  # Maximum sensor ray length

        
    def cast_rays(self):
        temp_angle = 0
        for i in range(12):
            end_x = self.player_pos.x + math.cos(temp_angle) * self.sensor_length
            end_y = self.player_pos.y + math.sin(temp_angle) * self.sensor_length
            pygame.draw.line(self.screen, (255, 255, 255), (self.player_pos.x, self.player_pos.y), (end_x, end_y), 1)
            temp_angle += self.STEP_ANGLE
    

    def detect_collisions(self):
        temp_angle = 0
        for i in range(12):
            sensor_end_x = self.player_pos.x + math.cos(temp_angle) * self.sensor_length
            sensor_end_y = self.player_pos.y + math.sin(temp_angle) * self.sensor_length

            # Initialize ray
            ray = ((self.player_pos.x, self.player_pos.y), (sensor_end_x, sensor_end_y))
            detected = []

            # Check each obstacle for collision with the ray
            for obstacle in self.obstacles:
                clipped_line = obstacle.clipline(ray)
                if clipped_line:
                    detected.append(clipped_line)

            # Find the closest collision, if any
            if detected:
                closest_collision = min(detected, key=lambda cl: self._distance_from_player(cl[0]))
                self._handle_collision(closest_collision, temp_angle)

            temp_angle += self.STEP_ANGLE


    def _handle_collision(self, collision, angle):
        collision_point = collision[0]
        distance = self._distance_from_player(collision_point)
        # Draw a line to the collision point
        pygame.draw.line(self.screen, (255, 130, 100), (self.player_pos.x, self.player_pos.y),
                         collision_point, 3)
        # Display the distance
        sensor_text = self.SENSORS_FONT.render(f"{distance}", 1, (255, 255, 255))
        self.screen.blit(sensor_text, collision_point)


    def _distance_from_player(self, point):

        return int(math.sqrt((point[1] - self.player_pos.y) ** 2 + (point[0] - self.player_pos.x) ** 2))