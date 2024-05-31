import math
from maps.map import Map
from models.world import World

DUST_RADIUS = 5
DISTANCE = 25
X_MIN = 25
X_MAX = 400
Y_MIN = 25
Y_MAX = 400

class Corner(Map):
    def __init__(self) -> None:
        super().__init__(400, 400)
        self.name = "Corner"
        self.wall_thickness = 10
    
    def build(self) -> World:
        self.world().add_obstacle((self.wall_thickness, 0, self.width() - (2 * self.wall_thickness), self.wall_thickness))  # Top wall
        self.world().add_obstacle((0, 0, self.wall_thickness, self.height()))  # Left wall
        self.world().add_obstacle((self.width() - self.wall_thickness, 0, self.wall_thickness, self.height()))  # Right wall
        self.world().add_obstacle(
            (self.wall_thickness, self.height() - self.wall_thickness, self.width() - (2 * self.wall_thickness), self.wall_thickness))  # Bottom wall

        self.add_middle_box()
        self.dust()
        return self.world()
    
    def add_middle_box(self):
        self.box_size = 250
        # Calculate the position of the box to be centered
        self.box_x = (self.width() - self.box_size) // 2
        self.box_y = (self.height() - self.box_size) // 2
        
        # self.box_size = 200
        # self.center_x = self.width() // 2
        # self.center_y = self.height() // 2
        # self.box_x = self.center_x - self.box_size // 2
        # self.box_y = self.center_y - self.box_size // 2
        self.world().add_obstacle((self.box_x, self.box_y, self.box_size, self.box_size))

    def dust(self) -> World:
        dusts = []

        x_tiles = math.floor((X_MAX - X_MIN) / DISTANCE)
        y_tiles = math.floor((Y_MAX - Y_MIN) / DISTANCE)

        for i in range(x_tiles):
            for j in range(y_tiles):
                dust_x = X_MIN + i * DISTANCE
                dust_y = Y_MIN + j * DISTANCE
                # Ensure dust is not within the middle box and does not touch it
                if not (self.box_x - DUST_RADIUS * 2 < dust_x < self.box_x + self.box_size + DUST_RADIUS * 2 and
                        self.box_y - DUST_RADIUS * 2 < dust_y < self.box_y + self.box_size + DUST_RADIUS * 2):
                    dusts.append((dust_x, dust_y))

        for dust in dusts:
            obj = (dust[0], dust[1], DUST_RADIUS * 2, DUST_RADIUS * 2)
            self.world().add_dust(obj)

        return self.world()