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
from abstract.vector import Vector3
from abstract.coordinatesystem import CoordinateSystem

class curve:
#Line2D, etc moet van class curve zijn. start end
    pass

class Vector2:
    def __init__(self, x, y) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y
        self.id = helper.generateID()

    @staticmethod
    def byTwoPoints(p1, p2):
        return Vector2(
            p2.x-p1.x,
            p2.y-p1.y
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.x * v1.x + v1.y * v1.y)

    @staticmethod
    def scale(v1, scalefactor):
        return Vector2(
            v1.x * scalefactor,
            v1.y * scalefactor
        )

    @staticmethod
    def normalize(v1):
        scale = 1/Vector2.length(v1)
        return Vector2(
            v1.x*scale,
            v1.y*scale
        )

    @staticmethod #inwendig product, if zero, then vectors are perpendicular
    def dotProduct(v1, v2):
        return v1.x*v2.x+v1.y*v2.y

    @staticmethod
    def angleBetween(v1, v2):
        return math.degrees(math.acos((Vector2.dotProduct(v1, v2)/(Vector2.length(v1) * Vector2.length(v2)))))

    @staticmethod
    def angleRadianBetween(v1, v2):
        return math.acos((Vector2.dotProduct(v1, v2)/(Vector2.length(v1) * Vector2.length(v2))))

    @staticmethod #Returns vector perpendicular on the two vectors
    def crossProduct(v1, v2):
        return Vector3(
            v1.y - v2.y,
            v2.x - v1.x,
            v1.x*v2.y - v1.y*v2.x
        )

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self.X},{self.Y})"

class Point2D:
    def __init__(self, x, y) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y
        self.id = helper.generateID()

    def __id__(self):
        return f"id:{self.id}"
    
    def translate(self, vector: Vector2):
        x = self.x + vector.x
        y = self.y + vector.y
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

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    @staticmethod
    def midpoint(point1, point2):
        return Point2D((point2.x-point1.x)/2, (point2.y-point1.y)/2)

    @staticmethod
    def toPixel(point1, Xmin, Ymin, TotalWidth, TotalHeight, ImgWidthPix: int, ImgHeightPix: int):
      # Convert Point to pixel on a image given a deltaX, deltaY, Width of the image etc.
      x = point1.x
      y = point1.y
      xpix = math.floor(((x - Xmin) / TotalWidth) * ImgWidthPix)
      ypix = ImgHeightPix-math.floor(((y - Ymin) / TotalHeight) * ImgHeightPix) # min vanwege coord stelsel Image.Draw
      return xpix, ypix

def transformPoint2D(PointLocal1: Point2D, CoordinateSystemNew: CoordinateSystem):
    # Transform point from Global Coordinatesystem to a new Coordinatesystem
    # CSold = CSGlobal
    from abstract.vector import Vector3
    from geometry.point import Point
    PointLocal = Point(PointLocal1.x, PointLocal1.y, 0)
    pn = Point.translate(CoordinateSystemNew.Origin, Vector3.scale(CoordinateSystemNew.Xaxis, PointLocal.x))
    pn2 = Point.translate(pn, Vector3.scale(CoordinateSystemNew.Yaxis, PointLocal.y))
    pn3 = Point2D(pn.x,pn.y)
    return pn3

class Line2D:
    def __init__(self, pntxy1, pntxy2) -> None:
        self.start: Point2D = pntxy1
        self.end: Point2D = pntxy2
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        self.dx = self.start.x-self.end.x
        self.dy = self.start.y-self.end.y
        self.length = 0
        self.id = helper.generateID()

    def __id__(self):
        return f"id:{self.id}"

    def length(self):
        self.length = math.sqrt(self.dx*self.dx+self.dy*self.dy)
        return self.length

    def fline(self):
        #returns line for Folium(GIS)
        return [[self.start.y,self.start.x],[self.end.y,self.end.x]]
    def __str__(self) -> str:
        return f"{__class__.__name__}({self.start},{self.end})"


