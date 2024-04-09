import pygame

from utils.picasso import draw_robot, draw_maze

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def move(temp_keys: pygame.key.ScancodeWrapper, local_pos: pygame.Vector2, delta: float | int) -> pygame.Vector2:
    if temp_keys[pygame.K_w]:
        local_pos.y -= 300 * delta
    if temp_keys[pygame.K_s]:
        local_pos.y += 300 * delta
    if temp_keys[pygame.K_a]:
        local_pos.x -= 300 * delta
    if temp_keys[pygame.K_d]:
        local_pos.x += 300 * delta
    return local_pos


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Draw the maze with walls around the screen
    # TODO: Visualize World instead of manually drawing walls
    walls = [
        ((0, 0), (1280, 0)),
        ((1280, 0), (1280, 720)),
        ((1280, 720), (0, 720)),
        ((0, 720), (0, 0)),
    ]
    draw_maze(walls, screen)

    # Draw the robot
    draw_robot(player_pos, 0, 20, screen)

    # Move the player
    # Note: This is temporary, we will replace this with the robot's movement
    player_pos = move(keys, player_pos, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
