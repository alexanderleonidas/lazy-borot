import math
import pygame


# Handles collision detection
class Sensors:
    def __init__(self, player_pos, screen):
        self.player_pos: tuple = player_pos
        self.screen = screen
        # self.obstacles = obstacles  # Assume this is a list of obstacle objects
        self.STEP_ANGLE = (math.pi * 2) / 12
        self.SENSORS_FONT = pygame.font.SysFont("comicsans", 15)
        self.sensor_length = 80  # Maximum sensor ray length

    def test_cast_rays(self):
        temp_angle = 0
        for _ in range(12):
            end_x = self.player_pos[0] + math.cos(temp_angle) * self.sensor_length
            end_y = self.player_pos[1] + math.sin(temp_angle) * self.sensor_length
            pygame.draw.line(self.screen, (0, 0, 0), (self.player_pos[0], self.player_pos[1]), (end_x, end_y), 1)
            temp_angle += self.STEP_ANGLE

    def cast_rays(self):
        self.all_sensors = []
        temp_angle = 0
        for i in range(12):
            self.all_sensors.append({
                "x": self.player_pos[0],
                "y": self.player_pos[1],
                "angle": temp_angle,
                "index": i
            })

        temp_angle += self.STEP_ANGLE

    def detect_collisions(self):
        for sensor in self.all_sensors:
            sensor['distance'] = 200  # Default distance if no collision
            sensor['collision_point'] = None
            for depth in range(200):
                target_x = sensor['x'] - math.sin(sensor['angle']) * depth
                target_y = sensor['y'] + math.cos(sensor['angle']) * depth
                ray = ((sensor['x'], sensor['y']), (target_x, target_y))
                for obstacle in self.obstacles:
                    clipped_line = obstacle.clipline(ray)
                    if clipped_line:
                        distance = int(math.sqrt(
                            (clipped_line[0][1] - sensor['y']) ** 2 + (clipped_line[0][0] - sensor['x']) ** 2)) - 32
                        if distance < sensor['distance']:
                            sensor['distance'] = distance
                            sensor['collision_point'] = clipped_line[0]

    def draw_sensors(self):
        for sensor in self.all_sensors:
            sensor_x, sensor_y = sensor['x'], sensor['y']
            if sensor['collision_point']:
                pygame.draw.line(self.screen, (255, 130, 100), (sensor_x, sensor_y), sensor['collision_point'], 3)
                sensor_text = self.SENSORS_FONT.render(str(sensor['distance']), True, (255, 255, 255))
                self.screen.blit(sensor_text, sensor['collision_point'])
            else:
                # If no collision, optionally draw the sensor line to its maximum extent
                end_x = sensor_x - math.sin(sensor['angle']) * sensor['distance']
                end_y = sensor_y + math.cos(sensor['angle']) * sensor['distance']
                pygame.draw.line(self.screen, (255, 255, 255), (sensor_x, sensor_y), (end_x, end_y), 1)
