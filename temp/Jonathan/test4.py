import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
# https://help.xtools.pro/pro/22.0/en/XTools_Pro_Components/Geometry_Tools/Split_Polygons.htm

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
from geometry.surface import *
from project.fileformat import *

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

# Point1 = Point(0,0,0)
# Point2 = Point(0,8000,0)
# Point3 = Point(3000,11000,0)
# Point4 = Point(5000,4000,0)
# Point5 = Point(5000,0,0)
# Point6 = Point(3000,0,0)
# Point7 = Point(3000,3000,0)
# Point8 = Point(1000,3000,0)
# Point9 = Point(1000,0,0)
# ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point6, Point7, Point8, Point9])

z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)
# project.objects.append(ply1)


l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))


startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))

part1 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(400.0,-2622.5,0), Point(1500,-4030,0), Point(6900,5000,0), Point(400.0,9710.144927536232,0)])
part2 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(0,10000,0), Point(0,0,0), Point(-2900,1600,0), Point(400.0,-2622.5,0), Point(400.0,9710.144927536232,0)])


gridLines = []
for xRange in range(50):
    vector1 = Vector3(0, 600*(xRange+1), 0)
    vector2 = Vector3(600*(xRange+1), 0, 0)
    gridLines.append(Line.offset(startLinexAxis, vector1))
    gridLines.append(Line.offset(startLineyAxis, vector2))

Intersctline  = Line(start=Point(5000,-200,0), end=Point(-10000,5000,0))
Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))
Intersctline2 = Line(start=Point(400,-4000,0), end=Point(400,12000,0))
Intersctline3  = Line(start=Point(8000,4000,0), end=Point(-10000,4500,0))

# for gl in flatten(gridLines):
#     project.objects.append(gl)

# lns = [Intersctline, Intersctline2]
lns = [Intersctline, Intersctline2, Intersctline3]

# project.objects.append(Intersctline)
# project.objects.append(Intersctline2)
# project.objects.append(Intersctline3)

# ply1.split(Intersctline3)

# project.objects.append(ply1)
singleLineSplit = Intersect2d().getIntersectLinePolyCurve(ply1, lns, split=True, stretch=False)
singleLineSplit = singleLineSplit["InnerGridLines"]

# innergridlines = Intersect2d().getIntersectLinePolyCurve(ply1, gridLines, split=True, stretch=False)
# innergridlines = innergridlines["InnerGridLines"]

for x in singleLineSplit:
    project.objects.append(x)
project.objects.append(ply1)

splitted = ply1.multi_split(lns)

for x in splitted:
    project.objects.append(Surface(x))


project.toSpeckle("5ab2faedba")