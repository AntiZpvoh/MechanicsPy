import numpy as np
from units import *

d = np.float64(1E-20)

class QuantityNotRightTypeError(RuntimeError):
    def __init__(self):
        pass

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
        if isinstance(rhs, Quantity):
            std_val = self.__std_val__ + rhs.__std_val__
            unit = self.unit + rhs.unit
            return Quantity(value = unit.stdToUnit(std_val), unit = unit)
        else:
            raise TypeError()

    def __sub__(self, rhs):
        if isinstance(rhs, Quantity):
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
        elif isinstance(rhs, Quantity):
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
        elif isinstance(rhs, Quantity):
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

    def getStdValue(self):
        return self.__std_val__

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

class Mass(Quantity):
    def __init__(self, value = 0, unit = kilogram):
        if type(unit) == BasicUnit and unit.form == "mass":
            Quantity.__init__(self, np.float64(value), unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

class Position(Quantity):
    def __init__(self, x = 0, y = 0, z = 0, unit = meter, value = None):
        if type(unit) == BasicUnit and unit.form == "space":
            if value is None:
                Quantity.__init__(self, np.array([x, y, z], dtype=np.float64), unit)
            else:
                Quantity.__init__(self, value, unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

class Time(Quantity):
    def __init__(self, value = 0, unit = second):
        if type(unit) == BasicUnit and unit.form == "time":
            Quantity.__init__(self, np.float64(value), unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

class Velocity(Quantity):
    def __init__(self, vx = 0, vy = 0, vz = 0, unit = meterPerSecond, value = None):
        if type(unit) == ComplexUnit and unit.dim == velocity_dim:
            if value is None:
                Quantity.__init__(self, np.array([vx, vy, vz], dtype=np.float64), unit)
            else:
                Quantity.__init__(self, value, unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

class Acceleration(Quantity):
    def __init__(self, ax = 0, ay = 0, az = 0, unit = meterPerSecond2, value = None):
        if type(unit) == ComplexUnit and unit.dim == acceleration_dim:
            if value is None:
                Quantity.__init__(self, np.array([ax, ay, az], dtype=np.float64), unit)
            else:
                Quantity.__init__(self, value, unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)

class Force(Quantity):
    def __init__(self, fx = 0, fy = 0, fz = 0, unit = newton, value = None):
        if type(unit) == ComplexUnit and unit.dim == force_dim:
            if value is None:
                Quantity.__init__(self, np.array([fx, fy, fz], dtype=np.float64), unit)
            else:
                Quantity.__init__(self, value, unit)
        else:
            raise QuantityNotRightTypeError()

    def output(self):
        return "{} {}".format(self.value, self.unit)

    def __str__(self):
        return "{} {}".format(self.value, self.unit)