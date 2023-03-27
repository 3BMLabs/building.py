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


"""This module provides tools to create 2D profiles 
"""

__title__= "geometry2d"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/geometry2d.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from packages import helper

class curve:
#Line2D, etc moet van class curve zijn. start end
    pass

class Vector2:
    def __init__(self, x, y, id=helper.generateID()) -> None:
        self.X: float = 0.0
        self.Y: float = 0.0
        self.X = x
        self.Y = y
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.X},{self.Y})"

class Point2D:
    def __init__(self, x, y, id=helper.generateID()) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y
        self.id = id

    def __id__(self):
        return f"id:{self.id}"
    def translate(self, vector: Vector2):
        x = self.x + vector.X
        y = self.y + vector.Y
        p1 = Point2D(x, y)
        return p1

    def rotate(self, rotation):
        x = self.x
        y = self.y
        r = math.sqrt(x * x + y * y)
        rotationstart = math.degrees(math.atan2(y, x))
        rotationtot = rotationstart + rotation
        xn = round(math.cos(math.radians(rotationtot)) * r,3)
        yn = round(math.sin(math.radians(rotationtot)) * r,3)
        p1 = Point2D(xn, yn)
        return p1

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.x},{self.y})"

class Line2D:
    def __init__(self, pntxy1, pntxy2, id=helper.generateID()) -> None:
        self.start: Point2D = pntxy1
        self.end: Point2D = pntxy2
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        self.dx = self.start.x-self.end.x
        self.dy = self.start.y-self.end.y
        self.length = 0
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    def length(self):
        self.length = math.sqrt(self.dx*self.dx+self.dy*self.dy)
        return self.length

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.start},{self.end})"


class Arc2D:
    def __init__(self,pntxy1,pntxy2,pntxy3, id=helper.generateID()) -> None:
        self.start:Point2D = pntxy1
        self.middle: Point2D = pntxy2
        self.end: Point2D = pntxy3
        #self.radius
        #self.length
        #self.origin
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    def points(self):
        #returns point on the curve
        return (self.start, self.middle, self.end)

    def __str__(self):
        return f"{__class__.__name__}({self.start},{self.middle},{self.end})"


class PolyCurve2D:
    def __init__(self, id=helper.generateID()) -> None:
        self.curves = [] #collect in list
        self.points2D = []
        self.id = id

    def __id__(self):
        return f"id:{self.id}"

    @classmethod
    def byJoinedCurves(cls, curves):
        pc = PolyCurve2D()
        for i in curves:
            pc.curves.append(i)
        return pc

    def points(self):
        for i in self.curves:
            self.points2D.append(i.start)
            self.points2D.append(i.end)
        return self.points2D

    def translate(self, vector2d:Vector2):
        crvs = []
        v1 = vector2d
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.translate(v1), i.middle.translate(v1), i.end.translate(v1)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.translate(v1), i.end.translate(v1)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.byJoinedCurves(crvs)
        return crv

    def rotate(self, rotation):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.rotate(rotation), i.middle.rotate(rotation), i.end.rotate(rotation)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.rotate(rotation), i.end.rotate(rotation)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.byJoinedCurves(crvs)
        return crv

    @staticmethod
    def polygon(self):
        points = []
        for i in self.curves:
            if i == Arc2D:
                points.append(i.start,i.middle)
            else:
                points.append(i.start)
        points.append(points[0])
        return points

 #   def __str__(self) -> str:
#        return f"{__class__.__name__}({self})"


class Surface2D:
    def __init__(self, id=helper.generateID()) -> None:
        pass #PolyCurve2D
        self.id = id
    pass #opening(PolyCurve2D)
        
    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Profile2D:
    def __init__(self, id=helper.generateID()) -> None:
        pass #Surface2D, collect curves and add parameters
        self.id = id
    #voorzien van parameters
    #gebruiken voor objecten(kanaalplaatvloer, HEA200, iets)
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class ParametricProfile2D:
    def __init__(self, id=helper.generateID()) -> None:
        pass #iets van profile hier inladen
        self.id = id
    # Aluminium
    # Generic
    # Precast Concrete
    # ParametricProfile2D
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"