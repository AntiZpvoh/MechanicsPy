import numpy as np
from quantity import *

class NotOrthogonalError(RuntimeError):
    def __init__(self):
        pass

def normalize(vector):
    return vector / np.power(np.sum(np.power(vector, 2)), 0.5)

class ReferenceSystem:
    def __init__(self, velocity = Velocity(), \
                 axis_x = Position(1, 0, 0), axis_y = Position(0, 1, 0), axis_z = Position(0, 0, 1), \
                 origin = Position(0, 0, 0)):
        self.velocity = velocity
        self.origin = origin
        x_std = normalize(axis_x.getStdValue())
        y_std = normalize(axis_y.getStdValue())
        z_std = normalize(axis_z.getStdValue())
        self.axis_matrix = np.stack((x_std, y_std, z_std))
        print(self.axis_matrix)
        if not np.all(np.dot(self.axis_matrix, self.axis_matrix.T) == np.identity(3)):
            raise NotOrthogonalError()

    def stdToRef(self, position):
        std_pos_in_std = position.getStdValue()
        std_pos_in_ref = np.dot(self.axis_matrix, (std_pos_in_std - self.origin.getStdValue()).T)
        return Position(value=position.unit.stdToUnit(std_pos_in_ref), unit=position.unit)

    def refToStd(self, position):
        std_pos_in_std = position.getStdValue()
        std_pos_in_ref = np.dot(self.axis_matrix.T, (std_pos_in_std + self.origin.getStdValue()).T)
        return Position(value=position.unit.stdToUnit(std_pos_in_ref), unit=position.unit)

