import sys, os, math, random
from pathlib import Path

import geometry.geometry2d

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from objects.datum import *

from geometry.linestyle import *
from geometry.curve import *
from exchange.speckle import *
from abstract.color import *
from geometry.text import *
from geometry.point import Point

def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b

# ------------------------

# INITIALIZE
v1 = Vector3(0, 100, 0)
v2 = Vector3(100, 100, 0)

p1 = Point(0, 100, 0)
p2 = Point(0, 300, 0)

# ------------------------

# FILE: COORDINATESYSTEM
CSGlobal = CoordinateSystem(pnt(0, 0, 0), XAxis, YAxis, ZAxis)

# ------------------------

# FILE: PLANE
btvo = Plane.byTwoVectorsOrigin(v1, v2, pnt(0, 0, 0))

# ------------------------

# FILE: VECTOR
# CLASS: Vector3

# sum ↓
# v1.X + v2.X, v1.Y + v2.Y, v1.Z + v2.Z
test1 = Vector3.sum(v1, v2)

# crossProduct ↓
# v1.Y*v2.Z - v1.Z*v2.Y, v1.Z*v2.X - v1.X*v2.Z, v1.X*v2.Y - v1.Y*v2.X
test2 = Vector3.crossProduct(v1, v2)

# dotProduct ↓
# v1.X * v2.X + v1.Y * v2.Y + v1.Z * v2.Z
test3 = Vector3.dotProduct(v1, v2)

# product ↓
# v1.X * n, v1.Y * n, v1.Z * n
test4 = Vector3.product(5, v1)

# length ↓
# math.sqrt(v1.X * v1.X + v1.Y * v1.Y + v1.Z * v1.Z)
test5 = Vector3.length(v1)

# pitch ↓
# v1.X, v1.Y*math.cos(angle) - v1.Z*math.sin(angle), v1.Y*math.sin(angle) + v1.Z*math.cos(angle)
test6 = Vector3.pitch(v1, 45)

# angleBetween ↓
# math.degrees(math.acos((Vector3.dotProduct(v1, v2) / (Vector3.length(v1) * Vector3.length(v2)))))
# (Calculate the angle of two directions)
test7 = Vector3.angleBetween(v1, v2)

# reverse ↓
# Turn positive into negative and the other way around
test8 = Vector3.reverse(v1)

# perpendicular ↓
# Vector Local X and Local Y perpendicular to given vector and in global Z direction
test9 = Vector3.perpendicular(v1)

# normalise ↓
# scale = 1 / Vector3.length(v1)
# v1.X * scale, v1.Y * scale, v1.Z * scale
test10 = Vector3.normalise(v1)

# byTwoPoints ↓
# Subtracts point1 x,y and z from point2 x,y and z
test11 = Vector3.byTwoPoints(p1, p2)

# ------------------------

# FILE : CURVE
# CLASS: Line

Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))

# Calculate the length of a line
Line.length(Line1)
# CLASS: PolyCurve
plycurve = PolyCurve()

# Create a PolyCurve object by joining a list of curves and collecting their starting points
PC1 = PolyCurve.byJoinedCurves([Line1, Line2, Line3])

PC2 = PolyCurve.byPoints(
    [Point(0, 0, 0),
     Point(2000, 0, 0),
     Point(0, 1000, 2000),
     Point(0, 0, 0)
     ])

# ------------------------
obj = []

# Point 3D
# p1 = Point(0, 100, 0)
# p2 = Point(0, 300, 0)

# Line2d
l2d = Line2D(0, 100)


# Point2d
p2d = Point2D(0,0)
p2d2 = Point2D(10,5)
p2d3 = Point2D(20,10)
test12 = Vector2(0, 10)
# Point2d Translate
p2dtrnslt = Point2D.translate(p2d, test12)
# Point2d rotate
p2drotate = Point2D.rotate(p2d, 90)

# Point 2D
p2 = Point2D(1000, 0)
p3 = Point2D.translate(p2, test12)
# Line2d Length
ln2dlength = Line2D.length(l2d)

# Arc2D
testarc = Arc2D(p2d, p2d2, p2d3)
Arc2D.points(testarc)

vctr2 = Vector2(10, 10)

ply = PolyCurve2D()
PolyCurve2D.byJoinedCurves(90)
PolyCurve2D.points(ply)
PolyCurve2D.translate(ply, vctr2)
PolyCurve2D.rotate(ply, 90)
PolyCurve2D.polygon(ply)

# Pattern
Lines4 = lineToPattern(Line(start=Point(0, 1200, 0),end=Point(11400, 1200, 0)), Centerline)

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

PolyCurve.translate(plycurve, v1)

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
pan2 = Panel.byBaselineHeight(Line(start = Point(0, -1000, 0), end = Point(3000, -1000, 0)), 2500, 150, "wand", rgb_to_int([192, 192, 192]))
data = searchProfile("HE120A").shape_coords
#ToDo test sjkfj
# Frames
# frame2 = Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test")
# frame3 = Frame.byStartpointEndpointProfileName(Point(500, 0, 0), Point(500, 1000, 0), "HE400B", "test2")

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

grids = GridSystem(spacX,seqX,spacY,seqY,ext)

obj0 = GridA.line
obj1 = grids[0] + grids[1]
obj2 = [Line1, Line2, Line3, Line4, Line5, Line6, Line7]
obj3 = [pan, pan2]#, frame2, frame3]
obj4 = Lines4


# SpeckleObj = translateObjectsToSpeckleObjects(obj2)
# Commit = TransportToSpeckle("3bm.exchange", "8136460d9e", SpeckleObj, "building.py examples.py")