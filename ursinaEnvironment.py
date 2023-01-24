from temp_first_person_controller import *
from ursinaZombie import *
from AI.maze import Maze
from AI.helpers.constants import Constants
from ursina.shaders import normals_shader

from ursina import *



# class Player(Entity):
#     def __init__(self,**kwargs):
#         self.controller =FirstPersonController(**kwargs)
#         super().__init__(parent = self.controller)
class UrsineEnviroment(Button):
    def __init__(self, x, y, z):
        self.ground = Entity(model="gamePlane_10",
                        # color= color.rgb(0,128,0),
                        # shader="normals_shader",
                        texture="grass",
                        position=(0, 0, 0),
                        rotation=(0, -90, 0),
                        # scale=(1,1,5),
                        scale=(20, 30, 20),
                        collider="mesh"
                        )


app =   Ursina()

zombie = Zombie(84.9217, 0, -28.8431)
# eentity = Entity(model = "zombie",
#                 color=color.rgb(255,255,255),
#                 position=(84.9217, 0, -28.8431),
#                 rotation=(0, 0, 0),
#                 scale=(0.05, 0.05, 0.05)
#                 )

# EditorCamera( )
# camera.orthographic = True

#
# camera.position = (128.5648, 10, 127.9014)
# camera.rotation_y = -135
# camera.position = (0, 400, 0)
# camera.rotation_x  = 90
# camera.position = (100, 2, 100)
# camera.rotation_y = -135
camera.position = (-100, 4, -100)
camera.rotation_y = 45
camera.rotation_x = -5

# camera.rotation_z =

# Vec3(98.5648, 0, -97.9014)
# 0
# Vec3(0, -46.1568, 0)
camera.fov = 90
# entity.setPos()
maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, (200, 200))
maze.generate_open_maze()
zombie = UrsinaZombie((-1, -1), maze, x=-100, y=1000, z=-100)
# player = FirstPersonController(y=1000, speed=10)

# player2=FirstPersonController(y=100)
# zombie.add_script(SmoothFollow(targe
# t=player,offset=[0,0,0],speed=0.5))
# def update():
#
#     print(player.position)
def input(key):
    if key=="left mouse down":
        print(1)
        # hitInfo=raycast((0,0,0), direction=(0, 1, 0), distance=inf)
        # zombie.setPos(10.5915, 11.8211, 7.7733)
        if zombie.hovered:
            print(0)
            destroy(zombie)


app.run()