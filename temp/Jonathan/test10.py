import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
# https://help.xtools.pro/pro/22.0/en/XTools_Pro_Components/Geometry_Tools/Split_Polygons.htm

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


Text2 = Text(text="2", font_family="arial", bounding_box=False, xyz=Point(0, 0, 5), rotation=0)

j = None
for n in Text2.write():
    j = n[0].points
    # print()
    # print(BoundingBox2d.perimeter())

x = BoundingBox2d().byPoints(j)
i = PolyCurve().byPoints(x)

project.objects.append(i)
project.objects.append(Text2)

# sys.exit()


# p1 = Point(0, 0, 0)
# p2 = Point(120, 210, 50)
# project.objects.append(p1)
# project.objects.append(p2)

# v1 = Vector3(1,0,0)

# wp1 = WorkPlane.create()

# cs1 = CoordinateSystem(p1, XAxis, YAxis, ZAxis)


# trans = []
# for pt in wp1.points:
#     trans.append(transformPoint(pt, cs1, p2, v1))
# project.objects.append(PolyCurve().byPoints(trans))


project.toSpeckle("5ab2faedba")