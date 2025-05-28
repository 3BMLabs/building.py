from abstract.vector import Point
from geometry.curve import Line, PolyCurve
from library.profile import data as jsondata
from project.fileformat import BuildingPy


project = BuildingPy("Split and Intersect examples", "0")
project.speckleserver = "speckle.xyz"

Line2 = Line(start=Point(-500, 500, 0), end=Point(1500, -200, 0))
project.objects.append(Line2)

p1 = Point(0, 0, 0)
p2 = Point(0, 1000, 0)
p3 = Point(1500, 1500, 0)
p4 = Point(1500, 2500, 0)
p5 = Point(2500, 2500, 0)
p6 = Point(2500, 0, 0)

contour = PolyCurve.by_points([p1, p2, p3, p4, p5, p6])
project.objects.append(contour)


polycurves = split_polycurve_by_line(contour, Line2)

for polycurve in polycurves["splittedPolycurve"]:
    project.objects.append(polycurve)


project.to_speckle("bd33f3c533")
