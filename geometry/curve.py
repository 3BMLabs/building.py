# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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
from abstract.vector import Vector3
from abstract.plane import Plane
from specklepy.objects.primitive import Interval as SpeckleInterval #temp


class Line: #add Line.bylenght (start and endpoint)
    def __init__(self, start: Point or Point2D, end: Point or Point2D, id=helper.generateID()) -> None:
        self.start: Point = start
        self.end: Point = end
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        try:
            self.z = [self.start.z, self.end.z]
        except:
            self.z = 0
        self.dx = self.end.x-self.start.x
        self.dy = self.end.y-self.start.y
        try:
            self.dz = self.end.z-self.start.z
        except:
            self.dz = 0
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    def length(self):
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy) + self.dz * self.dz)

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.start},{self.end})"


class PolyCurve:
    def __init__(self, points=None, id=helper.generateID()):
        self.curves = []
        self.points = points or []
        self.id = id

    @classmethod
    def byJoinedCurves(cls, curvelst):
        p1 = PolyCurve()
        for i in curvelst:
            p1.curves.append(i)
            p1.points.append(i.start)
        return p1

    @classmethod
    def byPoints(cls, points:list[Point]):
        crvs = []
        p1 = PolyCurve()
        curves = []
        
        for index, point in enumerate(points):
            try:
                nextpoint = points[index+1]
                
                crvs.append(Line(start=point, end=nextpoint))
            except:
                firstpoint = points[0]
                crvs.append(Line(start=point, end=firstpoint))
        crv = PolyCurve.byJoinedCurves(crvs)
        return crv


    @classmethod
    def byPolyCurve2D(cls, PolyCurve2D):
        # by points,
        p1 = PolyCurve()
        count = 0
        points = []
        for i in PolyCurve2D:
            points.append(Point(i.start.x, i.start.y, 0))
        p1.points = points
        for i in points:
            count = count + 1
            try:
                p1.curves.append(Line(start=i, end=points[count]))
            except:
                p1.curves.append(Line(start=i, end=points[0]))
        return p1

    def translate(self, vector3d:Vector3):
        crvs = []
        v1 = vector3d
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.translate(i.start, v1), Point.translate(i.middle, v1), Point.translate(i.end, v1)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.translate(i.start, v1), Point.translate(i.end, v1)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.byJoinedCurves(crvs)
        return crv

    def rotate(self, angle, dz):
        #angle in degrees
        #dz = displacement in z-direction
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.rotateXY(i.start, angle, dz), Point.rotateXY(i.middle, angle, dz), Point.rotateXY(i.end, angle, dz)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.rotateXY(i.start, angle, dz), Point.rotateXY(i.end, angle, dz)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.byJoinedCurves(crvs)
        return crv
    
    def __id__(self):
        return f"id:{self.id}"

    def __str__(self):
        PolyCurveName = f"{__class__.__name__}("
#       for i in self.curves:
#            PolyCurveName = PolyCurveName + i
        return PolyCurveName + ")"

# 2D PolyCurve to 3D PolyGon

def Rect(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(width, 0, 0), vector)
    p3 = Point(0,0,0).translate(Point(width, height, 0), vector)
    p4 = Point(0,0,0).translate(Point(0, height, 0), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4, p1])
    return crv

def RectXY(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(width, 0, 0), vector)
    p3 = Point(0,0,0).translate(Point(width, 0, height), vector)
    p4 = Point(0,0,0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4, p1])
    return crv

def RectYZ(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(0, width, 0), vector)
    p3 = Point(0,0,0).translate(Point(0, width, height), vector)
    p4 = Point(0,0,0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4, p1])
    return crv

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
    def __init__(self, startPoint: Point, midPoint: Point, endPoint: Point):
        self.startPoint = startPoint
        self.midPoint = midPoint
        self.endPoint = endPoint

        v1=Vector3(x=1, y=0, z=0)
        v2=Vector3(x=0, y=1, z=0)
        self.plane = Plane.byTwoVectorsOrigin(
            v1, 
            v2, 
            Point((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2)
        )
        
        self.radius=self.radius()
        self.startAngle=0
        self.endAngle=0
        self.angleRadians=0
        self.area=0
        self.length=self.length()
        self.units="mm"

    def distance(self, p1, p2):
        return math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2)

    def radius(self):
        a = self.distance(self.startPoint, self.midPoint)
        b = self.distance(self.midPoint, self.endPoint)
        c = self.distance(self.endPoint, self.startPoint)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s-a) * (s-b) * (s-c))
        R = (a * b * c) / (4 * A)
        return R

    def length(self):
        x1, y1, z1 = self.startPoint.x, self.startPoint.y, self.startPoint.z
        x2, y2, z2 = self.midPoint.x, self.midPoint.y, self.midPoint.z
        x3, y3, z3 = self.endPoint.x, self.endPoint.y, self.endPoint.z

        r1 = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5 / 2
        a = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
        b = math.sqrt((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)
        c = math.sqrt((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)
        cos_hoek = (a**2 + b**2 - c**2) / (2*a*b)
        m1 = math.acos(cos_hoek)
        arc_length = r1 * m1

        return arc_length

    def __str__(self) -> str:
        return f"{__class__.__name__}(Object output n.t.b.)"


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

