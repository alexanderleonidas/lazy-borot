import pygame
from pygame import Surface, Vector2


def draw_background(screen: Surface) -> None:
    screen.fill("gray100")


def draw_wall(vector1: tuple, vector2: tuple, width: int, screen: Surface) -> None:
    pygame.draw.line(screen, "gray13", vector1, vector2, width)
    return


def draw_robot(pos: tuple | Vector2, angle: int, radius: int, screen: Surface) -> None:
    # Draw the Robot as a circle with a rectangle to indicate direction
    # Draw the red circle
    pygame.draw.circle(screen, "red", pos, radius)

    # Draw the rectangle
    # Draw a line to indicate the front of the robot
    front_pos = pos + pygame.Vector2(radius, 0).rotate(angle)
    pygame.draw.line(screen, "black", pos, front_pos)
    return


def draw_maze(walls: list, screen: Surface) -> None:
    draw_background(screen)

    for wall in walls:
        draw_wall(wall[0], wall[1], 50, screen)
    return
