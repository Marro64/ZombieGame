from temp_first_person_controller import *
from ursinaZombie import *
from AI.maze import Maze
from AI.helpers.constants import Constants
from ursina.shaders import normals_shader

from ursina import *

class UrsinaEnvironment:
    def __init__(self, size):


        self.ground = Entity(model="gamePlane_10",
                        color=color.rgb(0, 128, 0),
                        # shader="normals_shader",
                        texture="grass",
                        position=(100, 0, 100),
                        rotation=(0, -90, 0),
                        scale=(size[0]/10, (size[0]+size[1])/20*1.5, size[1]/10),
                        collider="mesh"
                        )

        camera.position = (0, 4, 0)
        camera.rotation_y = 45
        camera.rotation_x = -5
        camera.fov = 90

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


# camera.rotation_z =

# Vec3(98.5648, 0, -97.9014)
# 0
# Vec3(0, -46.1568, 0)
# entity.setPos()
# maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, (200, 200))
# maze.generate_open_maze()
# zombie = UrsinaZombie((0, 0), maze, x=100, y=1000, z=100)
# player = FirstPersonController(y=1000, speed=10)

# player2=FirstPersonController(y=100)
# zombie.add_script(SmoothFollow(targe
# t=player,offset=[0,0,0],speed=0.5))
# def update():
#
#     print(player.position)

if __name__ == "__main__":
    pass