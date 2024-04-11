import pygame
from pygame import Rect, Vector2

# Draws the map and robot
class Picasso:
    def __init__(self, world):
        self.world = world

        # Colours
        self.WALL_COLOR = (0, 0, 0)
        self.FLOOR_COLOR = (255, 255, 255)
        self.AGENT_COLOR = (255, 0, 0)
        self.AGENT_DIR_COLOR = (0, 255, 0)

        self.map_surface = pygame.Surface((self.world.width, self.world.height))

    def draw_wall(self, wall):
        pygame.draw.rect(self.map_surface, self.WALL_COLOR, Rect(wall.top_left, wall.bottom_right))

    def draw_map(self):
        self.map_surface.fill(self.FLOOR_COLOR)
        for wall in self.world.walls:
            self.draw_wall(wall)

    def draw_robot(self, center, radius, direction=0):
        # Draw the Robot as a circle with a rectangle to indicate direction
        # Draw the red circle
        pygame.draw.circle(self.map_surface, self.AGENT_COLOR, center, radius)

        # Draw the rectangle
        # Draw a line to indicate the front of the robot
        front_pos = center + pygame.Vector2(radius, 0).rotate(direction)
        pygame.draw.line(self.map_surface, self.WALL_COLOR, center, front_pos)
