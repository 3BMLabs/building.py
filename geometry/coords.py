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
from typing import Any, SupportsIndex
from packages.helper import generateID
from abstract.serializable import Serializable

import operator

# [!not included in BP singlefile - end]

class Coords(list, Serializable):
    """a shared base class for point and vector. contains the x, y and z coordinates"""
    def __init__(self, *args) -> 'Coords':
        arrayArgs : list = args if len(args) > 1 else args[0]

        list.__init__(self, arrayArgs)
        Serializable.__init__(self)
        self.id = generateID()

    def __str__(self):
        length = len(self)
        result = '['
        if length >= 1:
            result += f'x: {self.x}'
            if length >= 2:
                result += f', y: {self.y}'
                if length >= 3:
                    result += f', z: {self.z}'

        result += ']'
        return result
    
    def __repr__(self):
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