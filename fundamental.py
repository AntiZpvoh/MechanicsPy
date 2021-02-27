import numpy as np
from units import *

d = np.float64(1E-20)

class Quantity:
    def __init__(self, value=np.float64(0), unit=meter):
        self.value = value
        self.unit = unit
        self.__std_val__ = unit.unitToStd(value)

    def __eq__(self, rhs):
        dim_equal = False
        if type(self.unit) == BasicUnit and type(rhs.unit) == BasicUnit:
            dim_equal = self.unit.form == rhs.unit.form
        elif type(self.unit) == ComplexUnit and type(rhs.unit) == ComplexUnit:
            dim_equal = self.unit.dim == rhs.unit.dim
        return self.__std_val__ == rhs.__std_val__ and dim_equal

    def __ne__(self, rhs):
        return not self==rhs

    def __add__(self, rhs):
        if type(rhs) == Quantity:
            std_val = self.__std_val__ + rhs.__std_val__
            unit = self.unit + rhs.unit
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def __sub__(self, rhs):
        if type(rhs) == Quantity:
            std_val = self.__std_val__ - rhs.__std_val__
            unit = self.unit - rhs.unit
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def __mul__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            std_val = self.__std_val__ * rhs
            unit = self.unit * rhs
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        elif type(rhs) == Quantity:
            std_val = self.__std_val__ * rhs.__std_val__
            unit = self.unit * rhs.unit
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def __truediv__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            std_val = self.__std_val__ / rhs
            unit = self.unit / rhs
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        elif type(rhs) == Quantity:
            std_val = self.__std_val__ / rhs.__std_val__
            unit = self.unit / rhs.unit
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def __pow__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            std_val = np.power(self.__std_val__, rhs)
            unit = self.unit ** rhs
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def setUnit(self, unit):
        dim_equal = False
        if type(self.unit) == BasicUnit and type(unit) == BasicUnit:
            dim_equal = self.unit.form == unit.form
        elif type(self.unit) == ComplexUnit and type(unit) == ComplexUnit:
            dim_equal = self.unit.dim == unit.dim
        if not dim_equal:
            raise TypeError()
        self.unit = unit
        self.value = unit.stdToUnit(self.__std_val__)

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)


