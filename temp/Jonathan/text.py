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
from geometry.surface import *
from objects.objectcollection import *
from project.fileformat import *
from objects.shape3d import Origin
from exchange.DXF import ReadDXF
from abstract.boundingbox import BoundingBox2d
from abstract.coordinatesystem import CSGlobal
from geometry.systemsimple import *


grids = GridSystem.bySpacingLabels("0 500 5400",seqChar,"0 500 1500 2000", seqNumber,2500)
project.objects.append(grids)


XAxis = Vector3(1, 0, 0)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, 1)
CSXGlobal = CoordinateSystem(Point(5900, 4000, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Piet", font_family="arial", cs=CSXGlobal, scale=1).write()
for x in t1:
    project.objects.append(x)
    

CSXGlobal = CoordinateSystem(Point(5900, 4000, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Jonathan", font_family="arial", cs=CSXGlobal, scale=1.2).write()
for x in t1:
    project.objects.append(x)

XAxis = Vector3(1, 1, 0)
YAxis = Vector3(-1, 1, 0)
ZAxis = Vector3(0, 0, 1)
CSXGlobal = CoordinateSystem(Point(500, 500, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Maarten", font_family="arial", cs=CSXGlobal, scale=5).write()
for x in t1:
    project.objects.append(x)

XAxis = Vector3(1, 0, 1)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, -1)
CSXGlobal = CoordinateSystem(Point(500, 4000, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Jurian", font_family="arial", cs=CSXGlobal, scale=1.5).write()
for x in t1:
    project.objects.append(x)

XAxis = Vector3(-1, 0, 0)
YAxis = Vector3(0, -1, 0)
ZAxis = Vector3(1, 0, 1)
CSXGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Joas", font_family="arial", cs=CSXGlobal, scale=1.5).write()
for x in t1:
    project.objects.append(x)

XAxis = Vector3(1, 0, 0)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, 1)
CSXGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)
t1 = Text(text="Yeez", font_family="arial", cs=CSXGlobal, height=500).write()
for x in t1:
    project.objects.append(x)


project.toSpeckle("286a541c18")