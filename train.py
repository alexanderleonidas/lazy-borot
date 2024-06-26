import math
from datetime import datetime
import logging
import os
import time

from matplotlib import pyplot as plt
from tqdm import tqdm
from models.controller import Controller
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.INFO)
logging.disable(logging.INFO)


def select_action(motor_output):
    #assert len(motor_output) == 7, "Motor output should have 7 values corresponding to actions."

    exp_values = np.exp(motor_output - np.max(motor_output))
    probabilities = exp_values / np.sum(exp_values)

    logging.info(f'Motor Output: {motor_output}')
    logging.info(f'Probabilities: {probabilities}')

    action = np.random.choice(range(6), p=probabilities)
    return action


def test_network_output_range(individual):
    action_count = {action: 0 for action in range(7)}
    for _ in range(100):
        inputs = np.random.uniform(low=0, high=100, size=16)
        motor_output, hidden_layer_output = individual.NN.runNN(inputs)
        action = select_action(motor_output)
        action_count[action] += 1
        logging.info(f'Test Inputs: {inputs}')
        logging.info(f'Motor Outputs: {motor_output}')
        logging.info(f'Selected Action: {action}')
    logging.info(f'Action distribution: {action_count}')


def train():
    logging.info('Start Training...')

    population_size = 12
    selection_percentage = 0.5
    error_range = 0.1
    mutate_percentage = 0.2
    time_steps = 100
    generations = 10
    map = "Corner"

    controller = Controller(population_size, selection_percentage, error_range, mutate_percentage, time_steps)

    for individual in controller.population:
        test_network_output_range(individual)

    avg_fitness_over_generations = []
    best_fitness_over_generations = []

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    experiment_name = f"{map}_gen_{generations}_steps_{time_steps}_pop_{population_size}_mut_{mutate_percentage}_sel_{selection_percentage}_error_{error_range}"
    save_dir = os.path.join(os.getcwd(), f'results/{experiment_name}_{timestamp}')
    os.makedirs(save_dir, exist_ok=True)

    save_every = 1

    for generation in tqdm(range(generations), desc="Epoch", leave=True):

        for robot_id, individual in enumerate(controller.population):
            individual.update_score(controller.compute_fitness(individual, generation, robot_id))
        controller.generate_new_population(generation, robot_id)
        logging.info(f'Generation: {generation}')

        avg_fitness = np.mean([ind.score for ind in controller.population])
        best_fitness = np.max([ind.score for ind in controller.population])
        avg_fitness_over_generations.append(avg_fitness)
        best_fitness_over_generations.append(best_fitness)
        logging.info(f'Generation: {generation}, Avg Fitness: {avg_fitness}, Best Fitness: {best_fitness}')

        if generations % save_every == 0:
            file_name = f"generation_{generation}"
            save_plots(avg_fitness_over_generations, best_fitness_over_generations, list(range(generation+1)), save_dir,
                       file_name)

    file_name = f"final_result"
    save_plots(avg_fitness_over_generations, best_fitness_over_generations, list(range(generations)), save_dir,
               file_name)

    logging.info('Finished Training...')


def save_plots(avg_fitness, best_fitness, generations, save_dir, file_name):
    plt.figure()
    plt.plot(generations, avg_fitness, label='Average Fitness')
    plt.plot(generations, best_fitness, label='Best Fitness')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.title('Fitness Over Generations')
    plt.savefig(os.path.join(save_dir, f'{file_name}.png'))
    plt.close()


if __name__ == '__main__':
    train()
