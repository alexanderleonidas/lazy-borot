from maps.map import Map
from models.world import World


class Maze(Map):
    def __init__(self):
        super().__init__(1000, 1000)
        self.__name = "Maze"
        self.wall_thickness = 25
        self.line_wall_thickness = 10
    
    def build(self) -> World:
        # Draw Walls around the map
        self.world().add_obstacle((self.wall_thickness, 0, self.width() - (2 * self.wall_thickness), self.wall_thickness))  # Top wall
        self.world().add_obstacle((0, 0, self.wall_thickness, self.height()))  # Left wall
        self.world().add_obstacle((self.width() - self.wall_thickness, 0, self.wall_thickness, self.height()))  # Right wall
        self.world().add_obstacle(
            (self.wall_thickness, self.height() - self.wall_thickness, self.width() - (2 * self.wall_thickness), self.wall_thickness))

        self.world().add_obstacle((self.wall_thickness, 150, self.width() - 400, self.line_wall_thickness))
        self.world().add_obstacle((self.wall_thickness + 800, 150, self.width() - 800 - 2 * self.wall_thickness, self.line_wall_thickness))
        self.world().add_obstacle((self.wall_thickness + 400, 325, self.width() - 400 - 2 * self.wall_thickness, self.line_wall_thickness))

        self.world().add_obstacle((self.wall_thickness, 500, self.width() - 400, self.line_wall_thickness))
        self.world().add_obstacle((self.wall_thickness + 400, 650, self.width() - 400 - 2 * self.wall_thickness, self.line_wall_thickness))

        return self.world()