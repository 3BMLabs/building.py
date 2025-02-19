

from geometry.curve import Line, PolyCurve
from geometry.coords import Point
from project.fileformat import BuildingPy

project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"


p1 = Point(0,0,0)
p2 = Point(0,3000,0)
p3 = Point(2000,6500,0)
p4 = Point(4000,3000,0)
p5 = Point(4000,0,0)

PC1 = PolyCurve.by_points([p1,p2,p3,p4,p5])
project.objects.append(PC1)

LN1 = Line(p2, p3)

print(PC1.length)