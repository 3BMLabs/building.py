import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from geometry.surface import Surface
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from geometry.geometry2d import Vector2, Point2D, Line2D, PolyCurve2D


project = BuildingPy("PolyGon, to Surface and DXF to Ifc","0")


p1 = Point(0,0, 0)
p2 = Point(0,3000, 0)
# p3 = Point(2000,6500, 0)
p4 = Point(4000,3000, 0)
p5 = Point(4000,0, 0)
PG1 = Polygon.by_points([p1,p2,p4,p5,])

ip1_1 = Point(1000, 1000, 0)
ip1_2 = Point(1000, 2000, 0)
ip1_3 = Point(2000, 2000, 0)
ip1_4 = Point(2000, 1000, 0)
innerPolygon1 = Polygon.by_points([ip1_1, ip1_2, ip1_3, ip1_4])

ip2_1 = Point(2500, 1000, 0)
ip2_2 = Point(2500, 2000, 0)
ip2_3 = Point(3500, 2000, 0)
ip2_4 = Point(3500, 1000, 0)
innerPolygon2 = Polygon.by_points([ip2_1, ip2_2, ip2_3, ip2_4])

# SF1 = Surface.by_patch(PG1, [innerPolygon1, innerPolygon2])

lst = [PG1, innerPolygon1, innerPolygon2]


obj = Surface.by_patch_inner_and_outer(lst)
print(obj)

project.objects.append(obj)
# project.objects.append(SF1)
project.objects.append(PG1)
project.objects.append(innerPolygon1)
project.objects.append(innerPolygon2)

project.toSpeckle("7603a8603c")