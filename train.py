
import logging
from tqdm import tqdm
from models.controller import Controller
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def select_action(motor_output):
    #assert len(motor_output) == 7, "Motor output should have 7 values corresponding to actions."
    
    exp_values = np.exp(motor_output - np.max(motor_output))
    probabilities = exp_values / np.sum(exp_values)
    
    logging.info(f'Motor Output: {motor_output}')
    logging.info(f'Probabilities: {probabilities}')
    
    action = np.random.choice(range(7), p=probabilities)
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

    population_size = 10
    selection_percentage = 0.5
    error_range = 0.1
    mutate_percentage = 0.4
    time_steps = 100
    generations = 10

    controller = Controller(population_size, selection_percentage, error_range, mutate_percentage, time_steps)

    for individual in controller.population:
        test_network_output_range(individual)

    for generation in tqdm(range(generations)):
        controller.generate_new_population()
        logging.info(f'Generation: {generation}')

    logging.info('Finished Training...')

if __name__ == '__main__':
    train()
