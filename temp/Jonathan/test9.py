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
from objects.objectcollection import *
from project.fileformat import *
from objects.shape3d import Origin
from exchange.DXF import ReadDXF

#finish
# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]


# Point1 = Point(1500,-4030,0) #b
# Point2 = Point(6900,5000,0) #b
# Point3 = Point(0,10000,0) #x
# Point4 = Point(-1000,4000,0) #x
# Point5 = Point(-2900,1600,0) #x
# ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])
# z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)

# arrow = ReadDXF("library/object_database/DXF/Arrow.dxf")
# arrowShape = ReadDXF.create_polycurve(arrow)
# print(arrowShape.points)
# project.objects.append(arrowShape)

# floor = ReadDXF("library/object_database/DXF/customfloor.dxf")
# floorShape = ReadDXF.create_polycurve(floor)
# for fshape in floorShape:
#     project.objects.append(fshape)

# l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))

# startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
# startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))

# part1 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(400.0,-2622.5,0), Point(1500,-4030,0), Point(6900,5000,0), Point(400.0,9710.144927536232,0)])
# part2 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(0,10000,0), Point(0,0,0), Point(-2900,1600,0), Point(400.0,-2622.5,0), Point(400.0,9710.144927536232,0)])


# gridLines = []
# for xRange in range(50):
#     vector1 = Vector3(0, 600*(xRange+1), 0)
#     vector2 = Vector3(600*(xRange+1), 0, 0)
#     gridLines.append(Line.offset(startLinexAxis, vector1))
#     gridLines.append(Line.offset(startLineyAxis, vector2))

# Intersctline  = Line(start=Point(5000,-200,0), end=Point(-10000,-200,0))
# Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))
# Intersctline2 = Line(start=Point(400,-4000,0), end=Point(400,12000,0))
# lns = [Intersctline, Intersctline2]


# insect = Intersect2d().getIntersectLinePolyCurve(ply1, gridLines, split=True, stretch=False) #stretch


# j = Intersect2d().getMultiLineIntersect(insect["InnerGridLines"])

part1 = Arc(startPoint = Point(50,3000,0), endPoint = Point(0,3100,0))
project.objects.append(part1)
project.objects.append(Line(start=Point(2000,0,0), end=Point(0,3000,0)))
# project.objects.append(Line(start=Point(0,0,0), end=Point(0,3000,0)))
project.objects.append(Point(0,0,0))
project.objects.append(Point(0,3100,0))


project.toSpeckle("5ab2faedba")