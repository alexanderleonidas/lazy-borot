import pygame
import numpy as np
import math
import matplotlib.pyplot as plt
import random

def distance(x,y):
    x = np.array(x)
    y = np.array(y)
    return np.linalg.norm(x-y)

class Robot:
    
    def __init__(self,startpos,width):
        
        self.m2p = 3779.52 # meters to pixles
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.heading = 0
        self.vl = 0.01*self.m2p #meters per second
        self.vr = 0.01*self.m2p
        self.maxspeed = 0.02*self.m2p
        self.minspeed = 0.01*self.m2p
        self.mi_obj_dist = 100
        self.count_down = 5 # seconds

    def avoid_obstacles(self, point_cloud, dt):
        closest_obj = None
        dist = np.inf

        if (len(point_cloud) > 1):
            for point in point_cloud:
                if dist > distance([self.x, self.y], point):
                    dist = distance([self.x, self.y], point)
                    closest_obj = (point,dist)
            
            if (closest_obj[1] < self.mi_obj_dist and self.count_down > 0):
                self.count_down -= dt
                self.move_backward()
            else:
                self.count_down = 5 # reset countdown 
                self.move_forward()
    
    def move_backward(self):
        self.vr = self.minspeed
        self.vl = self.minspeed/2
    
    def move_forward(self):
        self.vr = self.minspeed
        self.vl = self.minspeed
    
    def kinematics(self, dt):
        self.x += ((self.vl+self.vr)/2) * math.cos(self.heading) * dt
        self.y -= ((self.vl+self.vr)/2) * math.cos(self.heading) * dt
        self.heading += (self.vr - self.vl) / self.w * dt

        if (self.heading>2*math.pi or self.heading<-2*math.pi):
            self.heading = 0
        
        self.vr = max(min(self.maxspeed, self.vr), self.minspeed)
        self.vl = max(min(self.maxspeed, self.vl), self.minspeed)

class Graphics:
    def __init__(self, dimentions, map):
        pygame.init()

        # Colours
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.yellow = (255,255,0)

        # Map
        self.robot = pygame.image.load("robot.png")
        self.map = pygame.image.load("map.png")

        # Dimensions
        self.height, self.width = dimentions

        # Window settings
        pygame.display.set_caption("Obstacle Avoidance")
        self.map = pygame.display.set_mode((self.width,self.height))
        self.map.blit(self.map, (0,0))


    def generate_map(width, height):
        # Initialize the maze grid, 0 = empty space, 1 = wall
        maze = np.ones((height, width))

        # Stack for holding the cells to visit
        stack = []

        # Start with a random cell
        start_cell = (random.randint(1, height - 2), random.randint(1, width - 2))
        maze[start_cell] = 0
        stack.append(start_cell)

        # Directions to move: up, right, down, left
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]

        while stack:
            current_cell = stack[-1]
            x, y = current_cell

            # Check possible directions
            possible_directions = []
            for dx, dy in directions:
                if 1 <= x + dx < width - 1 and 1 <= y + dy < height - 1 and maze[y + dy, x + dx] == 1:
                    possible_directions.append((dx, dy))

            if possible_directions:
                dx, dy = random.choice(possible_directions)
                maze[y + dy // 2, x + dx // 2] = 0  # Remove wall between current cell and new cell
                maze[y + dy, x + dx] = 0  # Mark new cell as part of the maze
                stack.append((x + dx, y + dy))  # Add new cell to stack
            else:
                stack.pop()  # Backtrack if no directions are possible

        plt.figure(figsize=(10, 10))
        plt.imshow(maze, cmap='binary')
        plt.xticks([]), plt.yticks([])  # Remove axes
        plt.show()
        plt.savefig("map.png")
    
    def generate_robot(radius):
        # Define the circle's parameters
        circle = plt.Circle((0, 0), radius, color='red', fill=True)

        # Create a figure and a single subplot
        fig, ax = plt.subplots()

        # Add the circle to the subplot
        ax.add_artist(circle)

        # Draw the radius line from the origin to a point on the circle
        # Since it's a circle, we can choose any angle for the point on the circumference.
        # Here, we choose 0 degrees for simplicity, which means the point is (radius, 0).
        ax.plot([0, radius], [0, 0], 'r-')  # 'r-' indicates a red line

        # Set the aspect of the plot to be equal, so the circle isn't skewed
        ax.set_aspect('equal')

        # Set limits to ensure the circle and radius line are properly visible
        ax.set_xlim(-radius * 1.1, radius * 1.1)
        ax.set_ylim(-radius * 1.1, radius * 1.1)

        # Show the plot
        plt.show()
        plt.savefig("robot.png")