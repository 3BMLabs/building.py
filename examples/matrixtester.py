import sys
from pathlib import Path




from abstract.color import Color
from geometry.curve import Line, PolyCurve
from abstract.matrix import Matrix
from abstract.vector import Point
from abstract.vector import Vector
from geometry.curve import Arc
from geometry.pointlist import PointCloud

point = Point(1, 2, 3)
point2 : Point = Point([4,3,2])
mat = Matrix(Matrix.identity(3))
scalemat = Matrix.scale(4, 2)
scalemat[3][3] = 1
translatemat = Matrix.translate(Vector(4,5,3))
#multiplication order: right to left
combined = translatemat * scalemat *mat 
combined2 = scalemat* translatemat
result = combined * point

l = Line(Point(1,2,3), Point(4,5,6))

#multiply line by the matrix
transformed_l = combined2 * l

print(result)
print(result * 4)
print(result / 5)
#normalize
result.magnitude = 1

c  = Color(23,42,43,255)
print(c.hex)


#counter clockwise
l1 = Line(Point(7,7), Point(3, 7))
l2 = Arc(Point(3,7), Point(1.8, 6.2), Point(1,5))
l3 = Line(Point(1,5), Point(1,2))
curve = PolyCurve(l1,l2,l3)

pc = PointCloud([l.start, l.end])
transformed_pointcloud = combined2 * pc

curve.closed = True
area = curve.area
print(area)

centroid = curve.centroid
print(centroid)

sm = curve.statical_moment
print(sm)
