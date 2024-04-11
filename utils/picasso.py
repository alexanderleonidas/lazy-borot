import pygame
from pygame import Rect, Vector2

# Draws the map and robot
class Picasso:
    def __init__(self, world):
        self.world = world
        pygame.init()
        self.screen = pygame.display.set_mode((self.world.width, self.world.height))
        pygame.display.set_caption("Obstacle Avoidance")

        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        self.map_surface = pygame.Surface((self.world.width, self.world.height))

    def draw_obstacle_course(self):
        # Clear the surface by filling it with white
        self.map_surface.fill(self.WHITE)

        # Draw each obstacle onto the surface
        for obstacle in self.world.obstacles:
            pygame.draw.rect(self.map_surface, self.BLACK, Rect(Vector2(obstacle[0], obstacle[1]), Vector2(obstacle[2], obstacle[3])))

    def draw_robot(self, center, radius, direction=0):
        # Draw the Robot as a circle with a rectangle to indicate direction
        # Draw the red circle
        pygame.draw.circle(self.map_surface, self.RED, center, radius)

        # Draw the rectangle
        # Draw a line to indicate the front of the robot
        front_pos = center + pygame.Vector2(radius, 0).rotate(direction)
        pygame.draw.line(self.map_surface, self.BLACK, center, front_pos)
