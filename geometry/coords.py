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

from types import UnionType
from typing import Any, Iterable, Self, SupportsIndex
from packages.helper import generateID
from abstract.serializable import Serializable

import operator

# [!not included in BP singlefile - end]

class Coords(list, Serializable):
    """a shared base class for point and vector. contains the x, y and z coordinates"""
    def __init__(self, *args, **kwargs) -> 'Coords':
        arrayArgs:list
        if len(args) == 1 and hasattr(args[0], "__getitem__"):
            arrayArgs :list = args[0]
        else:
            arrayArgs : list = list(args)

        list.__init__(self, arrayArgs)
        Serializable.__init__(self)

        self.id = generateID()
        for kwarg in kwargs.items():
            self.set_axis(kwarg[0], kwarg[1])            

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
    def x(self):
        return self[0]
    @x.setter
    def x(self, value):
        self[0] = value
        
    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, value):
        self[2] = value
    
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
        return self.set_axis(Coords.axis_index(axis_name, value))
                    
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
        
    def operate(self, other, op:operator):
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
    
    def __add__(self, other):
        return self.operate(other, operator.add)

    def __sub__(self, other):
        return self.operate(other, operator.sub)
    
    def __truediv__(self, other):
        return self.operate(other, operator.truediv)

    def __mul__(self, other):
        return self.operate(other, operator.mul)
    __rmul__ = __mul__
    def __iadd__(self, other) -> Self:
        return self.operate(other, operator.iadd)