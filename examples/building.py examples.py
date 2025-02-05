import math
#import geometry.geometry2d



from construction.panel import *
from construction.frame import *
from construction.shape3d import *
from construction.datum import *
from geometry.linestyle import *
from geometry.curve import *
from abstract.text import *
from geometry.point import Point
from exchange.speckle import *
from abstract.color import *
from geometry.plane import *
from geometry.solid import Extrusion
from geometry.rect import Rect

# INITIALIZE
pnt1 = Point(0, 0, 0)
pnt2 = Point(0, 10, 0)
pnt3 = Point(0, 20, 0)

# Point2d
p2d = Point(0, 0)
p2d2 = Point(10, 5)
p2d3 = Point(20, 10)
test12 = Vector(0, 10)

# CLASS: PLANE
v1 = Vector(0, 100, 0)
v2 = Vector(100, 100, 0)

plane_ex = Plane.by_two_vectors_origin(v1, v2, Point(0, 0, 0))

# CLASS: Vector

# sum ↓
# v1.X + v2.X, v1.Y + v2.Y, v1.Z + v2.Z
test1 = v1 + v2

# cross_product ↓
# v1.Y*v2.Z - v1.Z*v2.Y, v1.Z*v2.X - v1.X*v2.Z, v1.X*v2.Y - v1.Y*v2.X
test2 = Vector.cross_product(v1, v2)

# dot_product ↓
# v1.X * v2.X + v1.Y * v2.Y + v1.Z * v2.Z
test3 = Vector.dot_product(v1, v2)

# product ↓
# v1.X * n, v1.Y * n, v1.Z * n
test4 = Vector.product(5, v1)

# length ↓
# math.sqrt(v1.X * v1.X + v1.Y * v1.Y + v1.Z * v1.Z)
test5 = Vector.length(v1)

# pitch ↓
# v1.X, v1.Y*math.cos(angle) - v1.Z*math.sin(angle), v1.Y*math.sin(angle) + v1.Z*math.cos(angle)
test6 = Vector.pitch(v1, 45)

# angle_between ↓
# math.degrees(math.acos((Vector.dot_product(v1, v2) / (Vector.length(v1) * Vector.length(v2)))))
# (Calculate the angle of two vectors)
test7 = Vector.angle_between(v1, v2)

# reverse ↓
# Turn positive into negative and the other way around
test8 = Vector.reverse(v1)

# perpendicular ↓
# Vector Local X and Local Y perpendicular to given vector and in global Z direction
test9 = Vector.perpendicular(v1)

# normalize ↓
# scale = 1 / Vector.length(v1)
# v1.X * scale, v1.Y * scale, v1.Z * scale
test10 = Vector.normalize(v1)

# Point
p1 = Point(0, 100, 0)
p2 = Point(0, 300, 0)

# by_two_points ↓
# Subtracts point1 x,y and z from point2 x,y and z
test11 = Vector.by_two_points(p1, p2)

# FILE : CURVE
# CLASS: Line

# (Create the lines)
Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))

# Calculate the length of a line (Line1 in this example)
Line.length(Line1)

# CLASS: PolyCurve
# Create a PolyCurve object by joining a list of curves and collecting their starting points
PC1 = PolyCurve.by_joined_curves([Line1, Line2, Line3])

# Creating a PolyCurve object (PC2) from a list of Points.
# by points, must be a closed polygon
PC2 = PolyCurve.by_points(
    [Point(0, 0, 0),
     Point(2000, 0, 0),
     Point(0, 1000, 2000),
     Point(0, 0, 0)
     ])

ply = PolyCurve.by_joined_curves([
    Line(
        Point(0,0),
        Point(100,0)),
    Line(
        Point(100, 0),
        Point(100, 100)),
    Line(
        Point(100,100),
        Point(0,0))]
    )

# Creating a PolyCurve object (PC4) from a 3D polygon curve defined by four points.
PC4 = PolyCurve.by_polycurve_(ply)

# Poly-curve translate moves the curve by v1 vector.
PC4.translate(v1)

# Poly-curve Rotate  # NOT SURE WHAT THE INPUT HAS TO BE
PC4.rotate(90, 10)

# Polygon # CHECK IF ITS WORKING
# CLASS: POLYGON
# create an instance
# moet nog naar worden gekeken
flat_curves = [Line(Point(0, 0, 0), Point(0, 100, 0)), Line(Point(0, 100, 0), Point(100, 100, 0))]
plygn1 = Polygon(flat_curves)

# CLASS ARC
# Create a new Arc
arc1 = Arc(pnt1, pnt2, pnt3)

# Arc distance
# Calculates the distance between two points
Arc.distance(arc1, p1, p2)

# Arc radius
# Calculating radius of arc using the distance function
Arc.radius(arc1)

# Arc length
# Calculate length of Arc using its points.
Arc.length(arc1)

# Arc byThreePoints
# Creates an Arc from 3 points, with optional plane and properties.
Arc.ByThreePoints(pnt1, pnt2, pnt3)

# CLASS CIRCLE

