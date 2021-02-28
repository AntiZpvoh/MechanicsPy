from objects import *

class LawSystem:
    def __init__(self, ref_translate_func = None, motion_update_func = None, force_update_func = []):
        self.ref_translate_func = ref_translate_func
        self.motion_update_func = motion_update_func
        self.force_update_func = force_update_func

    def translateReferenceSystem(self, obj, refsys):
        return self.ref_translate_func(obj, refsys)

    def motionUpdate(self, obj):
        return self.motion_update_func(obj)


def naive_ref_translate(obj, refsys):
    delta_ref_v = obj.refsys.velocity - refsys.velocity
    obj.velocity += delta_ref_v
    obj.refsys = refsys

def naive_motion_update(obj):
    obj.time += d
    obj.postion += obj.velocity * d
    acceleration = obj.force / obj.mass
    obj.velocity += acceleration * d

def gravity_force_update(obj1, obj2):
    if not isinstance(obj1, DynamicObject) or not isinstance(obj2, DynamicObject):
        return
    G_unit = newton*(meter**2)/(kilogram**2)
    G_quantity = Quantity(G, unit=G_unit)
    r2 = (obj1.position - obj2.position).getSquareSum()
    gravity = G_quantity * obj1.mass * obj2.mass / r2
    obj1.force += gravity
    obj2.force += gravity

GravityClassicalLawSystem = LawSystem(naive_ref_translate, naive_motion_update, [gravity_force_update])