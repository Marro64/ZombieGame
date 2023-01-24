from AI.maze import Maze
from AI.helpers.constants import Constants
from zombie_spawner import ZombieSpawner
from hand_tracking.cursor import Cursor as Aim
from game_state import GameState
from ursinaEnvironment import UrsinaEnvironment

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
        self.maze.generate_open_maze() # Open maze, which has no walls. Instead, it has a heightmap.
        self.zombie_spawner = ZombieSpawner(self, self.size, (0, 0), self.maze) # Spawns and keeps track of the
        self.cursor = Aim(self) # The finger tracking, renamed to aim to not clash with Ursina's cursor object
        self.game_state = GameState(self) # Keeps track of things like score and when the game ends. Mostly unfinished.
        self.ursina_environment = UrsinaEnvironment(self.size) # Ground and camera setup

        self.app.run()

    # The following are interfaces for different classes to communicate
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
