from typing import Tuple

BOROT_SIZE = 10

class Borot:
    def __init__(self, name, world) -> None:
        self.name = name
        self.position: Tuple[int, int] = (0, 0)
        self.radius = BOROT_SIZE
        self.world = world
        self.velocity: Tuple[float, float] = (0, 0)  # Left and Right Wheel
        self.rotation = 0
        self.icc: Tuple[float, float] = (0, 0)  # Instantaneous Center of Curvature

    def move(self, direction) -> Tuple[int, int]:
        new_pos = self.position + direction
        # Check if the new position is within the maze and not a wall
        if 0 <= new_pos.x < self.world.width and 0 <= new_pos.y < self.world.height:
            if self.world.obstacles[int(new_pos.y)][int(new_pos.x)] == 0:
                self.position = new_pos

        return self.get_position()

    def get_position(self) -> Tuple[int, int]:
        return self.position
