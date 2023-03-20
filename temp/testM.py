from objects.frame import *
from exchange.speckle import *
from objects.datum import *

obj1 = []
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(1000, 0, 1000), "K80/80/5","test")) # dakligger deel 1


SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "1852cf784e", SpeckleObj, "Test objects")