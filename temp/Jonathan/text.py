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


XAxis = Vector3(1, 0, 0)
YAxis = Vector3(0, 1, 0)
ZAxis = Vector3(0, 0, 1)
CSXGlobal = CoordinateSystem(Point(0, 0, 0), XAxis, YAxis, ZAxis)

t1 = Text(text="23 140 823A", font_family="arial", cs=CSXGlobal, xyz=Point(0, 0, 0)).write()
for x in t1:
    project.objects.append(x)




CSXGlobal = CoordinateSystem(Point(0, 500, 450), XAxis, ZAxis, YAxis)
t2 = Text(text="testit", font_family="arial", cs=CSXGlobal, xyz=Point(450, 0, 0)).write()
for x in t2:
    project.objects.append(x)

WorkPlane.create(5000, 5000)


project.toSpeckle("9f6798a2fa")