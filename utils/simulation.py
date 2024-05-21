import pygame
import numpy as np
import math
import time

from models.state import State
from utils import god
from utils.picasso import Picasso
from models.controller import Controller

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
OBSTACLE_SIZE = (40, 40)
N_OBSTACLES = 45
WALL_THICKNESS = 15
evaluate_fitness = Controller.evaluation

class Robot(object):

    def __init__(self, weights, epoch, robot_i):
        self.results = self.run(weights, epoch, robot_i)


    def run():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(
            "Left velocity: 'w' for +, 's' for -. Right velocity: 'o' for +, 'k' for -. Space for stop")
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        world = god.build(SCREEN_WIDTH, SCREEN_HEIGHT, N_OBSTACLES, OBSTACLE_SIZE, WALL_THICKNESS, True)
        world.find_landmarks()
        font = pygame.font.SysFont('Comic Sans MS', 10)
        picasso = Picasso(surface, font)

        picasso.draw(world)

        current_state = State(0, world)

        clock = pygame.time.Clock()
        dt = 0

        # simulation loop
        start_time = time.time()
        while time.time() - start_time < 15: #set time experiment

            current_state = god.listening(current_state, dt)

            screen.blit(picasso.canvas(), (0, 0))
            picasso.draw(world)
            picasso.robot_data(current_state.borot())
            picasso.robot(current_state.borot())
            pygame.display.flip()

            dt = clock.tick(60) / 500  # Limit to 60 FPS

            
            # score = evaluate_fitness(
            #         player_robot, environment.dustCheck(dustImg))
            # if player_robot.vl == -player_robot.vr or player_robot.vr == -player_robot.vl:
            #     print('Closed because of instability')
            #     return score
            # elif player_robot.vl == 0 or player_robot.vl == -0 and player_robot.vr == 0 or player_robot.vr == -0:
            #     print("Closed because of 0 velocity")
            #     return score
            # if player_robot.wallCollisions > 0:
            #     print('Closed because of collision')
            #     return score
        
        #return score
        # exit the game
        pygame.quit()
