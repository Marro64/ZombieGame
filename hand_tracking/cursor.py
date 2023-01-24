from hand_tracking.hand_tracking import HandTracking
from ursina import *
from numpy import interp


def map_values(x, a, b, c, d):
    y = (x-a)/(b-a)*(d-c)+c
    return y


class Cursor(Entity):
    def __init__(self, game, tracked_point=9, trigger_finger=0):
        super().__init__(
            parent=camera.ui,
            model="quad",
            color=color.rgb(255, 0, 0),
            position=(0,0,0),
            rotation=(0, 0, 0),
            scale=(0.02, 0.02, 0.02)
        )
        self.hands = HandTracking()
        self.hand_pos = None
        self.cursor_pos = (0, 0)
        self.tracked_point = tracked_point
        self.trigger_finger = trigger_finger
        self.has_shot = False
        self.game = game


    def update(self):
        self.hands.update()

        self.hand_pos = self.hands.get_point(self.tracked_point)
        if self.hand_pos is not None:
            # print(self.hand_pos)
            x = map_values(self.hand_pos[0], 535, 128, -.5, .5)
            y = map_values(self.hand_pos[1], 223, 422, .5, -.5)
            # x = interp(self.hand_pos[0], [535, 128], [-5, 5])
            # y = interp(self.hand_pos[1], [223, 422], [-5, 5])
            # print(x, y)
            self.cursor_pos = (x, y)

        if self.hands.get_finger_up(self.trigger_finger):
            if self.has_shot:
                self.reload()
        else:
            if not self.has_shot:
                self.shoot()

        self.position = self.cursor_pos

    def shoot(self):
        self.has_shot = True
        self.color = color.rgb(255, 255, 0)
        if self.game is not None:
            self.game.shoot(self.cursor_pos)

    def reload(self):
        self.has_shot = False
        self.color = color.rgb(255, 0, 0)

    def print_debug(self):
        print(self.hands.get_point(self.tracked_point))
