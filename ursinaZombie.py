from ursina.prefabs.first_person_controller import *


from ursina import *




class Zombie(Button):
    def __init__(self, x, y, z):
        super().__init__(
            parent =scene,
            model="zombie",
            # color=color.rgb(255, 255, 255),
            position=(x,y,z),
            rotation=(0, 0, 0),
            collider = "box",
           scale=(0.05, 0.05, 0.05)
           )


app =   Ursina()
entity = Entity(model = "Environment",
                # color= color.rgb(0,255,0),
                texture="grass",
                position=(0,0,0),
                rotation=(0,0,0),
                # scale=(1,1,5),
                scale=20,
                collider="mesh"
                )
zombie = Zombie(84.9217, 0, -28.8431)
# eentity = Entity(model = "zombie",
#                 color=color.rgb(255,255,255),
#                 position=(84.9217, 0, -28.8431),
#                 rotation=(0, 0, 0),
#                 scale=(0.05, 0.05, 0.05)
#                 )

# EditorCamera( )
# camera.orthographic = True


camera.position = (128.5648, 10, -127.9014)
camera.rotation_y  =-45


# Vec3(98.5648, 0, -97.9014)
# 0
# Vec3(0, -46.1568, 0)
# camera.fov = 40
# entity.setPos()
player = FirstPersonController(y=1000)
# zombie.add_script(SmoothFollow(target=player,offset=[0,0,0],speed=0.5))
# def update():
#     # eentity.rotation_y+=1

    # print(player.position)
    # print(0)
    # print(player.rotation)
def input(key):
    if key=="left mouse down":
        print(1)
        # hitInfo=raycast((0,0,0), direction=(0, 1, 0), distance=inf)
        # zombie.setPos(10.5915, 11.8211, 7.7733)
        if zombie.hovered:
            print(0)
            destroy(zombie)


app.run()