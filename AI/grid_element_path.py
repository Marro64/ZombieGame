from pygame import draw


class GridElementPath:
    def __init__(self, global_node):
        self.global_node = global_node
        self.color = None
        self.position = None
        self.size = None
        self.height = None
        self.parent = None
        self.distance = None
        self.score = None
        self.reset_state()

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return (self.score is not None) and (other.score is None or self.score < other.score)

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return str(self.position)

    def reset_state(self):
        self.color = self.global_node.color
        self.position = self.global_node.position
        self.size = self.global_node.size
        self.height = self.global_node.height
        self.parent = None
        self.score = None
        self.distance = None

    def set_score(self, score):
        self.score = score

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def get_score(self):
        return self.score

    def get_position(self):
        return self.position

    def set_color(self, color):
        self.color = color

    def set_parent(self, parent, cost):
        self.parent = parent
        if parent.distance is not None:
            self.distance = parent.distance + cost

    def direction(self, other):
        return other.position[0] - self.position[0], other.position[1] - self.position[1]

    def draw_grid_element(self, surface):
        # This draw an arrow to from the parent
        draw.rect(surface, self.color,
                  (self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1]), 0)

        if self.parent is not None:

            vector = self.direction(self.parent)

            center = ((self.position[0] + 0.5) * self.size[0], (self.position[1] + 0.5) * self.size[1])

            if vector[0] != 0:
                left_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5,
                              center[1] + (vector[1] - vector[0]) * self.size[0] / 5)
                right_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5,
                               center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
            else:
                left_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5,
                              center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
                right_point = (center[0] + (vector[0] + vector[1]) * self.size[0] / 5,
                               center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
            draw.polygon(surface, (100, 100, 100), (center, left_point, right_point))
            entry_point = (center[0] + vector[0] * self.size[0] / 2, center[1] + vector[1] * self.size[1] / 2)
            end_point = (center[0] + vector[0] * self.size[0] / 5, center[1] + vector[1] * self.size[1] / 5)
            draw.line(surface, (100, 100, 100), end_point, entry_point, int(self.size[0] / 20) + 1)
