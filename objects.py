from refsys import *

class DynamicObject:
    def __init__(self, mass = Mass(d), \
                 position = Position(0, 0, 0), \
                 time = Time(0), \
                 velocity = Velocity(0, 0, 0), \
                 force = Force(0, 0, 0), \
                 refsys = ReferenceSystem()):
        self.mass = mass
        self.position = position
        self.time = time
        self.velocity = velocity
        self.force = force
        self.refsys = refsys

    def output(self):
        return "mass: {}\nposition: {}\nvelocity: {}\nforce: {}".format(self.mass, self.position, self.velocity, self.force)

    def __str__(self):
        return "mass: {}\nposition: {}\nvelocity: {}\nforce: {}".format(self.mass, self.position, self.velocity, self.force)