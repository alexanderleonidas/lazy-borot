class Borot:
    def __init__(self, name, world):
        self.name = name
        self.position = None
        self.world = world
        pass

    def say_hello(self):
        return f"Hello, I am {self.name}!"

    def move(self, direction):
        new_pos = self.position + direction
        # Check if the new position is within the maze and not a wall
        if 0 <= new_pos.x < self.world.width and 0 <= new_pos.y < self.world.height:
            if self.world.obstacles[int(new_pos.y)][int(new_pos.x)] == 0:
                self.position = new_pos

    def get_position(self):
        return self.position
