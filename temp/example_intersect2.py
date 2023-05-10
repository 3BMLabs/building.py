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


l1 = Line(start=Point(230,-1000,0), end=Point(0,1000,0))
l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))

p1 = Intersect2d().getIntersectPoint(l1, l2)

obj = [l1, l2, p1]

SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "x"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)