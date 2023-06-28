import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path


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


#finish
# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]


Point1 = Point(1500,-4030,0)
Point2 = Point(6900,5000,0)
Point3 = Point(0,10000,0)
Point4 = Point(0,0,0)
Point5 = Point(-2900,1600,0)
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])
z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)




l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))

# obj = [ply1, z]




startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))

obj = [ply1]




gridLines = []

for xRange in range(50):
    vector1 = Vector3(0, 600*(xRange+1), 0)
    vector2 = Vector3(600*(xRange+1), 0, 0)
    gridLines.append(Line.offset(startLinexAxis, vector1))
    gridLines.append(Line.offset(startLineyAxis, vector2))

Intersctline  = Line(start=Point(2900,200,0), end=Point(-10000,200,0))
# Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))
Intersctline2 = Line(start=Point(200,-1000,0), end=Point(200,10000,0))
lns = [Intersctline, Intersctline2]

# centerpoint = Intersctline1.pointOnIntverval(0)
# obj.append(centerpoint)

insect = Intersect2d().getIntersectLinePolyCurve(ply1, gridLines, split=True, stretch=True) #stretch
print(insect)
# obj.append(Intersctline1)


for pt in insect["IntersectGridPoints"]:
    obj.append(pt)

# for ln in insect["SplittedLines"]:
#     for l in ln:
#         obj.append(l)


for pt in insect["InnerGridLines"]:
    obj.append(pt)


# sys.exit()


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