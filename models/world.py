from models.borot import Borot
import random


# Creates the map
class World:
    def __init__(self, dimensions: tuple[int, int]) -> None:
        # Initialize screen
        self.cell_size: int = 30
        self.rows: int = dimensions[0]
        self.columns: int = dimensions[1]
        self.height: int = self.rows * self.cell_size
        self.width: int = self.columns * self.cell_size
        self.radius = 0

        self.borot: Borot = Borot("Borot", self)

        self.obstacles: list = []

    def generate_obstacle_course(self) -> None:
        for _ in range(self.columns):
            size = (random.randint(1, 5) * self.cell_size, random.randint(1, 3) * self.cell_size)
            position = (
                random.randint(0, (self.width - size[0]) // self.cell_size) * self.cell_size,
                random.randint(0, (self.height - size[1]) // self.cell_size) * self.cell_size
            )

            self.obstacles.append((position[0], position[1], size[0], size[1]))

    def generate_maze(self):
        # Initialize the maze with walls (1)
        self.obstacles = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Random starting point
        start_x = random.randrange(0, self.width, 2)
        start_y = random.randrange(0, self.height, 2)
        self.obstacles[start_y][start_x] = 0

        # Start carving paths
        self.carve_path(start_x, start_y, self.columns, self.rows)

    def carve_path(self, x: int, y: int, width: int, height: int) -> None:
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height and self.obstacles[new_y][new_x] == 1:
                self.obstacles[new_y][new_x] = 0
                self.obstacles[new_y - dy // 2][new_x - dx // 2] = 0
                self.carve_path(new_x, new_y, width, height)

    def initial_position(self):
        open_spaces = []

        for y in range(self.rows):
            for x in range(self.columns):
                if (x, y) not in self.obstacles:
                    open_spaces.append((x, y))

        if not open_spaces:
            return 0, 0

        chosen = random.choice(open_spaces)
        self.borot.position = chosen
        self.radius = self.cell_size // 2.5
        self.l = self.radius * 2

    def build(self):
        # self.generate_maze()
        self.generate_obstacle_course()
        self.initial_position()

