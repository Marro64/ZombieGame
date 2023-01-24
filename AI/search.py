import bisect
from AI.grid_element_path import GridElementPath


class Search:
    def __init__(self, graph):
        self.graph = graph
        self.local_nodes = dict()

    def pathfind(self, start, target):
        self.local_nodes = dict()
        start = (int(start[0] // self.graph.cell_width), int(start[1] // self.graph.cell_height))
        target = (int(target[0] // self.graph.cell_width), int(target[1] // self.graph.cell_height))
        start = self.get_local_node(self.graph.grid[start[0]][start[1]])
        target = self.get_local_node(self.graph.grid[target[0]][target[1]])
        self.get_local_node(start).set_distance(0)

        priority_queue = [start]
        visited = []

        while len(priority_queue) > 0:
            current_node = priority_queue.pop(0)
            if current_node != target:
                if current_node not in visited:
                    visited.append(current_node)
                    neighbours = current_node.global_node.get_neighbour_data()
                    for neighbour in neighbours:
                        next_node = self.get_local_node(neighbour[0])
                        if next_node not in visited:
                            cost = neighbour[1]
                            g_score = next_node.global_node.calc_g_score(target)
                            f_score = current_node.get_distance() + cost
                            score = f_score + g_score
                            if next_node not in priority_queue:
                                next_node.set_parent(current_node, cost)
                                next_node.set_score(score)
                                bisect.insort(priority_queue, next_node)
                            elif score < next_node.get_distance():
                                next_node.set_parent(current_node, cost)
                                next_node.set_score(score)
                                priority_queue.remove(next_node)
                                bisect.insort(priority_queue, next_node)
            else:
                break
        print("The number of visited nodes is: {}".format(len(visited)))
        self.highlight_path(start, target)
        return self.output_path(start, target)

    @staticmethod
    def highlight_path(start, target):
        # Compute the path, back to front.
        current_node = target.parent

        while current_node is not None and current_node != start:
            current_node.set_color((248, 220, 50))
            current_node = current_node.parent

        print("Path length is: {}".format(target.distance))

    @staticmethod
    def output_path(start, target):
        current_node = target.parent
        nodes = []

        while current_node is not None and current_node != start:
            nodes += [current_node]
            current_node = current_node.parent

        length = len(nodes)-1
        path = []
        for i in range(0, length):
            node = nodes[length-i]
            path.append([(node.position[0]*node.size[0]), (node.position[1]*node.size[1]), node.height])

        return path

    def get_local_node(self, global_node):
        global_node_hashed = hash(global_node)
        if global_node_hashed in self.local_nodes:
            return self.local_nodes[global_node_hashed]
        else:
            local_node = GridElementPath(global_node)
            self.local_nodes[hash(global_node)] = local_node
            return local_node

    def draw_path(self, surface):
        for node in self.local_nodes.values():
            node.draw_grid_element(surface)
