import pygame

from models.state import State
from utils import god
from utils.picasso import Picasso

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
OBSTACLE_SIZE = (40, 40)
N_OBSTACLES = 45
WALL_THICKNESS = 15


def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(
        "Left velocity: 'w' for +, 's' for -. Right velocity: 'o' for +, 'k' for -. Space for stop")
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    world = god.build(SCREEN_WIDTH, SCREEN_HEIGHT, N_OBSTACLES, OBSTACLE_SIZE, WALL_THICKNESS)
    font = pygame.font.SysFont('Comic Sans MS', 10)
    picasso = Picasso(surface, font)

    picasso.draw(world)

    current_state = State(0, world)

    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:
        current_state = god.listening(current_state, dt)

        screen.blit(picasso.canvas(), (0, 0))
        picasso.draw(world)
        picasso.robot_data(current_state.borot())
        picasso.robot(current_state.borot())
        pygame.display.flip()

        dt = clock.tick(50) / 1000  # Limit to 60 FPS

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
