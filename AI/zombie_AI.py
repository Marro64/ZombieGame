from pygame import draw
from AI.search import Search
import math
import numpy
import pygame


class ZombieAI:
    def __init__(self, position, target, field, host):
        self.position = numpy.array([float(position[0]), float(position[1])])
        self.direction = numpy.array([0, 0])
        self.rotation = 0
        self.velocity = 0
        self.target = target
        self.search = Search(field)
        self.path = self.search.pathfind(position, target)
        self.path_progress = -1
        self.current_node = None
        self.current_node_pos = None
        self.movement_speed = None
        self.increment_path_progress()
        self.is_finished = False

        self.host = host

    def update_heading(self, dt=1):
        self.position = self.host.get_position_2d()

        if math.dist(self.position, self.current_node_pos) < 10:
            self.increment_path_progress()

        direction_vector = numpy.subtract(self.current_node_pos, self.position)
        direction_vector = direction_vector/numpy.linalg.norm(direction_vector)
        self.direction = direction_vector

        return self.direction

    def increment_path_progress(self):
        self.path_progress += 1
        if self.path_progress >= len(self.path):
            self.goal_reached()
        self.current_node = self.path[self.path_progress]
        self.current_node_pos = numpy.array([self.current_node[0], self.current_node[1]])
        # self.movement_speed = .2/(5*(abs(self.current_node[2] - self.path[self.path_progress-1][2])+.2))
        self.movement_speed = .5

    def goal_reached(self):
        self.path_progress = len(self.path) - 1
        self.is_finished = True

    def get_direction(self):
        return self.direction

    def finished(self):
        return self.is_finished
