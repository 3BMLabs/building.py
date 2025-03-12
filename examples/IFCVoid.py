from abstract.vector import Point
from construction.void import Void
from geometry.curve import PolyCurve
from project.fileformat import BuildingPy

polycurve = PolyCurve.by_points(
    [Point(0, 0, 0), Point(100, 0, 0), Point(100, 100, 0), Point(0, 100, 0)]
)
height = 10.0
dz_loc = 0.0

void_object = Void.by_polycurve_height(polycurve, height, dz_loc)
project = BuildingPy()
project.objects.append(void_object)

project.toSpeckle("7603a8603c")
