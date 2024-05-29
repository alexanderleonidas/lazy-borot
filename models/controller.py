import numpy as np
import random
import pygame
import torch
from models.brain import Brain
from models.state import State
from models.world import World
from models.action import Action
from utils import god
from utils.picasso import Picasso
import logging

SCREEN_SIZE = 400
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE, SCREEN_SIZE
OBSTACLE_SIZE = (40, 40)
N_OBSTACLES = 45
WALL_THICKNESS = 15


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_diverse_inputs(num_samples, input_size):
    return [np.random.uniform(low=0, high=100, size=input_size) for _ in range(num_samples)]

class Controller:
    def __init__(self, pop_size, select_perc, error_range, mutate, time_steps) -> None:
        self.population = [Individual(Brain()) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
        self.mutate = mutate
        self.world_size = SCREEN_SIZE
        self.time_steps = time_steps
        self.immigration_rate = 0.1  # Percentage of new random individuals each generation

    def evaluation(self):
        for idx, individual in enumerate(self.population):
            individual.update_score(self.compute_fitness(individual, idx))

    def compute_fitness(self, individual, idx):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Individual: {idx} and Score: {individual.score}")
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        world = god.build(SCREEN_WIDTH, SCREEN_HEIGHT, N_OBSTACLES, OBSTACLE_SIZE, WALL_THICKNESS, 2)
        world.find_landmarks()
        font = pygame.font.SysFont('Comic Sans MS', 10)
        picasso = Picasso(surface, font)
        picasso.draw(world)

        # Ensure dust is tracked
        dust_particles = world.dust()  # Assuming `world.dust()` provides the dust particles
        picasso.draw_dust(dust_particles)

        state = State(0, world)
        state.next(Action.NOTHING, 1E-3)
        clock = pygame.time.Clock()
        dt = 0
        total_reward = 0

        for _ in range(self.time_steps):
            sensor_inputs = self.get_inputs(state)
            motor_output, hidden_layer_output = individual.NN.runNN(sensor_inputs)
            action_index = self.get_valid_action_index(motor_output)
            action = list(Action)[action_index]
            dt += .1
            state = state.next(action, dt)
            reward = self.get_reward(state, world, picasso)
            total_reward += reward

            screen.blit(picasso.canvas(), (0, 0))
            picasso.draw(world)
            picasso.robot_data(state.borot())
            picasso.robot(state.borot())
            pygame.display.flip()
            dt = clock.tick(60) / 500

        pygame.quit()
        return total_reward

    def get_valid_action_index(self, motor_output):
        # Ensure the motor_output is a numpy array
        motor_output = np.array(motor_output)
        
        # Ensure motor_output size matches action space size (7 in this case)
        if len(motor_output) != len(Action):
            motor_output = np.resize(motor_output, len(Action))
        
        # Use softmax to convert motor outputs to probabilities
        exp_values = np.exp(motor_output - np.max(motor_output))
        probabilities = exp_values / np.sum(exp_values)
        
        # Randomly select action based on these probabilities
        action_index = np.random.choice(range(len(Action)), p=probabilities)
        return action_index

    def get_reward(self, state, world, picasso):
        borot = state.borot()
        removed_dust = picasso.remove_dust(borot)  # Count of removed dust particles
        reward = removed_dust * 10  # Reward for removing dust

        velocity = borot.speed()
        left_wheel_speed, right_wheel_speed = velocity
        penalty = -1 if left_wheel_speed == 0 and right_wheel_speed == 0 else 0
        unbalance_penalty = -0.1 * abs(left_wheel_speed - right_wheel_speed)

        return reward + penalty + unbalance_penalty


    def get_inputs(self, state):
        borot = state.borot()
        sensors = borot.sensors()
        velocity = borot.speed()
        theta = borot.theta()
        inputs = [sensor[2] / 100.0 for sensor in borot.get_obstacle_sensors()]  # Normalize sensor readings
        inputs.extend([v / 40.0 for v in velocity])  # Normalize velocity
        inputs.append(theta / np.pi)  # Normalize theta
        inputs.append(1)  # bias
        return inputs

    def selection(self):
        self.population.sort(key=lambda s: s.score, reverse=True)
        selected = self.population[:int(self.select_perc * len(self.population))]
        
        # Ensure at least one individual has non-zero velocities
        if all(ind.score < -90 for ind in selected):  # assuming -100 is the score for zero velocities
            logging.warning('All selected individuals have zero velocities, reconsidering selection...')
            selected = self.population[:2]  # select top 2 regardless of score to maintain diversity
        
        return selected

    def tournament_selection(self, k=3):
        selected = []
        for _ in range(self.pop_size):
            participants = random.sample(self.population, k)
            winner = max(participants, key=lambda ind: ind.score)
            selected.append(winner)
        return selected

    def reproduction(self, parent_1, parent_2):
        child_weights = []
        for w1, w2 in zip(parent_1.dna, parent_2.dna):
            new_weight = (w1 + w2) / 2
            child_weights.append(new_weight)
        child = Individual(Brain(child_weights))
        return child

    def random_crossover(self, selected):
        children = []
        for _ in range(self.pop_size):
            parent_1, parent_2 = random.sample(selected, 2)
            child_weights = []
            for w1, w2 in zip(parent_1.dna, parent_2.dna):
                mask = np.random.rand(*w1.shape) < 0.5
                new_weight = np.where(mask, w1, w2)
                child_weights.append(new_weight)
            child = Individual(Brain(child_weights))
            children.append(child)
        return children

    def mutation(self, children):
        for child in children:
            if random.random() < self.mutate:
                for weight in child.dna:
                    noise = np.random.uniform(-1, 1, size=weight.shape) * self.error_range
                    weight += noise
        return children

    def introduce_immigrants(self, population):
        num_immigrants = int(self.pop_size * self.immigration_rate)
        immigrants = [Individual(Brain()) for _ in range(num_immigrants)]
        return population + immigrants

    def generate_new_population(self):
        # Life cycle
        self.evaluation()
        selected = self.tournament_selection()
        children = self.random_crossover(selected)
        children = self.mutation(children)
        children = self.introduce_immigrants(children)
        # Preserve best individuals
        children[:2] = selected[:2]
        self.population = children
        return self.population

class Individual:
    def __init__(self, NN):
        self.NN = NN
        self.dna = NN.weights
        self.score = 0

    def update_score(self, score):
        self.score = score

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Robot score: {self.score}'
