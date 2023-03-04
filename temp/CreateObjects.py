from objects.panel import *
from exchange.speckle import *

test = PolyCurve.byPoints(
    [Point(0,0,0),
     Point(2000,0,0),
     Point(0,1000,2000),
    Point(0,0,0)
     ])

pan = Panel.byPolyCurveThickness(test,100,0,"test")
pan2 = Panel.byBaselineHeight(Line(start= Point(0,0,0),end=Point(3000,0,0)),2500,150,"wand")
pan3 = Panel.byBaselineHeight(Line(start= Point(3000,0,0),end=Point(3000,3000,0)),2500,150,"wand")
pan4 = Panel.byBaselineHeight(Line(start= Point(3000,3000,0),end=Point(5000,5000,0)),2500,150,"wand")

SpeckleObj = translateObjectsToSpeckleObjects([pan2, pan3, pan4, pan.origincurve, pan2.origincurve])

Commit = TransportToSpeckle("3bm.exchange", "9548edd190", SpeckleObj, "Shiny Commit")