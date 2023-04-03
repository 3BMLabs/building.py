<<<<<<< HEAD
from objects.panel import *  # Done
=======
import sys, os, math, random
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


from objects.panel import *
>>>>>>> ddcc731000766a3b8ae12e500c1f7c349f66d9eb
from objects.frame import *
from objects.steelshape import *
from objects.datum import *

from geometry.linestyle import *
from geometry.curve import *
from exchange.speckle import *
from abstract.color import *
from geometry.text import *

def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b


obj = []

# Point 3D
p1 = Point(0, 100, 0)
p2 = Point(0, 300, 0)

# Vector
v1 = Vector3(0, 100, 0)
v2 = Vector3(100, 100, 0)

# Vector sum(v1, v2)
test1 = Vector3.sum(v1, v2)
# vector crossProduct(v1, v2)
test2 = Vector3.crossProduct(v1, v2)
# vector dotProduct(v1, v2)
test3 = Vector3.dotProduct(v1, v2)
# vector product(n, v1)
test4 = Vector3.product(5, v1)
# vector length(v1)
test5 = Vector3.length(v1)
# vector pitch(v1, angle)
test6 = Vector3.pitch(v1, 45)
# vector angleBetween(v1, v2)
test7 = Vector3.angleBetween(v1, v2)
# vector reverse(v1)
test8 = Vector3.reverse(v1)
# vector perpendicular(v1)
test9 = Vector3.perpendicular(v1)
# vector normalise(v1)
test10 = Vector3.normalise(v1)
# vector byTwoPoints(cls, p1, p2)
test11 = Vector3.byTwoPoints(p1, p2)


# Point 2D
p2 = Point2D(1000, 0)

# Curve.py
Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))

# Line length
test12 = Line.length(Line1)

Line.

# Pattern
Lines4 = lineToPattern(Line(start=Point(0, 1200, 0),end=Point(11400, 1200, 0)), Centerline)

# sys.exit()
# PolyCurves(not working)
PC1 = PolyCurve.byJoinedCurves([Line1,Line2,Line3])
PC2 = PolyCurve.byPoints(
    [Point(0, 0, 0),
     Point(2000, 0, 0),
     Point(0, 1000, 2000),
     Point(0, 0, 0)
     ])

PC3 = PolyCurve.byPoints(
    [Point(3000, 0, 0),
     Point(5000, 0, 0),
     Point(5000, 2000, 2000),
     Point(2000, 2000, 2000),
     Point(3000, 0, 0)
     ])

PC4 = PolyCurve.byPolyCurve2D(
    [Point(0, 0, 0),
     Point(2000, 0, 0),
     Point(0, 1000, 2000),
     Point(0, 0, 0)
     ])

# Polygon(NOT WORKING!)
flatcurves = [1, 2, 3, 4, 5]
plygn1 = polygon(flatcurves)


pnt1 = Point(0, 0, 0)
pnt2 = Point(0, 10, 0)
pnt3 = Point(0, 20, 0)

arc1 = Arc(pnt1, pnt2, pnt3)
# Arc distance
Arc.distance(arc1, p1, p2)
# Arc radius
Arc.radius(arc1)
# Arc length
Arc.length(arc1)
# Arc bythreepoints
Arc.ByThreePoints(pnt1, pnt2, pnt3)

# Panels
pan = Panel.byPolyCurveThickness(PC3, 100, 0, "test1", rgb_to_int([192, 192, 192]))
pan2 = Panel.byBaselineHeight(Line(start=Point(0, -1000, 0),
                                   end=Point(3000, -1000, 0)), 2500, 150, "wand", rgb_to_int([192, 192, 192]))
data = searchProfile("HE120A").shape_coords
<<<<<<< HEAD

# Frames (NOT COMPLETE)
frame2 = Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test")
frame3 = Frame.byStartpointEndpointProfileName(Point(500, 0, 0), Point(500, 1000, 0), "HE400B", "test2")
frame4 = Frame.byStartpointEndpointProfileNameShapevector(Point(200, 0, 0), Point(500, 500, 0), "HE100A", "test3", 0, 100, 180, )
frame5 = Frame.byStartpointEndpoint(Point(0, 0, 0), Point(0, 1000, 0), )
=======
#ToDo test sjkfj
# Frames
# frame2 = Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test")
# frame3 = Frame.byStartpointEndpointProfileName(Point(500, 0, 0), Point(500, 1000, 0), "HE400B", "test2")
>>>>>>> ddcc731000766a3b8ae12e500c1f7c349f66d9eb

# Grid
GridA = Grid.byStartpointEndpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A")

# Color
c = Color()
print(c.red)
print(c.green)
print(c.blue)
print(c.Components('red'))
print(c.Hex('#ff2ba4'))
print(c.rgba_to_hex([0.5, 0.225, 0, 1]))
print(c.hex_to_rgba('#7F3900FF'))
print(c.CMYK([0.5, 0.25, 0, 0.2]))
print(c.Alpha([255, 0, 0, 128]))
print(c.Brightness(0.03))
print(c.RGB([255, 0, 0]))
print(c.HSV([120, 0.5, 0.8]))
print(c.HSL([120, 0.5, 0.8]))
print(c.RAL(1002))
print(c.Pantone('19-5232'))
print(c.LRV(237))


# Text
Text1 = Text(text="PyBuildingSystem1", font_family="arial", bounding_box=False, xyz=[0,0,0], rotation=90).write() #all parms (with optional)
Text2 = Text(text="PyBuildingSystem2", font_family="arial").write() # without optional parms

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 1000
spacX = "20x5400 2500"
spacY = "10x5400 1000"

grids = GridSystem(spacX, seqX, spacY, seqY, ext)

obj0 = GridA.line
obj1 = grids[0] + grids[1]
obj2 = [Line1, Line2, Line3, Line4, Line5, Line6, Line7]
obj3 = [pan, pan2]  # , frame2, frame3]
obj4 = Lines4


# SpeckleObj = translateObjectsToSpeckleObjects(obj2)
# Commit = TransportToSpeckle("3bm.exchange", "8136460d9e", SpeckleObj, "building.py examples.py")
