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


"""This module provides tools to create curves
"""

__title__= "curve"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/curve.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.point import *
from packages import helper


class Line:
    def __init__(self, start: Point, end: Point, id=helper.generateID()) -> None:
        self.start: Point = start
        self.end: Point = end
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        self.z = [self.start.z, self.end.z]
        self.dx = self.end.x-self.start.x
        self.dy = self.end.y-self.start.y
        self.dz = self.end.z-self.start.z
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    @staticmethod
    def length(self):
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy) + self.dz * self.dz)

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.start},{self.end})"


class PolyCurve: #pass this object before using it.
    def __init__(self, id=helper.generateID()) -> None:
        self.curves = [] #collect in list
        self.points = []
        self.id = id

    @classmethod
    def byJoinedCurves(cls, curvelst):
        p1 = PolyCurve()
        for i in curvelst:
            p1.curves.append(i)
            p1.points.append(i.start)
        return p1

    @classmethod
    def byPoints(cls, points):
        #by points,
        p1 = PolyCurve()
        count = 0
        p1.points = points
        for i in points:
            count = count + 1
            try:
                p1.curves.append(Line(start=i, end=points[count]))
            except:
                p1.curves.append(Line(start=i, end=points[0]))
        return p1

    @classmethod
    def byPolyCurve2D(cls, PolyCurve2D):
        #by points,
        p1 = PolyCurve()
        count = 0
        points = []
        for i in PolyCurve2D.curves:
            points.append(Point(i.start.x, i.start.y, 0))
        p1.points = points
        for i in points:
            count = count + 1
            try:
                p1.curves.append(Line(start=i, end=points[count]))
            except:
                p1.curves.append(Line(start=i, end=points[0]))
        return p1

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self):
        PolyCurveName = f"{__class__.__name__}("
 #       for i in self.curves:
#            PolyCurveName = PolyCurveName + i
        return PolyCurveName + ")"

#2D PolyCurve to 3D PolyGon
def polygon(flatCurves):
    points = []
    for i in flatCurves:
        points.append(i.start)
        try:
            points.append(i.middle)
        except:
            pass
    points.append(points[0])
    points3D = []
    for i in points:
        points3D.append(Point.point2DTo3D(i))
    return points3D

class PolyGon:
    def __init__(self, lines, id=helper.generateID()) -> None:
        self.Lines = lines#collect in list
        self.id = id
        pass #Lines
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Arc:
    def __init__(self, radius, startAngle, endAngle, angleRadians, plane, startPoint, midPoint, endPoint, length, id=helper.generateID()) -> None:
        self.radius = radius
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.angleRadians = angleRadians
        self.plane = plane
        self.startPoint = startPoint
        self.midPoint = midPoint
        self.endPoint = endPoint
        self.length = length
        self.id = id
        pass #Curve

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Circle:
    def __init__(self, radius, plane, length, id=helper.generateID()) -> None:
        self.radius = radius
        self.plane = plane
        self.length = length
        self.id = id
        pass #Curve

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Ellipse:
    def __init__(self, firstRadius, secondRadius, plane, id=helper.generateID()) -> None:
        self.firstRadius = firstRadius
        self.secondRadius = secondRadius
        self.plane = plane
        self.id = id
        pass #Curve
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"

