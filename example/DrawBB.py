import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.shape3d import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from objects.annotation import *

project = BuildingPy("BoundingBoxes from Revit","1")
bb = Rect()

height = 3675

cs1 = CoordinateSystem(origin = Point(-16991.315, -3433.505, 1837.500), x_axis = Vector(0.766, 0.643, 0.000), y_axis = Vector(-0.643, 0.766, 0.000), z_axis = Vector(0.000, 0.000, 1.000))



bb_2d = Rect.centered_at_origin(Vector( 7350, 8550))
bb_3d = bb_2d

cbd_3d = bb_3d.to_cuboid()
cbd_parm = cbd_3d.set_parameter({"test_1": "1", "test_2": 2, 3: "test_3", 4:4})
project.objects.append(cbd_parm)

for axis in bb_3d.to_axis():
    project.objects.append(axis)


project.toSpeckle("29a6c39880")