import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.geometry2d import Point2D
from exchange.speckle import *
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline
from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Arc as SpeckleArc
from specklepy.objects.primitive import Interval as SpeckleInterval
from abstract.boundingbox import BoundingBox

# from geometry.point import Point
# from geometry.curve import PolyCurve

p1 = Point(x=0, y=0, z=0)
p2 = Point(x=0, y=500, z=0)
p3 = Point(x=400, y=800, z=0)
bb = BoundingBox([p1,p2,p3])#.perimeter()
#Speckle Point

# pc1 = Polyline.from_points(points=[p1,p2,p3])


#Speckle Line
# Line = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(-800, -1000, 1000))


obj = []
obj.append(bb)
# obj.append(p2)

SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "fa4e56aed4"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)