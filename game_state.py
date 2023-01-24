from pygame import draw


class GameState:
    def __init__(self, game):
        self.score = 0
        self.game_over = False
        self.game = game

    def restart(self):
        self.score = 0
        self.game_over = False
        self.zombie_spawner.restart()

    def game_over(self):
        self.game_over = True
        self.zombie_spawner.freeze()

    def score_up(self, points=1):
        self.score += points