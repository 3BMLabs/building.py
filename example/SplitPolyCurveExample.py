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

project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"


# Line1 = Line(start=Point(1000,-500,0), end=Point(2000,3000,0))
# project.objects.append(Line1)

Line2 = Line(start=Point(-500,500,0), end=Point(1500,-200,0))
project.objects.append(Line2)

p1 = Point(0,0,0)
p2 = Point(0,1000,0)
p3 = Point(1500,1500,0)
p4 = Point(1500,2500,0)
p5 = Point(2500,2500,0)
p6 = Point(2500,0,0)

contour = PolyCurve.by_points([p1,p2,p3,p4,p5,p6])
project.objects.append(contour)


polycurves = split_polycurve_by_line(contour, Line2)

for polycurve in polycurves["splittedPolycurve"]:
    project.objects.append(polycurve)


project.toSpeckle("bd33f3c533")