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
t1 = Text(text="23 140 823A", font_family="arial", cs=CSXGlobal, scale=1).write()
print(t1.width)
sys.exit()
for x in t1:
    project.objects.append(x)

# t2 = Text(text="23 140 823A", font_family="arial", cs=CSXGlobal).write()
# for x in t2:
#     project.objects.append(x)

# CSXGlobal = CoordinateSystem(Point(0, 500, 450), XAxis, ZAxis, YAxis)
# t2 = Text(text="testit", font_family="arial", cs=CSXGlobal).write()
# for x in t2:
#     project.objects.append(x)
#
# print(Vector3.normalize(Vector3(1,1,0)))
# CSXGlobal = CoordinateSystem(Point(7000, 7000, 450), Vector3.normalize(Vector3(1,1,0)), Vector3.normalize(Vector3(-1,1,0)), ZAxis)
# t3 = Text(text="tralalkalala  123565437584392012345 asdagdg", font_family="calibri", cs=CSXGlobal).write()
# for x in t3:
#     project.objects.append(x)

WorkPlane.create(5000, 5000)
WorkPlane.create(5000, 2000)


project.toSpeckle("9f6798a2fa")