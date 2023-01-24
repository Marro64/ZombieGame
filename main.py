import sys
from AI.helpers.keyboard_handler import KeyboardHandler
from AI.maze import Maze
from AI.helpers.constants import Constants
from AI.search import Search
from zombie_spawner import ZombieSpawner
from hand_tracking.cursor import Cursor as Aim
from game_state import GameState
from ursinaEnvironment import UrsinaEnvironment
from hand_tracking.hitdetection import HitDetection

from ursina import *


class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """
    def __init__(self):
        self.app = Ursina()

        self.size = (200, 200)
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_open_maze()
        self.search = Search(self.maze)
        self.zombie_spawner = ZombieSpawner(self, self.size, (0, 0), self.maze)
        self.cursor = Aim(self)
        self.game_state = GameState(self)
        self.ursina_environment = UrsinaEnvironment(self.size)
        self.hitdetection = HitDetection(self.cursor)

        self.app.run()

    def update(self):
        self.cursor.update()
        self.zombie_spawner.update(time.dt)

    def shoot(self, location):
        if not self.game_state.game_over:
            self.hitdetection.shoot(location)
        else:
            self.game_state.click()

    def game_over(self):
        self.game_state.end_game()

    def restart(self):
        self.zombie_spawner.restart()

    def freeze(self):
        self.zombie_spawner.freeze()

    def add_score(self, score=None):
        self.game_state.score_up(score)


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
