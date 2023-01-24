import traceback
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from ursina import application
from ursina.window import instance as window
from ursina.scene import instance as scene
from ursina.camera import instance as camera
from ursina.hit_info import HitInfo
from ursina.ursinamath import distance

# Code from Ursina, hastily modified to use a virtual curser instead of the OS cursor


class HitDetection:

    def __init__(self, cursor):
        self.hovered_entity = None # returns the closest hovered entity with a collider.
        self.traverse_target = scene  # set this to None to disable collision with scene, which might be a good idea if you have lots of colliders.
        self._picker = CollisionTraverser()  # Make a traverser
        self._pq = CollisionHandlerQueue()  # Make a handler
        self._pickerNode = CollisionNode('mouseRay')
        self._pickerNP = camera.attach_new_node(self._pickerNode)
        self._pickerRay = CollisionRay()  # Make our ray
        self._pickerNode.addSolid(self._pickerRay)
        self._picker.addCollider(self._pickerNP, self._pq)
        self._pickerNode.set_into_collide_mask(0)

        self.raycast = True
        self.collision = None
        self.collisions = []
        self.enabled = True


    # calls on_hit() for the frontmost enemies overlapping an UI coordinate
    def shoot(self, position):
        x = position[0]
        y = position[1]
        # collide with world
        self._pickerNP.reparent_to(camera)
        self._pickerRay.set_from_lens(scene.camera.lens_node, x * 2 / window.aspect_ratio, y * 2)
        if self.traverse_target:
            self._picker.traverse(self.traverse_target)

        if self._pq.get_num_entries() > 0:
            self.find_collision()

        self.left = True
        if self.hovered_entity:
            if hasattr(self.hovered_entity, 'on_hit') and callable(self.hovered_entity.on_hit):
                try:
                    self.hovered_entity.on_hit()
                except Exception as e:
                    print(traceback.format_exc())
                    application.quit()

            for s in self.hovered_entity.scripts:
                if hasattr(s, 'on_hit') and callable(s.on_hit):
                    s.on_hit()

    @property
    def normal(self): # returns the normal of the polygon, in local space.
        if not self.collision is not None:
            return None
        return Vec3(*self.collision.normal)

    @property
    def world_normal(self): # returns the normal of the polygon, in world space.
        if not self.collision is not None:
            return None
        return Vec3(*self.collision.world_normal)

    @property
    def point(self): # returns the point hit, in local space
        if self.collision is not None:
            return Vec3(*self.collision.point)
        return None

    @property
    def world_point(self): # returns the point hit, in world space
        if self.collision is not None:
            return Vec3(*self.collision.world_point)
        return None

    def find_collision(self):
        self.collisions = []
        self.collision = None
        if not self.raycast or self._pq.get_num_entries() == 0:
            self.unhover_everything_not_hit()
            return False

        self._pq.sortEntries()

        for entry in self._pq.getEntries():
            for entity in scene.entities:
                if entry.getIntoNodePath().parent == entity and entity.collision:
                    if entity.collision:
                        hit = HitInfo(
                            hit = entry.collided(),
                            entity = entity,
                            distance = distance(entry.getSurfacePoint(scene), camera.getPos()),
                            point = entry.getSurfacePoint(entity),
                            world_point = entry.getSurfacePoint(scene),
                            normal = entry.getSurfaceNormal(entity),
                            world_normal = entry.getSurfaceNormal(scene),
                            )
                        self.collisions.append(hit)
                        break

        if self.collisions:
            self.collision = self.collisions[0]
            self.hovered_entity = self.collision.entity
            if not self.hovered_entity.hovered:
                self.hovered_entity.hovered = True
                if hasattr(self.hovered_entity, 'on_mouse_enter'):
                    self.hovered_entity.on_mouse_enter()
                for s in self.hovered_entity.scripts:
                    if hasattr(s, 'on_mouse_enter'):
                        s.on_mouse_enter()


        self.unhover_everything_not_hit()



    def unhover_everything_not_hit(self):
        for e in scene.entities:
            if e == self.hovered_entity:
                continue

            if hasattr(e, 'hovered') and e.hovered:
                e.hovered = False
                if hasattr(e, 'on_mouse_exit'):
                    e.on_mouse_exit()
                for s in e.scripts:
                    if hasattr(s, 'on_mouse_exit'):
                        s.on_mouse_exit()