class Arc2D:
    def __init__(self,pntxy1,pntxy2,pntxy3) -> None:
        self.start:Point2D = pntxy1
        self.mid: Point2D = pntxy2
        self.end: Point2D = pntxy3
        self.origin = self.originarc()
        self.angleRadian = self.angleRadian()
        self.radius = self.radiusarc()
        self.coordinatesystem = self.coordinatesystemarc()
        #self.length

        self.id = helper.generateID()

    def __id__(self):
        return f"id:{self.id}"

    def points(self):
        #returns point on the curve
        return (self.start, self.mid, self.end)

    def coordinatesystemarc(self):
        vx2d = Vector2.byTwoPoints(self.origin, self.start)  # Local X-axe
        vx = Vector3(vx2d.x, vx2d.y, 0)
        vy = Vector3(vx.y, vx.x * -1,0)
        vz = Vector3(0,0,1)
        self.coordinatesystem = CoordinateSystem(self.origin, Vector3.normalize(vx), Vector3.normalize(vy), Vector3.normalize(vz))
        return self.coordinatesystem

    def angleRadian(self):
        v1 = Vector2.byTwoPoints(self.origin, self.end)
        v2 = Vector2.byTwoPoints(self.origin, self.start)
        angle = Vector2.angleRadianBetween(v1,v2)
        return angle

    def originarc(self):
        #calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector2.byTwoPoints(self.start, self.end)
        halfVstartend = Vector2.scale(Vstartend,0.5)
        b = 0.5 * Vector2.length(Vstartend) #half distance between start and end
        x = math.sqrt(Arc2D.radiusarc(self) * Arc2D.radiusarc(self) - b * b) #distance from start-end line to origin
        mid = Point2D.translate(self.start, halfVstartend)
        v2 = Vector2.byTwoPoints(self.mid, mid)
        v3 = Vector2.normalize(v2)
        tocenter = Vector2.scale(v3, x)
        center = Point2D.translate(mid, tocenter)
        #self.origin = center
        return center

    def radiusarc(self):
        a = Vector2.length(Vector2.byTwoPoints(self.start, self.mid))
        b = Vector2.length(Vector2.byTwoPoints(self.mid, self.end))
        c = Vector2.length(Vector2.byTwoPoints(self.end, self.start))
        s = (a + b + c) / 2
        A = math.sqrt(s * (s-a) * (s-b) * (s-c))
        R = (a * b * c) / (4 * A)
        return R


    @staticmethod
    def pointsAtParameter(arc, count: int):
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angleRadian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point2D(arc.radius * math.cos(alpha), arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        CSNew = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transformPoint2D(i, CSNew))
        return pnts2

    @staticmethod
    def segmentedarc(arc, count):
        pnts = Arc2D.pointsAtParameter(arc,count)
        i = 0
        lines = []
        for j in range(len(pnts)-1):
            lines.append(Line2D(pnts[i],pnts[i+1]))
            i = i + 1
        return lines

    def __str__(self):
        return f"{__class__.__name__}({self.start},{self.mid},{self.end})"


class PolyCurve2D:
    def __init__(self) -> None:
        self.curves = [] #collect in list
        self.points2D = []
        self.id = helper.generateID()

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

    @classmethod
    def byPoints(self, points: list):
        plycrv = PolyCurve2D()
        for index, point2D in enumerate(points):
            plycrv.points2D.append(point2D)
            try:
                nextpoint = points[index + 1]
                plycrv.curves.append(Line2D(point2D, nextpoint))
            except:
                firstpoint = points[0]
                plycrv.curves.append(Line2D(point2D, firstpoint))
        return plycrv

    def translate(self, vector2d:Vector2):
        crvs = []
        v1 = vector2d
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.translate(v1), i.mid.translate(v1), i.end.translate(v1)))
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
                crvs.append(Arc2D(i.start.rotate(rotation), i.mid.rotate(rotation), i.end.rotate(rotation)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.rotate(rotation), i.end.rotate(rotation)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.byJoinedCurves(crvs)
        return crv

    @staticmethod
    def boundingboxGlobalCS(PC):
        x =[]
        y =[]
        for i in PC.points():
            x.append(i.x)
            y.append(i.y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        bbox = PolyCurve2D.byPoints([Point2D(xmin,ymin),Point2D(xmax,ymin),Point2D(xmax,ymax),Point2D(xmin,ymax),Point2D(xmin,ymin)])
        return bbox

    @staticmethod
    def polygon(self):
        points = []
        for i in self.curves:
            if i == Arc2D:
                points.append(i.start, i.mid) #
            else:
                points.append(i.start)
        points.append(points[0])
        return points

 #   def __str__(self) -> str:
#        return f"{__class__.__name__}({self})"


class Surface2D:
    def __init__(self) -> None:
        pass #PolyCurve2D
        self.id = helper.generateID()
    pass #opening(PolyCurve2D)
        
    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Profile2D:
    def __init__(self) -> None:
        pass #Surface2D, collect curves and add parameters
        self.id = helper.generateID()
    #voorzien van parameters
    #gebruiken voor objecten(kanaalplaatvloer, HEA200, iets)
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class ParametricProfile2D:
    def __init__(self) -> None:
        pass #iets van profile hier inladen
        self.id = helper.generateID()
    # Aluminium
    # Generic
    # Precast Concrete
    # ParametricProfile2D
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"