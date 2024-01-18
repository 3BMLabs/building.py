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


p1 = Point(0,0,0)
p2 = Point(0,3000,0)
p3 = Point(2000,6500,0)
p4 = Point(4000,3000,0)
p5 = Point(4000,0,0)

PC1 = PolyCurve.byPoints([p1,p2,p3,p4,p5])
project.objects.append(PC1)

#MULTI PATROON

test2 = PatternSystem().StretcherBondWithJoint("halfsteensverband",0,210,50,10,12.5)
# test2 = PatternSystem().TileBondWithJoint("tegels",400,400,0,10,10)
test_res = PatternGEOM(test2,4200,6500)

for index, line in enumerate(PC1.curves):
    for p, i in enumerate(test_res):
        PCPanel = i.extrusion.polycurve_3d_translated
        got = None
        x = splitPolyCurveByLine(PCPanel, line)

        pc = None
        if len(x["splittedPolycurve"]) == 0:
            pc = [PCPanel]
        else:
            pc = x["splittedPolycurve"]

        if len(x["splittedPolycurve"]) == 0:
            if is_polycurve_in_polycurve(PCPanel, PC1):
                project.objects.append(PCPanel)
        else:
            for i in x["splittedPolycurve"]:
                try:
                    if is_point_in_polycurve(i.centroid(), PC1):
                        project.objects.append(i)
                except:
                    pass

project.toSpeckle("bd33f3c533")