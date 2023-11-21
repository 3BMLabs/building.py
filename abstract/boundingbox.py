# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides tools for boundingbox
"""

__title__= "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/boundingbox.py"


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from geometry.curve import PolyCurve
import helper


# [!not included in BP singlefile - end]

class BoundingBox2d:
    def __init__(self):
        self.id = helper.generateID()
        self.points = []
        self.corners = []
        self.isClosed = True
        self.width = 0
        self.height = 0
        self.z = 0

    def length(self):
        return 0
    
    def area(self):
        return 0

    def byPoints(self, points=Point):
        self.points = points
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        
        left_top = Point(x=min_x, y=max_y, z=self.z)
        left_bottom = Point(x=min_x, y=min_y, z=self.z)
        right_top = Point(x=max_x, y=max_y, z=self.z)
        right_bottom = Point(x=max_x, y=min_y, z=self.z)
        self.width = abs(Point.distance(left_top, right_top))
        self.height = abs(Point.distance(left_top, left_bottom))
        self.corners.append(left_top) 
        self.corners.append(left_bottom) 
        self.corners.append(right_bottom)
        self.corners.append(right_top)
        # print(self.height)
        return self


class BoundingBox3d:
    def __init__(self, points=Point):
        self.points = points


    def corners(self, points=Point):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        min_z = min(z_values)
        max_z = max(z_values)

        left_top_bottom = Point(x=min_x, y=max_y, z=min_z)
        left_bottom_bottom = Point(x=min_x, y=min_y, z=min_z)
        right_top_bottom = Point(x=max_x, y=max_y, z=min_z)
        right_bottom_bottom = Point(x=max_x, y=min_y, z=min_z)
        
        left_top_top = Point(x=min_x, y=max_y, z=max_z)
        left_bottom_top = Point(x=min_x, y=min_y, z=max_z)
        right_top_top = Point(x=max_x, y=max_y, z=max_z)
        right_bottom_top = Point(x=max_x, y=min_y, z=max_z)

        return [left_top_bottom, left_top_top, right_top_top, right_top_bottom, left_top_bottom, left_bottom_bottom, left_bottom_top, left_top_top, left_bottom_top, right_bottom_top, right_bottom_bottom, left_bottom_bottom, right_bottom_bottom, right_top_bottom, right_top_top, right_bottom_top]

    def perimeter(self):
        return PolyCurve.byPoints(self.corners(self.points))