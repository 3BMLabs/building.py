from geometry.point import *

p1 = Point(1000,0,0)
p2 = Point.rotate_XY(p1, 180, 100)
print(p2)