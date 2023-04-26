import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.curve import *
from abstract.vector import *

startPoint = Point(0,0,0)
midPoint = Point(70,181,0)
endPoint = Point(47,374,0)

a = Vector3.length(Point.difference(startPoint, midPoint))
b = Vector3.length(Point.difference(midPoint, endPoint))
c = Vector3.length(Point.difference(endPoint, startPoint))
s = (a + b + c) / 2
A = math.sqrt(s * (s - a) * (s - b) * (s - c))
R = (a * b * c) / (4 * A)

# calculation of origin of arc
Vstartend = Vector3.byTwoPoints(startPoint, endPoint)
halfVstartend = Vector3.scale(Vstartend, 0.5)
b = 0.5 * Vector3.length(Vstartend)  # half distance between start and end
x = math.sqrt(R * R - b * b)  # distance from start-end line to origin
mid = Point.translate(startPoint, halfVstartend)
v2 = Vector3.byTwoPoints(midPoint, mid)
v3 = Vector3.normalise(v2)
tocenter = Vector3.scale(v3, x)
center = Point.translate(mid, tocenter)
origin = center

a = Arc(startPoint=startPoint,midPoint=midPoint,endPoint=endPoint)
b = a.originarc()
print(b)