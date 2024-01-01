
from geometry.geometry2d import *
from abstract.vector import *
p1 = Point(100,200,0) #Point to mirror

AxisMirror = Vector3(5,3,0)


Perp = Vector3.crossProduct(AxisMirror,ZAxis)

print(Perp)