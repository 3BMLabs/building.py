import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
import numpy as np

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
from objects.panel import Panel
from abstract.color import Color
from geometry.surface import Surface
from packages.helper import *





Point1 = Point(1500,-3500,0)
Point2 = Point(6900,5000,0)
Point3 = Point(3420,5000,0)
Point4 = Point(0,0,0)
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point1])

Point5 = Point(400,0,0)
# Point6 = Point(-1400,0,0)

# is_point_in_polygon(Point5, ply1) #True
# is_point_in_polygon(Point6, ply1) #False

Point6 = Point(1200,400,0)
Point7 = Point(350,400,0)
Point8 = Point(300,30,0)
ply2 = PolyCurve.byPoints([Point5, Point6, Point7, Point8, Point5])

Point9 = Point(400,0,0)
Point10 = Point(1200,400,0)
Point11 = Point(0,400,0)
Point12 = Point(300,30,0)
ply3 = PolyCurve.byPoints([Point9, Point10, Point11, Point12, Point9])


is_polygon_in_polygon(ply1, ply2) #True
is_polygon_in_polygon(ply1, ply3) #False


obj = [ply1, ply2]



SpeckleHost = "3bm.exchange"
StreamID = "3e0d8773b3"
SpeckleObjects = obj
Message = "x"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)