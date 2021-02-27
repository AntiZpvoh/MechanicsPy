import numpy as np
from numpy.core import numeric

class DimensionOperateError(RuntimeError):
    def __init__(self):
        pass

class DimensionPowerError(RuntimeError):
    def __init__(self):
        pass

class UnitNotMatchError(RuntimeError):
    def __init__(self):
        pass

class DimensionStructure:
    def __init__(self, up={}):
        self.up = up
        self.basic_quantity_set = set()

    def __eq__(self, rhs):
        for up_key in self.up:
            if up_key not in rhs.up:
                if self.up[up_key] == 0:
                    continue
                else:
                    return False
            if self.up[up_key] != rhs.up[up_key]:
                return False
            
        return True

    def __ne__(self, rhs):
        return not self==rhs

    def __add__(self, rhs):
        if self!=rhs:
            raise DimensionOperateError
        else:
            return self

    def __sub__(self, rhs):
        if self!=rhs:
            raise DimensionOperateError
        else:
            return self

    def __mul__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == DimensionStructure:
            new_up = self.up.copy()
            for up_key in rhs.up:
                if up_key in self.up:
                    new_up[up_key] = self.up[up_key] + rhs.up[up_key]
                else:
                    new_up[up_key] = rhs.up[up_key]

            return DimensionStructure(up=new_up)
        else:
            raise TypeError()

    def __truediv__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == DimensionStructure:
            new_up = self.up.copy()
            for up_key in rhs.up:
                if up_key in new_up:
                    new_up[up_key] = self.up[up_key] - rhs.up[up_key]
                else:
                    new_up[up_key] = - rhs.up[up_key]

            return DimensionStructure(up=new_up)
        else:
            raise TypeError()

    def __pow__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            new_up = self.up.copy()
            for up_key in new_up:
                new_up[up_key] *= rhs

            return DimensionStructure(up=new_up)
        else:
            raise DimensionPowerError()

    def output(self):
        return "{}".format(self.up)

    def __str__(self):
        return "{}".format(self.up)

class BasicUnit:
    def __init__(self, form="space", name="m", factor=1):
        self.form = form
        self.name = name
        self.factor = factor

    def unitToStd(self, unit_value):
        return unit_value * self.factor

    def stdToUnit(self, std_value):
        return std_value / self.factor

    def __eq__(self, rhs):
        return self.form == rhs.form and \
               self.name == rhs.name and \
               self.factor == rhs.factor

    def __ne__(self, rhs):
        return not self==rhs

    def __add__(self, rhs):
        if self.form!=rhs.form:
            raise DimensionOperateError
        else:
            return self

    def __sub__(self, rhs):
        if self.form!=rhs.form:
            raise DimensionOperateError
        else:
            return self

    def __mul__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == BasicUnit:
            dim = DimensionStructure(up={self.form : 1}) * DimensionStructure(up={rhs.form : 1})
            basic_unit_map = {}
            basic_unit_map[rhs.form] = rhs
            basic_unit_map[self.form] = self
            return ComplexUnit(dim = dim, basic_unit_map = basic_unit_map)
        elif type(rhs) == ComplexUnit:
            return ComplexUnit * self
        else:
            raise TypeError()

    def __truediv__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == BasicUnit:
            dim = DimensionStructure(up={self.form : 1}) / DimensionStructure(up={rhs.form : 1})
            basic_unit_map = {}
            basic_unit_map[rhs.form] = rhs
            basic_unit_map[self.form] = self
            return ComplexUnit(dim = dim, basic_unit_map = basic_unit_map)
        elif type(rhs) == ComplexUnit:
            return ComplexUnit / self
        else:
            raise TypeError()

    def __pow__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            dim = DimensionStructure(up={self.form : 1}) ** rhs
            basic_unit_map = {}
            basic_unit_map[self.form] = self
            return ComplexUnit(dim = dim, basic_unit_map = basic_unit_map)
        else:
            raise TypeError()

    def __str__(self):
        return "[{}]".format(self.name)

