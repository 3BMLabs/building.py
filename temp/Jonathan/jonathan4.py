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

#finish
# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]


Point1 = Point(1500,-4030,0) #b
Point2 = Point(6900,5000,0) #b
Point3 = Point(0,10000,0) #x
Point4 = Point(0,0,0) #x
Point5 = Point(-2900,1600,0) #x
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])
z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)






l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))


startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))

part1 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(400.0,-2622.5,0), Point(1500,-4030,0), Point(6900,5000,0), Point(400.0,9710.144927536232,0)])
part2 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(0,10000,0), Point(0,0,0), Point(-2900,1600,0), Point(400.0,-2622.5,0), Point(400.0,9710.144927536232,0)])


obj = []

# obj = [ply1]
# obj = [part2, part1]

gridLines = []
# sys.exit()
for xRange in range(50):
    vector1 = Vector3(0, 600*(xRange+1), 0)
    vector2 = Vector3(600*(xRange+1), 0, 0)
    gridLines.append(Line.offset(startLinexAxis, vector1))
    gridLines.append(Line.offset(startLineyAxis, vector2))

Intersctline  = Line(start=Point(5000,-200,0), end=Point(-10000,-200,0))
# Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))
Intersctline2 = Line(start=Point(400,-4000,0), end=Point(400,12000,0))
lns = [Intersctline, Intersctline2]


insect = Intersect2d().getIntersectLinePolyCurve(ply1, Intersctline2, split=True, stretch=False) #stretch


st = insect["InnerGridLines"][0].start #Point(400.0,9710.144927536232,0)
en = insect["InnerGridLines"][0].end #Point(400.0,-2622.5,0)


i1 = None
i2 = None

list1 = []
list2 = []


for index, i in enumerate(ply1.curves):
    if is_point_on_line_segment(st, i) == True:
        i1 = index
    if is_point_on_line_segment(en, i) == True:
        i2 = index


for x in range(i1,(i2)):
    list1.append(x)

for p in range(i2,len(ply1.curves)):
    list2.append(p)

for a in range(0,i1):
    list2.append(a)


part1 = [st, en]
for x1 in list2:
    if ply1.curves[x1].end not in part1:
        part1.append(ply1.curves[x1].end)
part1.append(st)

part2 = [st]
for x1 in list1:
    if ply1.curves[x1].end not in part2:
        part2.append(ply1.curves[x1].end)
part2.append(en)
part2.append(st)

plyl1 = PolyCurve.byPoints(part1)
obj.append(Surface([plyl1]))
obj.append(plyl1)

plyl2 = PolyCurve.byPoints(part2)
obj.append(Surface([plyl2]))
obj.append(plyl2)



for pt in insect["IntersectGridPoints"]:
    obj.append(pt)



SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "x"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)