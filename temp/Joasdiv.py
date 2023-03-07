from objects.panel import *
from objects.frame import *
from objects.shape import *
from exchange.speckle import *

# pan1 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")
# pan2 = Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand")

test = searchProfile("HEA300")

# e1shape = Frame.byStartpointEndpoint(Point(0, 0, 0), Point(0, 0, 50), Eshape("joas", 300, 200, 50).curve,"Joas zijn E1-frame")
# tshape = Frame.byStartpointEndpoint(Point(400, 0, 0), Point(400, 0, 50), Tshape("joas", 300, 200, 60, 50).curve,"Joas zijn T-frame")
# e2shape = Frame.byStartpointEndpoint(Point(800, 0, 0), Point(800, 0, 50), Eshape("joas", 300, 200, 50).curve,"Joas zijn E2-frame")
# nshape = Frame.byStartpointEndpoint(Point(1200, 0, 0), Point(1200, 0, 50), Nshape("joas", 300, 200, 50).curve,"Joas zijn N-frame")


lshape = Frame.byStartpointEndpoint(Point(0, 0, 0), Point(0, 0, 50),Lshape("joas", 300, 200, 50, 50).curve,"Joas zijn L-frame")
e1shape = Frame.byStartpointEndpoint(Point(400, 0, 0), Point(400, 0, 50), Eshape("joas", 300, 200, 50).curve,"Joas zijn E1-frame")
nshape = Frame.byStartpointEndpoint(Point(800, 0, 0), Point(800, 0, 50), Nshape("joas", 300, 200, 50).curve,"Joas zijn N-frame")
tshape = Frame.byStartpointEndpoint(Point(1200, 0, 0), Point(1200, 0, 50), Tshape("joas", 300, 200, 60, 50).curve,"Joas zijn T-frame")
e2shape = Frame.byStartpointEndpoint(Point(1600, 0, 0), Point(1600, 0, 50), Eshape("joas", 300, 200, 50).curve,"Joas zijn E2-frame")


# SpeckleObj = translateObjectsToSpeckleObjects([tshape, lshape, eshape, nshape])
# SpeckleObj = translateObjectsToSpeckleObjects([e1shape, tshape, e2shape, nshape])
SpeckleObj = translateObjectsToSpeckleObjects([lshape, e1shape, nshape, tshape, e2shape])

Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit")
