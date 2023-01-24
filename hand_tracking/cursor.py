from hand_tracking.hand_tracking import HandTracking
from pygame import draw


def map_values(x, a, b, c, d):
    y = (x-a)/(b-a)*(d-c)+c
    return y


class Cursor:
    def __init__(self, game, tracked_point=5):
        self.hands = HandTracking()
        self.hand_pos = None
        self.cursor_pos = (0, 0)
        self.tracked_point = tracked_point
        self.color = (255, 0, 0)
        self.has_shot = False
        self.game = game

    def update(self):
        self.hands.update()

        self.hand_pos = self.hands.get_point(self.tracked_point)
        if self.hand_pos is not None:
            x = map_values(self.hand_pos[0], 535, 128, 0, 640)
            y = map_values(self.hand_pos[1], 223, 422, 0, 640)
            # print(x, y)
            self.cursor_pos = (x, y)

        if self.hands.get_finger_up(1):
            if self.has_shot:
                self.reload()
        else:
            if not self.has_shot:
                self.shoot()

    def draw(self, surface):
        draw.rect(surface, self.color, (self.cursor_pos[0], self.cursor_pos[1], 10, 10), 0)

    def shoot(self):
        self.has_shot = True
        self.color = (255, 255, 0)
        if self.game is not None:
            self.game.shoot(self.cursor_pos)

    def reload(self):
        self.has_shot = False
        self.color = (255, 0, 0)

    def print_debug(self):
        print(self.hands.get_point(self.tracked_point))
