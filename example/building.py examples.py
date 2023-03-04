from objects.panel import *
from objects.frame import *
from objects.shape import *
from exchange.speckle import *

Vector3(0,100,0)
Point(0,100,0)
Point2D(1000,0)

test = PolyCurve.byPoints(
    [Point(0,0,0),
     Point(2000,0,0),
     Point(0,1000,2000),
     Point(0,0,0)
     ])

pan = Panel.byPolyCurveThickness(test,100,0,"test")
pan2 = Panel.byBaselineHeight(Line(start= Point(0,0,0),end=Point(3000,0,0)),2500,150,"wand")
data = searchProfile("HE120A").shape_coords

#print(curve)
#sys.exit()
frame2 = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(0,1000,0), "HE100A", "test")
frame3 = Frame.byStartpointEndpointProfileName(Point(500,0,0), Point(500,1000,0), "HE400B", "test")
