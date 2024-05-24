from maps.map import Map
from models.world import World


class Hallway(Map):
    def __init__(self):
        super().__init__(400, 400)
        self.__name = "Hallway"
        self.wall_thickness = 10

    def build(self) -> World:
        self.world().add_obstacle((self.wall_thickness, 0, self.width() - (2 * self.wall_thickness), self.wall_thickness))  # Top wall
        self.world().add_obstacle((0, 0, self.wall_thickness, self.height()))  # Left wall
        self.world().add_obstacle((self.width() - self.wall_thickness, 0, self.wall_thickness, self.height()))  # Right wall
        self.world().add_obstacle(
            (self.wall_thickness, self.height() - self.wall_thickness, self.width() - (2 * self.wall_thickness), self.wall_thickness))
        return self.world()
