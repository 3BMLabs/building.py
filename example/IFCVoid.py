import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import *
from geometry.curve import *
from construction.void import *

polycurve = PolyCurve.by_points([Point(0,0,0), Point(100,0,0), Point(100,100,0), Point(0,100,0)])
height = 10.0
dz_loc = 0.0

void_object = Void.by_polycurve_height(polycurve, height, dz_loc)
project.objects.append(void_object)

project.toSpeckle("7603a8603c")