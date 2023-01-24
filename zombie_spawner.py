from zombie import Zombie
from random import randint


class ZombieSpawner:
    def __init__(self, game, size, target, maze):
        self.size = size
        self.target = target
        self.maze = maze
        self.zombies = []
        self.game = game
        self.time_to_next_zombie = 1

    def update(self, dt):
        self.time_to_next_zombie -= dt
        if self.time_to_next_zombie <= 0:
            self.spawn_zombie(self.size, self.target, self.maze)
            self.time_to_next_zombie = randint(1000, 4000)

        for zombie in list(self.zombies):
            zombie.update(dt)

            if zombie.is_finished:
                self.zombies.remove(zombie)

    def draw(self, surface):
        for zombie in self.zombies:
            zombie.draw(surface)

    def shoot(self, position):
        for zombie in list(self.zombies):
            if zombie.hit_check(position):
                self.zombies.remove(zombie)

    def spawn_zombie(self, size, target, maze):
        x = randint(0, size[0]-1)
        y = randint(0, size[1]-1)

        self.zombies.append(Zombie((x, y), target, maze))

    def restart(self):
        self.zombies = []
        self.time_to_next_zombie = 1000

