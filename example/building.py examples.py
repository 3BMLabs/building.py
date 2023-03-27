from objects.panel import *
from objects.frame import *
from objects.shape import *
from exchange.speckle import *
from geometry.color import *
from geometry.linestyle import *
from objects.datum import *


def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b


obj = []

# Vector
v1 = Vector3(0, 100, 0)
v2 = Vector3(100,100,0)

# Point 3D
p1 = Point(0, 100, 0)

# Point 2D
p2 = Point2D(1000, 0)

# Lines
Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(-200, 500, 0))
Line3 = Line(start=Point(-200, 500, 0), end=Point(100, 1000, 0))
Line4 = Line(start=Point(100, 1000, 0), end=Point(400, 500, 0))
Line5 = Line(start=Point(400, 500, 0), end=Point(200, 500, 0))
Line6 = Line(start=Point(200, 500, 0), end=Point(200, 0, 0))
Line7 = Line(start=Point(200, 0, 0), end=Point(0, 0, 0))

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

# Panels
pan = Panel.byPolyCurveThickness(PC3, 100, 0, "test1", rgb_to_int([192, 192, 192]))
pan2 = Panel.byBaselineHeight(Line(start=Point(0, -1000, 0), end=Point(3000, -1000, 0)), 2500, 150, "wand", rgb_to_int([192, 192, 192]))
data = searchProfile("HE120A").shape_coords

# Frames
frame2 = Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(0, 1000, 0), "HE100A", "test")
frame3 = Frame.byStartpointEndpointProfileName(Point(500, 0, 0), Point(500, 1000, 0), "HE400B", "test2")

# Grid
GridA = Grid.byStartpointEndpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A")


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
obj3 = [pan, pan2, frame2, frame3]
obj4 = Lines4


SpeckleObj = translateObjectsToSpeckleObjects(obj2)
Commit = TransportToSpeckle("3bm.exchange", "8136460d9e", SpeckleObj, "building.py examples.py")