radius = 5
length = 2 * radius * math.pi
circle = Circle(radius, plane_ex, length)

# CLASS ELLIPSE
# An Ellipse object is created with firstRadius=3, secondRadius=5
ellipse = Ellipse(3, 5, plane_ex)

# FILE Geometry

# Class Vector2
vctr2 = Vector2(10, 10)

# Class Point
# A new point P2Translate is created by translating p2d by the vector test12.
p2translate = Point.translate(p2d, test12)

# Poly-curve rotate
# A new point (P2Rotate) is created by rotating p2d 90 degrees.
p2rotate = Point.rotate(p2d, 90)

# Class Line
# A new  Line is created
l2d = Line(0, 100)
l2d2 = Line(100, 200)
l2d3 = Line(200, 300)

# Calculate the length of a  Line
ln2dlength = Line.length(l2d)

# Class Arc2d
testarc = Arc(p2d, p2d2, p2d3)

# returns point on the curve
Arc.points(testarc)

# Class PolyCurve
# Combine multiple lines and make it as 1 object
ply = PolyCurve.by_joined_curves([l2d, l2d2, l2d3])

# return all the points within the PolyCurve
PolyCurve.points(ply)

# translates each curve in ply by a Vector and returns a new PolyCurve.
PolyCurve.translate(ply, vctr2)

# rotates each curve in ply by a given rotation angle (90 degrees) and returns a new PolyCurve.
PolyCurve.rotate(ply, 90)

# returns a polygon by collecting start points of curves in ply.
PolyCurve.polygon(ply)

# Class Surface
surface1 = Surface()

# Class Profile
profile = Profile()

# Class ParametricProfile
para = ParametricProfile()

# ------------------------

# FILE: Line style
# line_to_pattern
LTP = line_to_pattern(Line(start=Point(0, 1200, 0), end=Point(11400, 1200, 0)), Centerline)

# ------------------------

# FILE: POINT
# Class Point
# calculate the difference between two 3D points and return a Vector.
exam = Point(0, 0, 0)

Point.difference(p1, p2)

# translates a 3D point (p1) by a given Vector (v1) and returns a new Point.
Point.translate(p1, v1)

# Transforms a  point into a 3D point
Point.point__to_3D(p2d)

# rotate (30 degrees) and translate (5 steps) a 3D point around the Z axis.
Point.rotate_XY(p1, 30, 5)

# Transforms a 3D point from one coordinate system to another using direction vectors.
transformed_point = transform_point(p1, CSGlobal, p2, v1)

# ------------------------

# FILE: Solid.py
# Class Extrusion
# Extrude a  profile to a 3D mesh
Extrusion.by_polycurve_height_vector(PC1, 20, 30, p1, v1)
Extrusion.by_polycurve_height(PC1, 20, 40)
  
# ------------------------

# FILE: Datum
GridA = Grid.by_startpoint_endpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A")

# get_grid_distances
# Function to create grids from the format 0, 4x5400, 4000, 4000 to absolute XYZ-values
get_grid_distances(GridA)

# GridSystem
spacingX = "4x5400 4000 4000"
labelsX = "A B C D"
spacingY = "4x4000 5400"
labelsY = "1 2 3"
gridExtension = 1000
grdsystem = GridSystem(spacingX, labelsX, spacingY, labelsY, gridExtension)

# ------------------------

# FILE: frame
# Class Frame
frame2 = Frame.by_startpoint_endpoint_profile(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test", "steel")
frame3 = Frame.by_startpoint_endpoint_profile(Point(500, 0, 0), Point(500, 1000, 0), "HE400B", "test2", "steel")
frame4 = Frame.by_startpoint_endpoint_profile_shapevector(p1, p2, "HE100A", "Frame 4", vctr2, 20, "steel")
frame5 = Frame.by_startpoint_endpoint_profile_justifiction(p1, p2, "HE100A", "Test", 5, 4, 90, "steel")
frame6 = Frame.by_startpoint_endpoint(p1, p2, PC1, "test", 90, "Steel")

# ------------------------

# CLASS: Panel
pan = Panel.by_polycurve_thickness(PC4, 100, 0, "test1", rgb_to_int([192, 192, 192]))
pan2 = Panel.by_baseline_height(Line(start=Point(0, -1000, 0),
                                   end=Point(3000, -1000, 0)), 2500, 150, "wand", rgb_to_int([192, 192, 192]))

# ------------------------

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
Text1 = Text(text="PyBuildingSystem1", font_family="arial", bounding_box=False, xyz=[0, 0, 0], rotation=90).write()
# all parms (with optional)
Text2 = Text(text="PyBuildingSystem2", font_family="arial").write()
# without optional parms


#Boundingbox
p1 = Point(x=900, y=0, z=0)
p2 = Point(x=20, y=500, z=30)
p3 = Point(x=400, y=410, z=160)
p4 = Point(x=650, y=800, z=0)
obj = [p1,p2,p3,p4]

bb = Rect.by_points(points=[p1,p2,p3,p4])