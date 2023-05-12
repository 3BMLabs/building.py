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

# f1 = Intersect2d().getIntersectPoint(l1, l2)

# obj = [l1, l2, f1]





Point1 = Point(1500,0,0)

Point2 = Point(6900,1000,0)

Point3 = Point(0,1000,0)

Point4 = Point(0,0,0)

ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1])

z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)




l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))

obj = [ply1, z]




startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))

startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))

obj = [ply1]




gridLines = []

for xRange in range(50):

    vector1 = Vector3(0, 600*(xRange+1), 0)

    vector2 = Vector3(600*(xRange+1), 0, 0)

    gridLines.append(Line.offset(startLinexAxis, vector1))

    gridLines.append(Line.offset(startLineyAxis, vector2))


# Intersctline  = Line(start=Point(2580,200,0), end=Point(-10000,200,0))
Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))

# centerpoint = Intersctline1.pointOnIntverval(0)
# obj.append(centerpoint)

insect = Intersect2d().getIntersectPointPolyCurve(ply1, Intersctline1, split=True)


for pt in insect["IntersectPoints"]:
    obj.append(pt)


for ln in insect["IntersectLines"]:
    for l in ln:
        print(l)
        obj.append(l)




# for grid in gridLines: #shows grid lines
#     obj.append(grid)

# obj.append(startLinexAxis)

# obj.append(startLineyAxis)





SpeckleHost = "3bm.exchange"

StreamID = "fa4e56aed4"

SpeckleObjects = obj

Message = "x"

SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)