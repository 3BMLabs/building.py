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

l1 = Line(start=Point(0, 0, 0), end=Point(0,1000,0))
project.objects.append(l1)

a3 = Arc(startPoint=Point(0,0,0), midPoint=Point(500,500,0), endPoint=Point(1000,0,0))
project.objects.append(a3)

a2 = Arc(startPoint=Point(0,0,0), midPoint=Point(500,-500,0), endPoint=Point(0,-1000,0))
project.objects.append(a2)

a1 = Arc(startPoint=Point(-500,0,0), midPoint=Point(500,500,0), endPoint=Point(500,0,0))
project.objects.append(a1)
print(f"id: {a1.id}", f"start: {a1.start}", f"mid: {a1.mid}", f"end: {a1.end}", f"origin: {a1.origin}", f"radius: {a1.radius}", f"angleRad: {a1.angleRadian}", f"length: {a1.length}", a1.coordinatesystem, sep="\n")

l2 = Line(start=Point(-500,0,0), end=Point(0,-1000,0))
project.objects.append(l2)

l3 = Line(start=Point(500,0,0), end=Point(0,-1000,0))
project.objects.append(l3)

# l2 = Line(start=Point(0, 0, 0), end=Point(0,1000000,0))
# project.objects.append(l2)

project.toSpeckle("5ab2faedba")