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
from geometry.point import Point, Point2D
from geometry.curve import PolyCurve, Line
from abstract.vector import Vector3


v10 = Vector3(-500, 500, 0)
v20 = Vector3(1500, 500, 0)
LineX = Vector3.toLine(v10, v20)

Point1 = Point(0, 0, 0)
Point2 = Point(0, 1000, 0)
Point3 = Point(1000, 1000, 0)
Point4 = Point(1000, 0, 0)

Ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1])


# p1 = Point(-500, 500, 0)
# p2 = Point(1500, 500, 0)
# l1 = Line(start=p1, end=p2)

# p3 = Point(1000, 1000, 0)
# p4 = Point(1000, 0, 0)
# l2 = Line(start=p3, end=p4)



from abstract.intersect import *
# p1 = Point2D(10, 10)
# q1 = Point2D(100, 10)
# p2 = Point2D(10, 20)
# q2 = Point2D(100, 20)
# Ply1 = PolyCurve.byPoints([p1, q1, p2, q2])
# if doIntersect(p1, q1, p2, q2):
# 	print("Yes")
# else:
# 	print("No")

# p1 = Point2D(1000, 0)
# q1 = Point2D(0, 1000)
# p2 = Point2D(0, 0)
# q2 = Point2D(1000,1000)


p1 = Point(1000, 0, 0)
q1 = Point(0, 1000, 0)
p2 = Point(0, 0, 0)
q2 = Point(1000,1000, 0)

lx2 = Line(p1, q1)
lx3 = Line(p2, q2)
intersection_point = Intersect().getIntersect(lx2, lx3)


# dointersect = Intersect().doIntersect(lx2, lx3)

# print(dointersect)
print(intersection_point)

# p3 = intersection_point


# intersection_point = Intersect().doIntersect(lx2, lx3)

# if doIntersect(p1, q1, p2, q2):
# 	print("Yes")
# else:
# 	print("No")

# getIntersect(p1, q1, p2, q2)

# p1 = Point2D(-50,-50)
# q1 = Point2D(0, 0)
# p2 = Point2D(10, 10)
# q2 = Point2D(100, 100)
# Ply3 = PolyCurve.byPoints([p1, q1, p2, q2, p1])

# if doIntersect(p1, q1, p2, q2):
# 	print("Yes")
# else:
# 	print("No")


obj = [lx2, lx3, intersection_point]
# obj = [Ply1, Ply2, Ply3]

SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "Shiny commit 170"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)