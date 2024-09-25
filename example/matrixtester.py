import sys
from pathlib import Path

from geometry.pointlist import PointCloud

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.color import Color
from geometry.curve import Line, PolyCurve
from abstract.matrix import Matrix
from geometry.point import Point
from abstract.vector import Vector
from geometry.curve import Arc

point = Point(1, 2, 3)
point2 : Point = Point([4,3,2])
mat = Matrix(Matrix.identity(4))
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

l1 = Line(Point(1,2), Point(1, 5))
l2 = Arc(Point(1,5), Point(1.8, 6.2), Point(3,7))
l3 = Line(Point(3,7), Point(7,7))
curve = PolyCurve(l1,l2,l3)

pc = PointCloud([l.start, l.end])
transformed_pointcloud = combined2 * pc