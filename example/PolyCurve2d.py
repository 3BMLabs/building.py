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


project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"

p1 = Point2D(0,0)
p2 = Point2D(0,3000)
p3 = Point2D(2000,6500)
p4 = Point2D(4000,3000)
p5 = Point2D(4000,0)

PC1 = PolyCurve2D.byPoints([p1,p2,p3,p4,p5])

i = PolyCurve2D.length(PC1)
print(i)

for j in PC1.curves2D:
    print(j)

project.objects.append(PC1)
project.toSpeckle("bd33f3c533")