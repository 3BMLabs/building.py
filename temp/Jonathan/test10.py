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
from abstract.text import Text, Text2
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

# Text1 = Text(text="123 4", font_family="arial", bounding_box=True, xyz=Point(0, 0, 0), rotation=Vector3(1, 0, 0)).write()


Text(text="23 140 823A", font_family="arial", cs=CSGlobal, xyz=Point(0, 0, 0), v=Vector3(0, 1, 0)).write()
WorkPlane.create(5000, 5000)
# sys.exit()


# project.objects.append(Text2[0])
# print(Text2.write())
# j = None
# for n in Text1:
#     j = n.points
    # print()
    # print(BoundingBox2d.perimeter())

# x = BoundingBox2d().byPoints(j)
# i = PolyCurve().byPoints(x)

# project.objects.append(i)
# project.objects.append(Text2)

# sys.exit()


project.toSpeckle("5ab2faedba")