class ComplexUnit:
    def __init__(self, dim=DimensionStructure(), basic_unit_map={}, name=None):
        self.dim = dim
        self.basic_unit_map = basic_unit_map
        self.checkUnitMap()
        self.factor, self.name = self.calcFactor()
        self.name = self.name if name is None else name

    def unitToStd(self, unit_value):
        return unit_value * self.factor

    def stdToUnit(self, std_value):
        return std_value / self.factor

    def __eq__(self, rhs):
        return self.dim == rhs.dim and \
               self.basic_unit_map == rhs.basic_unit_map

    def __ne__(self, rhs):
        return not self==rhs

    def __add__(self, rhs):
        if self.dim!=rhs.dim:
            raise DimensionOperateError
        else:
            return self

    def __sub__(self, rhs):
        if self.dim!=rhs.dim:
            raise DimensionOperateError
        else:
            return self

    def __mul__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == ComplexUnit:
            dim = self.dim * rhs.dim
            new_basic_unit_map = self.basic_unit_map.copy()
            for rhs_unit in rhs.basic_unit_map:
                if rhs_unit not in new_basic_unit_map:
                    new_basic_unit_map[rhs_unit] = rhs.basic_unit_map[rhs_unit]
            return ComplexUnit(dim = dim, basic_unit_map = new_basic_unit_map)
        elif type(rhs) == BasicUnit:
            dim = self.dim * DimensionStructure(up={rhs.form : 1})
            new_basic_unit_map = self.basic_unit_map.copy()
            if rhs.form not in new_basic_unit_map:
                new_basic_unit_map[rhs.form] = rhs
            return ComplexUnit(dim = dim, basic_unit_map = new_basic_unit_map)
        else:
            raise TypeError()

    def __truediv__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            return self
        elif type(rhs) == ComplexUnit:
            dim = self.dim / rhs.dim
            new_basic_unit_map = self.basic_unit_map.copy()
            for rhs_unit in rhs.basic_unit_map:
                if rhs_unit not in new_basic_unit_map:
                    new_basic_unit_map[rhs_unit] = rhs.basic_unit_map[rhs_unit]
            return ComplexUnit(dim = dim, basic_unit_map = new_basic_unit_map)
        elif type(rhs) == BasicUnit:
            dim = self.dim / DimensionStructure(up={rhs.form : 1})
            new_basic_unit_map = self.basic_unit_map.copy()
            if rhs.form not in new_basic_unit_map:
                new_basic_unit_map[rhs.form] = rhs
            return ComplexUnit(dim = dim, basic_unit_map = new_basic_unit_map)
        else:
            raise TypeError()

    def __pow__(self, rhs):
        if type(rhs) == int or type(rhs) == float:
            dim = self.dim ** rhs
            basic_unit_map = self.basic_unit_map.copy()
            return ComplexUnit(dim = dim, basic_unit_map = basic_unit_map)
        else:
            raise TypeError()

    def checkUnitMap(self):
        for up_key in self.dim.up:
            if up_key not in self.basic_unit_map:
                raise UnitNotMatchError()

        for form in self.basic_unit_map:
            if self.basic_unit_map[form].form != form:
                raise UnitNotMatchError()

    def calcFactor(self):
        result_up = 1
        name_up = ""
        for up_key in self.dim.up:
            result_up *= self.basic_unit_map[up_key].factor**self.dim.up[up_key]
            if self.dim.up[up_key] == 1:
                name_up += self.basic_unit_map[up_key].name + " "
            elif self.dim.up[up_key] != 0:
                name_up += (self.basic_unit_map[up_key].name + "^" + str(self.dim.up[up_key])) + " "
        return result_up, name_up

    def __str__(self):
        return "[{}]".format(self.name)

meter = BasicUnit(form="space", name="m", factor=1)
second = BasicUnit(form="time", name="s", factor=1)
kilogram = BasicUnit(form="mass", name="kg", factor=1)
kilometer = BasicUnit(form="space", name="km", factor=1000)
minute = BasicUnit(form="time", name="min", factor=60)
gram = BasicUnit(form="mass", name="g", factor=0.001)

velocity_dim = DimensionStructure(up={"space" : 1, "time" : -1})
meterPerSecond = ComplexUnit(dim=velocity_dim, basic_unit_map={"space":meter, "time":second})

acceleration_dim = DimensionStructure(up={"space" : 1, "time" : -2})
meterPerSecond2 = ComplexUnit(dim=acceleration_dim, basic_unit_map={"space":meter, "time":second})

force_dim = DimensionStructure(up={"space" : 1, "time" : -2, "mass" : 1})
newton = ComplexUnit(dim=force_dim, basic_unit_map={"space":meter, "time":second, "mass": kilogram})