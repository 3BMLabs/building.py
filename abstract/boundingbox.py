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


import sys, math, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

# from geometry.point import Point
# from geometry.curve import PolyCurve

from specklepy.objects.geometry import Point
from specklepy.objects.geometry import Polyline


class BoundingBox:
    def __init__(self, points=list[Point]):
        self.points = points
        print(points)
        self.z = 0
        self.x = 0
        self.y = 0

    def corners(self, points=list[Point]):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        ltX = self.x
        ltY = self.y + max_y - min_y

        lbX = self.x
        lbY = self.y + min_y - min_y

        rtX = self.x + max_x - min_x
        rtY = self.y + max_y - min_y

        rbX = self.x + max_x - min_x
        rbY = self.y + min_y - min_y
        
        left_top = Point(x=ltX, y=ltY, z=self.z)
        left_bottom = Point(x=lbX, y=lbY, z=self.z)
        right_top = Point(x=rtX, y=rtY, z=self.z)
        right_bottom = Point(x=rbX, y=rbY, z=self.z)
        
        return left_top, left_bottom, right_bottom, right_top


    def perimeter(self):
        left_top, left_bottom, right_bottom, right_top = self.corners(self.points)
        closed = left_top, left_bottom, right_bottom, right_top, left_top
        p1 = Point(x=0, y=0, z=0)
        p2 = Point(x=0, y=500, z=0)
        p3 = Point(x=400, y=800, z=0)
        return Polyline.from_points([p1,p2,p3,p1])


# ptList = [(0,0), (1,1), (2,2)]
# bTest = BoundingBox(ptList)
# bTest.get_points()

#make sure tthat print prints all given points

    #fetch only the floats/numbers
    #skip the rest of tekens
    #get the smallest x/y
    #draw rectangle around these
    # check if points have xyz or only just xy