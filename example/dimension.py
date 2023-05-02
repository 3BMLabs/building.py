#Line to polycurve. return intersects

# line to polycurve intersect
# line to surface intersect
# divide surfaces


import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import PolyCurve, Line
from abstract.vector import Vector3
from abstract.intersect2 import *


p1 = Point(5,5,4)
q1 = Point(10,10,6)
p2 = Point(5,5,5)
q2 = Point(10,10,3)




lx2 = Line(p1, q1)
lx3 = Line(p2, q2)
intersection_point = Intersect().getIntersect(lx2, lx3)


obj = [lx2, lx3, intersection_point]


SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "Shiny commit 170"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)