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


"""This module provides tools to create a PointList
"""

__title__ = "PointList"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/PointList.py"


import operator
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from abstract.rect import Rect
from abstract.vector import Vector
from packages.helper import *

class PointList(Vector[Vector]):
    """Represents a collection of points in space as a point cloud."""
    
    def __init__(self, points: list) -> 'PointList':
        """Initializes a PointList object with a list of points.

        #### Parameters:
        - `points` (list): An optional list of points to initialize the point cloud. Each point can be an instance of a Point class or a tuple/list of coordinates.

        Initializes the PointList's attributes and sets up the list of points based on the input provided. The ID is generated to uniquely identify the point cloud.
        """
        super().__init__(points)
        
    
    #just execute the operator for all list members
    def operate_2(self, op:operator, other):
        return self.__class__([self[index].operate_2(op, other) for index in range(len(self))])
    
    def ioperate_2(self, op:operator, other):
        for index in range(len(self)):
            self[index].ioperate_2(op, other)
        return self

    def operate_1(self, op:operator):
        return self.__class__([self[index].operate_1(op) for index in range(len(self))])
    
    @property
    def bounds(self) -> 'Rect':
        return Rect.by_points(self)

#alternative naming
PointCloud = PointList