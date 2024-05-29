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

SCREEN_SIZE = 400
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE, SCREEN_SIZE
OBSTACLE_SIZE = (40, 40)
N_OBSTACLES = 45
WALL_THICKNESS = 15

class Controller:
    def __init__(self, pop_size, select_perc, error_range, mutate, time_steps) -> None:
        self.population = [Individual(Brain.create()) for _ in range(pop_size)]
        self.pop_size = pop_size
        self.select_perc = select_perc
        self.error_range = error_range
        self.mutate = mutate
        self.world_size = SCREEN_SIZE
        self.time_steps = time_steps
        if torch.backends.mps.is_available():
            self.device = torch.device("mps") 
        else:
            self.device = torch.device("cpu")

    def evaluation(self):
        for idx, individual in enumerate(self.population):
            individual.update_score(self.compute_fitness(individual, idx))

    def compute_fitness(self, individual, idx):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(
            f"Individidual: {idx} and Score: {individual.score} ")
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        world = god.build(SCREEN_WIDTH, SCREEN_HEIGHT, N_OBSTACLES, OBSTACLE_SIZE, WALL_THICKNESS, 2)
        world.find_landmarks()

        font = pygame.font.SysFont('Comic Sans MS', 10)
        picasso = Picasso(surface, font)

        picasso.draw(world)

        state = State(0, world)
        state.next(Action.NOTHING, 1E-3)

        clock = pygame.time.Clock()
        dt = 0

        total_reward = 0
        h = individual.NN.init_hidden(1)

        for _ in range(self.time_steps):
            inputs = self.get_inputs(state)
            inputs = torch.tensor(inputs, dtype=torch.float, device=self.device).unsqueeze(0).unsqueeze(0)  # batch_size=1, seq_len=1
            outputs, h = individual.NN(inputs, h)
            action_index = torch.argmax(outputs).item()
            action = list(Action)[action_index]
            dt += .1
            state = state.next(action, dt)  # assuming dt = 0.1
            reward = self.get_reward(state)
            total_reward += reward

            screen.blit(picasso.canvas(), (0, 0))
            picasso.draw(world)
            picasso.robot_data(state.borot())
            picasso.robot(state.borot())
            pygame.display.flip()

            dt = clock.tick(60) / 500  # Limit to 60 FPS

        pygame.quit()

        return total_reward

    def get_inputs(self, state):
        borot = state.borot()
        sensors = borot.sensors()
        velocity = borot.speed()
        theta = borot.theta()
        inputs = [sensor[2] for sensor in borot.get_obstacle_sensors()]  # distance readings
        inputs.extend(velocity)
        inputs.append(theta)
        inputs.append(1)  # bias
        return inputs

    def get_reward(self, state: State):
        # TODO: Maybe add to funcationality to account for time alive + not constantly spinning in circles + not hitting obstacles
        # Sample reward function based on the distance to the closest landmark
        borot = state.borot()
        landmarks = [lm[2] for lm in borot.get_landmark_sensors()]
        # borot_pos = borot.position()
        dust, cleaned_dust = state.dust(), state.cleaned_dust()

        dust_reward = len(dust)/(cleaned_dust + 1)

        if not landmarks:
             distance_reward = -1 # no landmarks, give negative reward
        else:
            # closest_landmark = min(landmarks, key=lambda lm: np.hypot(lm[0] - borot_pos[0], lm[1] - borot_pos[1]))
            # distance = np.hypot(closest_landmark[0] - borot_pos[0], closest_landmark[1] - borot_pos[1])
            # Invert distance to get a higher reward for closer distances
            distance_reward = 1 / (min(landmarks) + 1)  # Adding 1 to avoid division by zero

        # Combine the rewards
        reward = distance_reward + dust_reward

        return reward

    def selection(self):
        self.population.sort(key=lambda s: s.score, reverse=True)
        selected = self.population[:int(self.select_perc * len(self.population))]
        return selected

    def reproduction(self, parent_1, parent_2):
        child_weights = []
        for w1, w2 in zip(parent_1.dna, parent_2.dna):
            new_weight = (w1 + w2) / 2
            child_weights.append(new_weight)
        child = Individual(Brain.create())
        child.NN.load_state_dict(parent_1.NN.state_dict())
        for param, new_weight in zip(child.NN.parameters(), child_weights):
            param.data.copy_(new_weight)
        return child

    def crossover(self, selected):
        if not selected:
            raise ValueError("Selected list is empty. Cannot perform crossover.")

        children = []
        parent_1 = [selected[rand] for rand in np.random.randint(len(selected), size=self.pop_size)]
        parent_2 = [selected[rand] for rand in np.random.randint(len(selected), size=self.pop_size)]
        for p1, p2 in zip(parent_1, parent_2):
            child = self.reproduction(p1, p2)
            children.append(child)
        return children

    def mutation(self, children):
        for child in children:
            if random.random() < self.mutate:
                for param in child.NN.parameters():
                    noise = torch.randn(param.size()) * self.error_range
                    param.data.add_(noise)
        return children

    def generate_new_population(self):
        # Life cycle
        self.evaluation()
        selected = self.selection()
        children = self.crossover(selected)
        children = self.mutation(children)
        # Preserve best individuals
        children[:2] = selected[:2]
        self.population = children
        return self.population

class Individual:
    def __init__(self, NN):
        self.NN = NN
        self.dna = [param.data.clone() for param in NN.parameters()]
        self.score = 0

    def update_score(self, score):
        self.score = score

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Robot score: {self.score}'
