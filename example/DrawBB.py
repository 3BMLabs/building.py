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


#Vector x_axis, y_axis, z_axis -> cs system
height = 3675

cs1 = CoordinateSystem(origin = Point(-16991.315, -3433.505, 1837.500), x_axis = Vector3(0.766, 0.643, 0.000), y_axis = Vector3(-0.643, 0.766, 0.000), z_axis = Vector3(0.000, 0.000, 1.000))
# cs2 = CoordinateSystem(origin = Point(-30978.610, -4389.113, 774.449), x_axis = Vector3(0.754, 0.633, -0.174), y_axis = Vector3(-0.407, 0.659, 0.633), z_axis = Vector3(0.515, -0.407, 0.754))
# cs3 = CoordinateSystem(origin = Point(-18712.652, -17614.200, 1837.500), x_axis = Vector3(1.000, 0.000, 0.000), y_axis = Vector3(0.000, 1.000, 0.000), z_axis = Vector3(0.000, 0.000, 1.000))

bb_2d = BoundingBox2d().by_dimensions(7350, 8550)
bb_3d = BoundingBox3d().convert_boundingbox_2d(bb_2d, cs1, height)

cbd_3d = bb_3d.to_cuboid()
cbd_parm = cbd_3d.set_parameter({"test_1": "1", "test_2": 2, 3: "test_3", 4:4})
project.objects.append(cbd_parm)

for axis in bb_3d.to_axis():
    project.objects.append(axis)


project.toSpeckle("801883ce31")