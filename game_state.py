import pygame


class GameState:
    def __init__(self, game):
        self.score = 0
        self.game_over = False
        self.game = game

    def draw(self, surface):
        font = pygame.font.SysFont(None, 24)
        img = font.render(f'Score: {self.score}', True, (0, 0, 255))
        surface.blit(img, (20, 20))

        if self.game_over:
            font = pygame.font.SysFont(None, 72)
            img = font.render(f'Game Over', True, (255, 0, 0))
            # pos = (img.)




    def restart(self):
        self.score = 0
        self.game_over = False
        self.game.restart()

    def end_game(self):
        self.game_over = True
        self.game.freeze()

    def score_up(self, points=1):
        self.score += points

    def click(self):
        if self.game_over:
            self.game.restart()