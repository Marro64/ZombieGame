from ursina import *
from AI.zombie_AI import ZombieAI


class UrsinaZombie(Entity):
    def __init__(self, target, field, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__(
            parent=scene,
            model="zombie",
            # color=color.rgb(255, 255, 255),
            rotation=(0, 0, 0),
            collider="box",
            scale=(0.2, 0.2, 0.2)
        )
        self.speed = 5
        self.height = 2
        mouse.locked = False
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1

        self.zombie_AI = ZombieAI(self.get_position_2d(), target, field, self)

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y

        self.position = self.world_position


    def custom_update(self):

        # self.direction = Vec3(
        #     self.forward * (held_keys['w'] - held_keys['s'])
        #     + self.right * (held_keys['d'] - held_keys['a'])
        #     ).normalized()
        #
        # feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False)
        # head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=False)
        # if not feet_ray.hit and not head_ray.hit:
        #     move_amount = self.direction * time.dt * self.speed
        #
        #     if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,)).hit:
        #         move_amount[0] = min(move_amount[0], 0)
        #     if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,)).hit:
        #         move_amount[0] = max(move_amount[0], 0)
        #     if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,)).hit:
        #         move_amount[2] = min(move_amount[2], 0)
        #     if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,)).hit:
        #         move_amount[2] = max(move_amount[2], 0)
        #     self.position += move_amount
        self.direction = self.zombie_AI.update_heading()

        direction_2d = self.zombie_AI.update_heading()
        self.direction = Vec3(direction_2d[0], 0, direction_2d[1])

        # self.position += self.direction * self.speed * time.dt
        self.position += self.direction * self.speed * time.dt
        # print(self.position)

        # if self.gravity:
        #     # gravity
        ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            # if ray.distance <= self.height+.1:
            #     if not self.grounded:
            #         self.land()
            #     self.grounded = True
            #     # make sure it's not a wall and that the point is not too far up
            #     if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
        self.y = ray.world_point[1]
            #     return
            # else:
            #     self.grounded = False
            #
            # # if not on ground and not on way up in jump, fall
            # self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            # self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space':
            self.jump()


    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = False
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

    def get_position_2d(self):
        return self.position[0], self.position[2]

    def is_finished(self):
        return self.zombie_AI.finished()


if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    window.vsync = False
    app = Ursina()
    # Sky(color=color.gray)
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
    # hill = Entity(model='sphere', position=(20,-10,10), scale=(25,25,25), collider='sphere', color=color.green)
    # hill = Entity(model='sphere', position=(20,-0,10), scale=(25,25,25), collider='mesh', color=color.green)
    # from ursina.shaders import basic_lighting_shader
    # for e in scene.entities:
    #     e.shader = basic_lighting_shader

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    def input(key):
        if key == 'left mouse down' and player.gun:
            gun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    # player.add_script(NoclipMode())
    app.run()
