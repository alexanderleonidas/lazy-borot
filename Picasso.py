# Imports
import pygame
import random

# Draws onto pygame surface
class Picasso:
    def __init__(self, surface:pygame.Surface):
        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Coordinate list of obstacles
        self.space = []

        # Initiallize Surface
        self.surface = surface

        # Set dimensions
        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()
        self.wall_thickness = 15
        self.obstacle_height, self.obstacle_width = 40, 40
        self.n_obstacles = 45

    def draw_walls(self):
        # Draw walls around the screen
        walls = [
            pygame.Rect(0, 0, self.screen_width, self.wall_thickness),  # Top wall
            pygame.Rect(0, 0, self.wall_thickness, self.screen_height),  # Left wall
            pygame.Rect(self.screen_width - self.wall_thickness, 0, self.wall_thickness, self.screen_height),  # Right wall
            pygame.Rect(0, self.screen_height - self.wall_thickness, self.screen_width, self.wall_thickness)  # Bottom wall
        ]
        for wall in walls:
            pygame.draw.rect(self.surface, self.BLACK, wall)
            self.space.append(wall)

    def draw_obstacles(self):
        # Create Obstacles
        for _ in range(self.n_obstacles):
            lim = 0
            while True:
                x = random.randint(1, (self.screen_width - self.obstacle_width) // self.obstacle_width) * self.obstacle_width
                y = random.randint(1, (self.screen_width - self.obstacle_height) // self.obstacle_height) * self.obstacle_height
                obstacle = pygame.Rect(x, y, self.obstacle_width, self.obstacle_height)

                # Ensure there's a clear path by avoiding the direct line from start to end
                if self.obstacle_height < y < self.screen_width - 2 * self.obstacle_height:
                    self.space.append(obstacle)
                    pygame.draw.rect(self.surface, self.BLACK, obstacle)
                    break
                # Break if the loop runs for too long
                if lim > 100:
                    break
                lim += 1

    def draw(self):
        self.surface.fill((0,0,0,0))
        self.draw_walls()
        self.draw_obstacles() 