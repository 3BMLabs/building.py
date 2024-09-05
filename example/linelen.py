import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from geometry.geometry2d import Vector2, Point2D, Line2D, PolyCurve2D


project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"


p1 = Point(0,0,0)
p2 = Point(0,3000,0)
p3 = Point(2000,6500,0)
p4 = Point(4000,3000,0)
p5 = Point(4000,0,0)

PC1 = PolyCurve.by_points([p1,p2,p3,p4,p5])
project.objects.append(PC1)

LN1 = Line(p2, p3)

print(PC1.length)

i = PolyCurve.length(PC1)
print(i)