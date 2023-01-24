from ursina import *
from ursinaZombie import UrsinaZombie as Zombie
from random import randint


class ZombieSpawner(Entity):
    def __init__(self, game, size, target, maze):
        super().__init__()
        self.size = size
        self.target = target
        self.maze = maze
        self.zombies = []
        self.game = game
        self.time_to_next_zombie = 1
        self.running = True

    def update(self):
        if self.running:
            self.time_to_next_zombie -= time.dt*1000
            if self.time_to_next_zombie <= 0:
                self.spawn_zombie(self.size, self.target, self.maze)
                self.time_to_next_zombie = randint(1000, 4000)

            to_be_destroyed = []
            for zombie in list(self.zombies):
                if zombie.is_finished():
                    self.zombies.remove(zombie)
                    to_be_destroyed.append(zombie)

            for thing in to_be_destroyed:
                destroy(thing)

    def draw(self, surface):
        for zombie in self.zombies:
            zombie.draw(surface)

    def shoot(self, position):
        pass
        # for zombie in list(self.zombies):
        #     if zombie.hit_check(position):
        #         self.zombies.remove(zombie)
        #         self.game.add_score(1)

    def spawn_zombie(self, size, target, maze):
        x = randint(0, size[0]-1)
        y = randint(0, size[1]-1)

        self.zombies.append(Zombie(target, maze, x=x, y=1000, z=y))

    def restart(self):
        self.zombies = []
        self.time_to_next_zombie = 1000
        self.running = True

    def freeze(self):
        self.running = False
