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
from packages.helper import *
from abstract.interval import Interval

class Line: #add Line.bylenght (start and endpoint)
    def __init__(self, start: Point, end: Point, id=helper.generateID()) -> None:
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

    def offset(line, vector):
        start = Point(line.start.x + vector.x, line.start.y + vector.y, line.start.z + vector.z)
        end = Point(line.end.x + vector.x, line.end.y + vector.y, line.end.z + vector.z)
        return Line(start=start, end=end)

    def pointOnIntverval(self, interval=None):
        if interval == None:
            interval = 0.0

        x1, y1, z1 = self.start.x, self.start.y, self.start.z
        x2, y2, z2 = self.end.x, self.end.y, self.end.z
        if float(interval) == 0.0:
            return self.start
        else:
            devBy = 1/interval
            return Point((x1 + x2) / devBy, (y1 + y2) / devBy, (z1 + z2) / devBy)
        

    def split(self, points: list[Point]):
        lines = []
        if type(points) == list:
            print(points)
            # for index, p in enumerate(range(len(points)+1)):
            #     if index == 0:
            #         lines.append(Line(start=self.start, end=points[index-1]))
            #     elif index == len(points):
            #         lines.append(Line(start=points[index-2], end=self.end))
            #     else:
            #         lines.append(Line(start=points[index], end=points[index-1]))

        elif type(points) == Point:
            point = points
            lines.append(Line(start=self.start, end=point))
            lines.append(Line(start=point, end=self.end))
        return lines

    def length(self):
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy) + self.dz * self.dz)

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.start},{self.end})"


