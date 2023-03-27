from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *


pan1 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")
pan2 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")

pan3 = Panel.byPolyCurveThickness(PolyCurve.byPoints([Point(0,0,0),Point(1000,0,0),Point(1000,1000,0),Point(0,1000,0),Point(0,0,0)]),300,100,"De plate of Rob from New Jersey")
#sys.exit()
#frame1 = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(10000,0,0), "HEA300", "test")
#frame2 = Frame.byStartpointEndpointProfileName(Point(0,5000,0), Point(10000,5000,0), "HEA300", "test")
frame2 = Frame.byStartpointEndpointProfileName(Point(0,5000,0), Point(10000,5000,0), "IPE600", "test")
frame3 = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(10000,0,0), "IPE450", "test2")


SpeckleObj = translateObjectsToSpeckleObjects([frame2,frame3,pan3])

Commit = TransportToSpeckle("struct4u.xyz", "498714a19b", SpeckleObj, "Shiny Commit of Rob from the Headquarters of Struct4U Europe")
