# from svg.path import parse_path
# from typing import List, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


# from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
# from abstract.vector import Vector3
# from abstract.intersect2d import *
# from abstract.plane import Plane
# from abstract.text import Text
# from abstract.intersect2d import Intersect2d
# from objects.datum import *
# from geometry.solid import Extrusion
# from geometry.surface import *
# from math import fabs

l = Line(Point(0, 0, 0), Point(1, 250, 0))
print(l.length)
a = Arc(Point(10,20,30), Point(10,1,30), Point(10,20,2))
print(a.length)

Point1 = Point(1500,-4030,0) #b
Point2 = Point(6900,5000,0) #b
Point3 = Point(0,10000,0) #x
Point4 = Point(0,0,0) #x
Point5 = Point(-2900,1600,0) #x
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])
ply1.length
# print()