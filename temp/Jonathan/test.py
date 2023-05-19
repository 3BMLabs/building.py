import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2d import *
from abstract.plane import Plane
from abstract.text import Text
from abstract.intersect2d import Intersect2d
from objects.datum import *
from geometry.solid import Extrusion
from objects.panel import Panel
from abstract.color import Color
from geometry.surface import Surface

Point1 = Point(1500,-3500,0)
Point2 = Point(6900,5000,0)
Point3 = Point(3420,5000,0)
Point4 = Point(0,0,0)
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1])
Point5 = Point(400,0,0)
Point6 = Point(1200,400,0)
Point7 = Point(350,400,0)
Point8 = Point(300,30,0)
ply2 = PolyCurve.byPoints([Point5, Point6, Point7, Point8, Point5])
# obj = [ply1, ply2]



# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]

Point1 = Point(1500,0,0)
Point2 = Point(6900,1000,0)
Point3 = Point(0,1000,0)
Point4 = Point(0,0,0)
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1])

# srf1 = Surface([ply1, ply2])
l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))
# obj.append(srf1)
obj = [ply1]


f1 = Intersect2d().getIntersectLinePolyCurve(ply1, l3, split=True)

for ff in f1: #points
    obj.append(ff)

# i1 = l3.split(ply1)
# for ff in i1:
#     obj.append(ff)

# startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
# startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))
# obj = [ply1]

# gridLines = []
# for xRange in range(50):
#     vector1 = Vector3(0, 600*(xRange+1), 0)
#     vector2 = Vector3(600*(xRange+1), 0, 0)
#     gridLines.append(Line.offset(startLinexAxis, vector1))
#     gridLines.append(Line.offset(startLineyAxis, vector2))

# insect = Intersect2d().getLineIntersectPolyCurve(ply1, gridLines, split=True)

# for innie1 in insect[1]:
#     for z in innie1:
#         obj.append(z)

# for grid in gridLines: #shows grid lines
#     obj.append(grid)
# obj.append(startLinexAxis)
# obj.append(startLineyAxis)

SpeckleHost = "3bm.exchange"
StreamID = "5ab2faedba"
SpeckleObjects = obj
Message = "x"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)