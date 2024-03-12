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
import threading

project = BuildingPy("BoundingBoxes from Revit","1")


bb = BoundingBox3d()


#Vector xaxis, yaxis, zaxis -> cs system
height = 3675

cs1 = CoordinateSystem(origin = Point(-16991.315, -3433.505, 1837.500), xaxis = Vector3(0.766, 0.643, 0.000), yaxis = Vector3(-0.643, 0.766, 0.000), zaxis = Vector3(0.000, 0.000, 1.000))
# cs2 = CoordinateSystem(origin = Point(-30978.610, -4389.113, 774.449), xaxis = Vector3(0.754, 0.633, -0.174), yaxis = Vector3(-0.407, 0.659, 0.633), zaxis = Vector3(0.515, -0.407, 0.754))
# cs3 = CoordinateSystem(origin = Point(-18712.652, -17614.200, 1837.500), xaxis = Vector3(1.000, 0.000, 0.000), yaxis = Vector3(0.000, 1.000, 0.000), zaxis = Vector3(0.000, 0.000, 1.000))

bb_2d = BoundingBox2d().byDimensions(7350, 8550)
bb_3d = BoundingBox3d().convertBoundingbox2d(bb_2d, cs1, height)

cbd_3d = bb_3d.toCuboid()
cbd_parm = cbd_3d.setParameter({"test_1": "1", "test_2": 2, 3: "test_3", 4:4})
project.objects.append(cbd_parm)

for axis in bb_3d.toAxis():
    project.objects.append(axis)


project.toSpeckle("801883ce31")