from abstract.vector import Point
from geometry.curve import PolyCurve
from project.fileformat import BuildingPy

project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"

p1 = Point(0,0)
p2 = Point(0,3000)
p3 = Point(2000,6500)
p4 = Point(4000,3000)
p5 = Point(4000,0)

PC1 = PolyCurve.by_points([p1,p2,p3,p4,p5])

print(PC1.length)

for j in PC1:
    print(j)

project.objects.append(PC1)
project.to_speckle("ed88c2cdb3")