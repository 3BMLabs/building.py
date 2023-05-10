#Line to polycurve. return intersects

# line to polycurve intersect
# line to surface intersect
# divide surfaces


import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2 import *
from abstract.plane import Plane
from abstract.text import Text

p001 = Point(0,0,0)
p002 = Point(1000,1000,0)
p003 = Point(500,500,10)

print(Vector3.angleRadianBetween(p002, p001))
cp = Point.origin(p001, p002)

i = Point(cp.x, cp.y, cp.z)

p1 = Point(30,10,0)
p2 = Point(10,0,0)
p3 = Point(130,5000,0)
p4 = Point(20,20,0)

dimLine = Line(p001, p002)
len = round(dimLine.length(), 2)

plane1 = Plane.byTwoVectorsOrigin(
    p1, p2, Point.origin(p1, p2)
)

pvector = Point.toVector(p2)
calcAngle = Vector3.angleBetween(pvector, p1)
print(calcAngle)
#tekst er haaks op zetten
Text1 = Text(text=str(len), xyz=Point(200,10,20), rotation=45)

# print(p1, Point.origin(p1,p2), p2)

arcy = Arc(p001, p003, p002)

# print(calcAngle)
#2 lines er haaks op.
#2 circles
#test along the line



obj = [p1, p2, dimLine, plane1, Text1]


SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "Shiny commit 170"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)