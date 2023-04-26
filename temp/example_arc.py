import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects

from geometry.point import Point as Point
from abstract.vector import Vector3 as Vector3
from geometry.curve import Arc as Arc
from abstract.plane import Plane as Plane


p10=Point(10, 0, 0)
p20=Point(500, 20, 0)
p30=Point(1000, 0, 0)

p = Arc(p10, p20, p30)


obj = [p]


SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "fa4e56aed4"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"


SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)