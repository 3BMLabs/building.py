import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from abstract.boundingbox import BoundingBox2d, BoundingBox3d
from geometry.curve import PolyCurve


p1 = Point(x=900, y=0, z=0)
p2 = Point(x=20, y=500, z=30)
p3 = Point(x=400, y=410, z=160)
p4 = Point(x=650, y=800, z=0)
obj = [p1,p2,p3,p4]


# bb = BoundingBox2d(points=[p1,p2,p3,p4]).perimeter()
bb = BoundingBox3d(points=[p1,p2,p3,p4]).perimeter()


obj.append(bb)


SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "fa4e56aed4"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"


SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)