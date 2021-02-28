import numpy as np
from quantity import *

class NotOrthogonalError(RuntimeError):
    def __init__(self):
        pass

class ReferenceSystem:
    def __init__(self, velocity = Velocity()):
        self.velocity = velocity

