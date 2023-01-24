from math import sqrt, pow
from pygame import draw
from AI.heightmap import heightMap


class GridElement:
    """
    GridElement used as a tile in the exercise
    """

    """
    Initialise the GridElement and assign the starting values
    """

    def __init__(self, x, y, size):
        self.heightmap = heightMap()

        self.position = (x, y)
        self.neighbours = []
        self.neighbour_data = []
        self.size = (size[0], size[1])
        self.g_score = None
        self.height = self.heightmap.get_height_at(x, y)
        self.color = self.height_to_color(self.height)

    """
    Overload the equals operator
    """

    def __eq__(self, other):
        return self.position == other.position

    """
       Overload the hash operator
    """
    def __hash__(self):
        return hash(self.position)
    """
    Overload the string representation of the object
    """

    def __repr__(self):
        return str(self.position)

    """
    Remove all neighbours
    """

    def reset_neighbours(self):
        self.neighbours = []

    """
    Sets the state of the GridElement 
    """

    def cache_g_score(self, target):
        self.g_score = self.calc_g_score(target)

    def get_neighbours(self):
        return self.neighbours[:]

    def get_neighbour_data(self):
        return self.neighbour_data[:]

    """
     Method to calculate the Manhattan distance from a certain 
     GridElement to another GridElement of the exercise
     """

    def manhattan_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return x_distance + y_distance

    def euclidean_distance(self, other):
        return sqrt(
            pow(self.position[0]+other.position[0], 2) +
            pow(self.position[1]+other.position[1], 2),
        )

    def mixed_distance(self, other):
        dx = abs(other.position[0] - self.position[0])
        dy = abs(other.position[1] - self.position[1])
        diagonal_distance = min(dx, dy)
        dx -= diagonal_distance
        dy -= diagonal_distance
        return sqrt(2)*diagonal_distance + dx + dy

    def null_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return max(x_distance, y_distance)

    def direction(self, other):
        return other.position[0] - self.position[0], other.position[1] - self.position[1]

    def get_position(self):
        return self.position

    def get_g_score(self):
        return self.g_score

    """
    Assign the GridElement used to reach this GridElement
    """

    def set_color(self, color):
        self.color = color

    @staticmethod
    def height_to_color(height):
        if height < 0:
            height = 0
        elif height > 1:
            height = 1

        return 255 * (1 - height), 255 * (1 - height), 255 * (1 - height)

    def get_height_difference(self, other):
        return pow(abs((other.height - self.height)*7), 2)

    def get_cost_to(self, other, distance):
        return distance + self.get_height_difference(other)

    def calc_g_score(self, target):
        return self.mixed_distance(target) + self.get_height_difference(target)

    """
    Draw the GridElement
    """

    def draw_grid_element(self, surface):
        draw.rect(surface, self.color,
                  (self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1]), 0)

        # discard the directions where neighbours are
        compass = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # The four directions
        for neighbour in self.neighbours:
            if self.direction(neighbour) in compass:
                compass.remove(self.direction(neighbour))

        for direction in compass:
            if direction == (0, -1):  # North
                draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]), 2)
            if direction == (1, 0):  # East
                draw.line(surface, (0, 0, 0), ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
            if direction == (0, 1):  # South
                draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
            if direction == (-1, 0):  # West
                draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]), 2)

    def print_walls(self):
        # discard the directions where neighbours are
        compass = {(0, -1): "North",
                   (1, 0): "East",
                   (0, 1): "South",
                   (-1, 0): "West"}  # The four directions
        for neighbor in self.neighbours:
            compass.pop(self.direction(neighbor))

        print(list(compass.values()))
        return None
