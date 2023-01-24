from ursina import *
from AI.zombie_AI import ZombieAI
import numpy


class UrsinaZombie(Entity):
    def __init__(self, target, field, **kwargs):
        super().__init__(
            parent=scene,
            # color=color.rgb(255, 255, 255),
            model="Assets/zombie.fbx",
            texture="Assets/zombie",
            rotation=(0, 0, 0),
            collider="box",
            scale=(0.2, 0.2, 0.2)
        )
        self.speed = 5
        self.height = 2
        mouse.locked = False
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y+1

        self.position = self.world_position

        self.zombie_AI = ZombieAI(self.get_position_2d(), target, field, self)

        self.finished = False


    def update(self):
        self.direction = self.zombie_AI.update_heading()
        self.rotation.y = 180 - numpy.degrees(numpy.angle(self.direction[0] + 1j * self.direction[1]))

        direction_2d = self.zombie_AI.update_heading()
        self.direction = Vec3(direction_2d[0], 0, direction_2d[1])
        self.position += self.direction * self.speed * time.dt
        ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
        if ray.world_point is not None:
            self.y = ray.world_point[1]+3

    def get_position_2d(self):
        return self.position[0], self.position[2]

    def is_finished(self):
        return self.zombie_AI.finished() or self.finished

    def on_hit(self):
        self.finished = True
