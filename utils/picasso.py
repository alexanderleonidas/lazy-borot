import pygame
import sys
import random

class Graphics:
    def __init__(self, dimensions):
        # Initialize screen
        self.cell_size = 30
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        height = self.rows * self.cell_size
        width = self.columns * self.cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Obstacle Avoidance")

        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Map information
        self.map = []
        self.map_surface = pygame.Surface((width, height))

        # Robot position
        self.robot_position = None
    
    def create_obstacle_course(self, num_obstacles):
        for _ in range(num_obstacles):
            # Using vectors for position and size
            size = pygame.math.Vector2(random.randint(1, 5) * self.cell_size, random.randint(1, 3) * self.cell_size)
            position = pygame.math.Vector2(
                random.randint(0, (self.screen.get_width() - size.x) // self.cell_size) * self.cell_size,
                random.randint(0, (self.screen.get_height() - size.y) // self.cell_size) * self.cell_size
            )

            self.map.append(pygame.Rect(position.x, position.y, size.x, size.y))

    def draw_obstacle_course(self):
        # Clear the surface by filling it with white
        self.map_surface.fill(self.WHITE)

        # Draw each obstacle onto the surface
        for obstacle in self.map:
            pygame.draw.rect(self.map_surface, self.BLACK, obstacle)

    def create_maze(self, width, height):
        # Initialize the maze with walls (1)
        self.map = [[1 for _ in range(width)] for _ in range(height)]

        # Random starting point
        start_x = random.randrange(0, width, 2)
        start_y = random.randrange(0, height, 2)
        self.map[start_y][start_x] = 0

        # Start carving paths
        self.carve_path(start_x, start_y, width, height)

    def carve_path(self, x, y, width, height):
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height and self.map[new_y][new_x] == 1:
                self.map[new_y][new_x] = 0
                self.map[new_y - dy // 2][new_x - dx // 2] = 0
                self.carve_path(new_x, new_y, width, height)

    def draw_maze(self):
        self.map_surface.fill(self.BLACK)
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                color = self.WHITE if self.map[y][x] == 0 else self.BLACK
                pygame.draw.rect(self.map_surface, color, [x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size])

    
    def initial_position(self):
        open_spaces = [pygame.math.Vector2(x, y) for y, row in enumerate(self.map) for x, cell in enumerate(row) if cell == 0]
        if not open_spaces:
            return  # No open spaces to draw the circle

        self.robot_position = random.choice(open_spaces)
        center = (self.robot_position + pygame.Vector2(0.5,0.5)) * self.cell_size
        radius = self.cell_size // 2.5

        return center, radius

    def draw_robot(self,center,radius):
         # Draw the Robot as a circle with a rectangle to indicate direction
        # Draw the red circle
        pygame.draw.circle(self.map_surface, self.RED, center, radius)

        # Draw the rectangle
        # Draw a line to indicate the front of the robot
        front_pos = center + pygame.Vector2(radius, 0).rotate(0)
        pygame.draw.line(self.map_surface, self.BLACK, center, front_pos)
    
    def update_robot_position(self, direction, width, height):
        new_pos = self.robot_position + direction
        # Check if the new position is within the maze and not a wall
        if 0 <= new_pos.x < width and 0 <= new_pos.y < height:
            if self.map[int(new_pos.y)][int(new_pos.x)] == 0:
                self.robot_position = new_pos
    
    def get_robot_position(self):
        return self.robot_position

    def set_robot_position(self, position):
        self.robot_position = position

    def is_open_space(self, position):
        if 0 <= position.x < self.columns and 0 <= position.y < self.rows:
            return self.map[int(position.y)][int(position.x)] == 0
        return False

    # def run(self, width, height):
    #     # self.create_maze(width, height)
    #     self.create_obstacle_course(width)
    #     [center, radius] = self.initial_position()

    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()

    #         self.screen.fill(self.WHITE)

    #         # self.draw_maze()
    #         self.draw_obstacle_course()
    #         self.draw_robot(center,radius)
    #         self.screen.blit(self.map_surface, (0, 0))
    #         pygame.display.flip()