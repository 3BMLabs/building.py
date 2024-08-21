import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.matrix import Matrix
from geometry.point import Point
from abstract.vector import Vector3

point = Point(1, 2, 3)
point2 : Point = Point([4,3,2])
mat = Matrix(Matrix.identity(4))
scalemat = Matrix.scale(4, 2)
scalemat[3][3] = 1
translatemat = Matrix.translate(Vector3(4,5,3))
combined = mat * scalemat * translatemat
combined2 = translatemat * scalemat
result = combined * point

print(result)