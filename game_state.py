import pygame
from ursina import *

class GameState(Sprite):
    def __init__(self, game):
        super().__init__()
        self.score = 0
        self.game_over = False
        self.game = game

    def update(self):
        # insert UI here
        pass

    def restart(self):
        self.score = 0
        self.game_over = False
        self.game.restart()

    def end_game(self):
        self.game_over = True

    def score_up(self, points=1):
        self.score += points

    def click(self):
        if self.game_over:
            self.game.restart()