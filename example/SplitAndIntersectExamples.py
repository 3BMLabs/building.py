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

project = BuildingPy("Split and Intersect examples","0")


# front = Rectangle("test", 5000, 4000)


Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(500, 500, 0))
Line3 = Line(start=Point(500, 500, 0), end=Point(100, 1000, 0))

p1 = Point(0,0,0)
p2 = Point(0,500,0)
p3 = Point(250,750,0)
p4 = Point(500,500,0)
p5 = Point(500,0,0)

PC1 = PolyCurve.byPoints([p1,p2,p3,p4,p5,p1])
# PC2 = PC1.translate(Vector3(0,0.1,5))


project.objects.append(PC1)
# project.objects.append(PC2)

project.toSpeckle("bd33f3c533")