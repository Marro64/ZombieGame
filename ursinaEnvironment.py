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

        # camera.position = (100, 200, 100)
        # camera.rotation_x  = 90
        camera.position = (2, 6, 2)
        camera.rotation_y = 45
        camera.rotation_x = -5
        camera.fov = 93

if __name__ == "__main__":
    pass