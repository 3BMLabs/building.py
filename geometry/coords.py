# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module forms the base for points and vectors
"""

__title__ = "coords"
__author__ = "JohnHeikens"
__url__ = "./geometry/coords.py"

import math
from typing import Self
from packages.helper import generateID
from abstract.serializable import Serializable

import operator

def to_array(*args) -> list:
    """converts the arguments into an array.

    Returns:
        list: the arguments provided, converted to a list.
    """
    return args[0] if len(args) == 1 and hasattr(args[0], "__getitem__") else list(args)

# [!not included in BP singlefile - end]

class Coords(list, Serializable):
    """a shared base class for point and vector. contains the x, y and z coordinates"""
    def __init__(self, *args, **kwargs) -> 'Coords':
        arrayArgs:list = to_array(*args)

        list.__init__(self, arrayArgs)
        Serializable.__init__(self)

        self.id = generateID()
        for kwarg in kwargs.items():
            self.set_axis_by_name(kwarg[0], kwarg[1])            

    def __str__(self):
        length = len(self)
        result = self.__class__.__name__ + '('
        if length >= 1:
            result += f'x={self.x}'
            if length >= 2:
                result += f', y={self.y}'
                if length >= 3:
                    result += f', z={self.z}'

        result += ')'
        return result
    
    def __repr__(self) -> str:
        return str(self)
    
    @property
    def x(self): return self[0]
    @x.setter
    def x(self, value): self[0] = value
        
    @property
    def y(self): return self[1]
    @y.setter
    def y(self, value): self[1] = value

    @property
    def z(self): return self[2]
    @z.setter
    def z(self, value): self[2] = value
    
    @property
    def squared_magnitude(self):
        result = 0
        for axis_value in self:
            result += axis_value * axis_value
        return result
    
    @property
    def magnitude(self): 
        """the 'length' could also mean the axis count. this makes it more clear.
        Returns:
            the length
        """
        return math.sqrt(self.squared_magnitude)
        
    
    @property
    def normalized(self):
        """Returns the normalized form of the vector.
        The normalized form of a vector is a vector with the same direction but with a length (magnitude) of 1.

        #### Returns:
        `Vector`: A new Vector object representing the normalized form of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector(3, 0, 4)
        normalized_vector = vector1.normalized
        # Vector(X = 0.600, Y = 0.000, Z = 0.800)
        ```
        """
        sqm = self.squared_magnitude
        
        return self / math.sqrt(sqm) if sqm > 0 else Coords()
    
    @property
    def angle(self):
        #treat this normal vector as a triangle. we know all sides but want to know the angle.
        #tan(deg) = other side / straight side
        #deg = atan(other side / straight side)
        return math.atan2(self.x, self.y)
    
    @staticmethod
    def axis_index(axis:str) -> int:
        """returns index of axis name.<br>
        raises a valueError when the name isn't valid.

        Args:
            axis (str): the name of the axis

        Returns:
            int: the index
        """
        return ['x', 'y', 'z', 'w'].index(axis)

    def change_axis_count(self,axis_count: int):
        """in- or decreases the amount of axes to the preferred axis count.

        Args:
            axis_count (int): the new amount of axes
        """
        if axis_count > len(self):
            diff = axis_count + 1 - len(self)
            self.extend([0] * diff)
        else:
            self = self[:axis_count]
    def set_axis(self, axis_index: int, value) -> int | None:
        """sets an axis with the specified index to the value. will resize when the coords can't contain them.

        Args:
            axis_index (int): the index of the axis, for example 2
            value: the value to set the axis to

        Returns:
            int: the new size when resized, -1 when the axis is invalid, None when the value was just set.
        """

        if axis_index >= len(self):
            self.extend([0] * (axis_index - len(self)))
            self.extend([value])
            return axis_index
        self[axis_index] = value
        return None
        
    def set_axis_by_name(self, axis_name: str, value) -> int | None:
        """sets an axis with the specified name to the value. will resize when the coords can't contain them.

        Args:
            axis_name (str): the name of the axis, for example 'x'
            value: the value to set the axis to

        Returns:
            int: the new size when resized, -1 when the axis is invalid, None when the value was just set.
        """
        return self.set_axis(Coords.axis_index(axis_name), value)
                    
    def volume(self):
        result = 1
        for val in self:
            result *= val
        return result
        
    #useful for sorting
    def compare(self, other):
        for axis in range(len(self)):
            if self[axis] != other[axis]:
                return other[axis] - self[axis]
        return 0
        
    def operate_2(self, op:operator, other):
        result = Coords([0] * len(self))
        try:
            for index in range(len(self)):
                result[index] = op(self[index], other[index])
        except TypeError:
            #variable doesn't support index
            #https://stackoverflow.com/questions/7604380/check-for-operator
            for index in range(len(self)):
                result[index] = op(self[index], other)
        return result
    def operate_1(self, op:operator):
        result = Coords([0] * len(self))
        for index in range(len(self)):
            result[index] = op(self[index])
        return result
    def __add__(self, other):
        return self.operate_2(operator.add,other)

    def __sub__(self, other):
        return self.operate_2(operator.sub,other)
    
    def __truediv__(self, other):
        return self.operate_2(operator.truediv,other)

    def __mul__(self, other):
        return self.operate_2(operator.mul,other)
    __rmul__ = __mul__
    
    def __iadd__(self, other) -> Self:
        return self.operate_2(operator.iadd,other)
    def __neg__(self) -> Self:
        return self.operate_1(operator.neg)