import random
from grid_element import GridElement
from math import sqrt


class Maze:
    """
        Generates a grid based maze based on GridElements
        This class also contains search algorithms for
        depth first, breath first, greedy and A* star search to
        solve the generated mazes
        """

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.grid_size = (grid_size_x, grid_size_y)
        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []
        for x in range(grid_size_x):
            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        # self.reset_all()
        random.seed(0)

    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                                                                                                                                            element.draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        neighbour_cost = []
        if cell.position[0] > 0:  # North
            neighbour = self.grid[cell.position[0] - 1][cell.position[1]]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, 1)))
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbour = self.grid[cell.position[0] + 1][cell.position[1]]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, 1)))
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbour = self.grid[cell.position[0]][cell.position[1] + 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, 1)))
        if cell.position[1] > 0:  # West
            neighbour = self.grid[cell.position[0]][cell.position[1] - 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, 1)))

        if cell.position[0] > 0 and cell.position[1] < self.grid_size[1] - 1:
            neighbour = self.grid[cell.position[0] - 1][cell.position[1] + 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, sqrt(2))))
        if cell.position[0] < self.grid_size[0] - 1 and cell.position[1] < self.grid_size[1] - 1:  # East
            neighbour = self.grid[cell.position[0] + 1][cell.position[1] + 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, sqrt(2))))
        if cell.position[0] > 0 and cell.position[1] > 0:  # South
            neighbour = self.grid[cell.position[0] - 1][cell.position[1] - 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, sqrt(2))))
        if cell.position[0] < self.grid_size[0] - 1 and cell.position[1] > 0:  # West
            neighbour = self.grid[cell.position[0] + 1][cell.position[1] - 1]
            neighbours.append((neighbour, cell.get_cost_to(neighbour, sqrt(2))))

        return neighbours

    def generate_open_maze(self):
        # self.reset_all()
        for col in self.grid:
            for cell in col:
                neighbour_data = self.possible_neighbours(cell)
                cell.neighbour_data = neighbour_data
                for data in neighbour_data:
                    cell.neighbours.append(data[0])
