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
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from geometry.geometry2d import Vector2, Point2D, Line2D, PolyCurve2D


point_1 = Point(100.23, 182, 19)
point_2 = Point(81, 0.1, -901)
output = Point.distance(point_1, point_2) 
# 938.0071443757771

point_1 = Point(231, 13, 76)
point_2 = Point(71, 12.3, -232)
point_3 = Point(2, 71, -102)
output = Point.distance_list([point_1, point_2, point_3])
# [(<geometry.point.Point object at 0x00000226BD9CAB90>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 158.45090722365714), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 295.78539517697624), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BD9CAB90>, 347.07994756251765)]

point_1 = Point(23, 1, 23)
point_2 = Point(93, 0, -19)
output = Point.difference(point_1, point_2)
# Vector3(X = 70.000, Y = -1.000, Z = -42.000)

point = Point(23, 1, 23)
vector = Vector3(93, 0, -19)
output = Point.translate(point, vector)
# Point(X = 116.000, Y = 1.000, Z = 4.000)

point_1 = Point(100.23, 182, 19)
point_2 = Point(81, 0.1, -901)
output = Point.origin(point_1, point_2)
# Point(X = 90.615, Y = 91.050, Z = -441.000)


l1 = Line(start=point_1, end=point_2)
l2 = Line(start=point_2, end=point_3)
output = PolyCurve.by_joined_curves([l1, l2])
print(output)