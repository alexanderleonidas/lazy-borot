from tqdm import tqdm

from models.controller import Controller



def train():
    print('Start Training...')

    population_size = 100
    selection_percentage = .1
    error_range = .3
    mutate_percentage = .1
    time_steps = 100
    generations = 100

    controller = Controller(population_size, selection_percentage, error_range, mutate_percentage,
                            time_steps)

    for generation in tqdm(range(generations)):
        controller.generate_new_population()

        if generation % 10 == 0:
            print(f'Generation: {generation}')

    print('Finished Training...')


if __name__ == '__main__':
    train()
