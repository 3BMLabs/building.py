import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *

filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\single.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

tmp = []

# for j in project.objects:
    # print(j.type)
    # if j.type == "Frame":
    #     pass
        # print(j.curve)
        

        # in the extrusion
        # project.objects.append(j.extrusion.centerline)
        # for x in j.extrusion.polycurve_3d_translated.curves:
        #     project.objects.append(x)
        # print()
        # if isinstance(j, list):
            # for i in j:
            #     i = PolyCurve2D.byJoinedCurves(j.extrusion.bottomshape)
            #     project.objects.append(i)
        # print(j.start, j.end)
        # project.objects.append(j.extrusion.bottomshape)
        # try:
        #     project.objects.append(j.curve3d)
        # except Exception as e:
        #     pass

project.toSpeckle("c6e11e74cb")