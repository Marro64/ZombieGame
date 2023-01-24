from pygame import draw
from AI.search import Search
import math
import numpy
import pygame


def to_numpy(series):
    return numpy.array(list(series))


class Zombie:
    def __init__(self, position, target, field):
        self.position = numpy.array([float(position[0]), float(position[1])])
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
        self.hitbox = (48, 48)

        self.sprite = pygame.image.load('zombie-topdown.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (32, 32)
                                             )

    def update(self, dt):
        if math.dist(self.position, self.current_node_pos) < 10:
            self.increment_path_progress()

        direction_vector = numpy.subtract(self.current_node_pos, self.position)
        direction_vector = direction_vector/numpy.linalg.norm(direction_vector)
        self.rotation = 180-numpy.degrees(numpy.angle(direction_vector[0] + 1j * direction_vector[1]))
        # print(direction_vector, self.rotation)

        self.velocity = (self.velocity+self.movement_speed)*.02*dt

        self.position += direction_vector * self.velocity

    def draw(self, surface):
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        surface.blit(rotated_sprite, (self.position[0] - rotated_sprite.get_width()/2, self.position[1] - rotated_sprite.get_height()/2))
        draw.rect(surface, (255, 0, 0), (self.position[0], self.position[1], 1, 1), 0)
        pass

    def increment_path_progress(self):
        self.path_progress += 1
        if self.path_progress >= len(self.path):
            self.goal_reached()
        self.current_node = self.path[self.path_progress]
        self.current_node_pos = numpy.array([self.current_node[0], self.current_node[1]])
        self.movement_speed = .5/(5*(abs(self.current_node[2] - self.path[self.path_progress-1][2])+.05))

    def goal_reached(self):
        self.path_progress = len(self.path) - 1
        self.is_finished = True

    def hit_check(self, position):
        left = self.position[0] - self.hitbox[0]/2
        top = self.position[1] - self.hitbox[1]/2
        right = self.position[0] + self.hitbox[0]/2
        bottom = self.position[1] + self.hitbox[1]/2

        if left < position[0] < right and top < position[1] < bottom:
            return True
        else:
            return False