class PolyCurve:
    def __init__(self, points=None, id=helper.generateID()):
        self.curves = []
        self.points = points or []
        self.segmentcurves = None
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
    def generate_lines(cls):
        # print(cls)
        print(cls.points)

        # lines = []
        # for i in range(len(self.points) - 1):
        #     print(Line(self.points[i], self.points[i+1]))
        #     lines.append(Line(self.points[i], self.points[i+1]))
        # return lines

    @staticmethod
    def segment(cls, count):
        #Create segmented polycurve. Arcs, elips will be translated to straight lines
        crvs = []
        for i in cls.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc.segmentedarc(i, count))
            elif i.__class__.__name__ == "Line":
                crvs.append(i)
        crv = flatten(crvs)
        pc = PolyCurve.byJoinedCurves(crv)
        return pc

    @staticmethod
    def byPolyCurve2D(PolyCurve2D):
        # by points,
        p1 = PolyCurve()
        count = 0
        curves = []
        for i in PolyCurve2D.curves:
            if i.__class__.__name__ == "Arc2D":
                curves.append(Arc(Point(i.start.x, i.start.y, 0), Point(i.mid.x, i.mid.y, 0), Point(i.end.x, i.end.y, 0)))
            elif i.__class__.__name__ == "Line2D":
                curves.append(Line(Point(i.start.x, i.start.y,0),Point(i.end.x, i.end.y,0)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        p1.points = pnts
        p1.curves = curves
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
        crv = flatten()
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

    def toPolyCurve2D(self):
        # by points,
        from geometry.geometry2d import PolyCurve2D
        from geometry.geometry2d import Point2D
        from geometry.geometry2d import Line2D
        from geometry.geometry2d import Arc2D

        p1 = PolyCurve2D()
        count = 0
        curves = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                curves.append(Arc2D(Point2D(i.start.x, i.start.y), Point2D(i.middle.x, i.middle.y),
                                  Point2D(i.end.x, i.end.y)))
            elif i.__class__.__name__ == "Line":
                curves.append(Line2D(Point2D(i.start.x, i.start.y), Point2D(i.end.x, i.end.y)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        p1.points = pnts
        p1.curves = curves
        return p1
    def __id__(self):
        return f"id:{self.id}"

    def __str__(self):
        PolyCurveName = f"{__class__.__name__}("
#       for i in self.curves:
#            PolyCurveName = PolyCurveName + i
        return PolyCurveName + ")"

# 2D PolyCurve to 3D PolyGon

def Rect(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane with translation of vector
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



class PolyGon:
    def __init__(self, lines, id=helper.generateID()) -> None:
        self.Lines = lines#collect in list
        self.id = id
        pass #Lines
    
    @staticmethod
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


    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Arc:
    def __init__(self, startPoint: Point, midPoint: Point, endPoint: Point):
        self.start = startPoint
        self.mid = midPoint
        self.end = endPoint
        self.origin = self.originarc()
        v1=Vector3(x=1, y=0, z=0)
        v2=Vector3(x=0, y=1, z=0)
        self.plane = Plane.byTwoVectorsOrigin(
            v1, 
            v2, 
            Point((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2)
        )
        self.radius = self.radiusarc()
        self.startAngle=0
        self.endAngle=0
        self.angleRadian = self.angleRadian()
        self.area=0
        self.length = self.length()
        self.units="mm"
        self.coordinatesystem = self.coordinatesystemarc()

    def distance(self, p1, p2):
        return math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2)

    def coordinatesystemarc(self):
        vx = Vector3.byTwoPoints(self.origin, self.start)  # Local X-axe
        v2 = Vector3.byTwoPoints(self.end, self.origin)
        vz = Vector3.crossProduct(vx, v2)  # Local Z-axe
        vy = Vector3.crossProduct(vx, vz)  # Local Y-axe
        self.coordinatesystem = CoordinateSystem(self.origin, Vector3.normalise(vx), Vector3.normalise(vy), Vector3.normalise(vz))
        return self.coordinatesystem

    def radiusarc(self):
        a = self.distance(self.start, self.mid)
        b = self.distance(self.mid, self.end)
        c = self.distance(self.end, self.start)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s-a) * (s-b) * (s-c))
        R = (a * b * c) / (4 * A)
        return R

    def originarc(self):
        #calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector3.byTwoPoints(self.start, self.end)
        halfVstartend = Vector3.scale(Vstartend,0.5)
        b = 0.5 * Vector3.length(Vstartend) #half distance between start and end
        x = math.sqrt(Arc.radiusarc(self) * Arc.radiusarc(self) - b * b) #distance from start-end line to origin
        mid = Point.translate(self.start, halfVstartend)
        v2 = Vector3.byTwoPoints(self.mid, mid)
        v3 = Vector3.normalise(v2)
        tocenter = Vector3.scale(v3,x)
        center = Point.translate(mid, tocenter)
        #self.origin = center
        return center

    def angleRadian(self):
        v1 = Vector3.byTwoPoints(self.origin, self.end)
        v2 = Vector3.byTwoPoints(self.origin, self.start)
        angle = Vector3.angleRadianBetween(v1,v2)
        return angle
    def length(self):
        x1, y1, z1 = self.start.x, self.start.y, self.start.z
        x2, y2, z2 = self.mid.x, self.mid.y, self.mid.z
        x3, y3, z3 = self.end.x, self.end.y, self.end.z

        r1 = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5 / 2
        a = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
        b = math.sqrt((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)
        c = math.sqrt((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)
        cos_angle = (a**2 + b**2 - c**2) / (2*a*b)
        m1 = math.acos(cos_angle)
        arc_length = r1 * m1

        return arc_length

    @staticmethod
    def pointsAtParameter(arc, count: int):
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angleRadian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point(arc.radius * math.cos(alpha), arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        CSNew = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transformPoint2(i, CSNew))
        return pnts2

    @staticmethod
    def segmentedarc(arc, count):
        pnts = Arc.pointsAtParameter(arc,count)
        i = 0
        lines = []
        for j in range(len(pnts)-1):
            lines.append(Line(pnts[i],pnts[i+1]))
            i = i + 1
        return lines

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

