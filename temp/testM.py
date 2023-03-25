from objects.frame import *
from exchange.speckle import *
from objects.datum import *
from library.profile import *
from copy import deepcopy
from geometry.geometry2d import *
import math
a = profiledataToShape("HEA200").prof.curve
b = deepcopy(a)
c = a.translate(Vector2(100,100))
print(a.curves)



obj1 = []
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(1000, 0, 0), "L70/70/7", "test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 100, 0), Point(1000, 100, 0), "L70/70/7", "test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 300, 0), Point(1000, 300, 0), "HEA200", "test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameShapevector(Point(0, 300, 0), Point(1000, 300, 0), "HEA200","test",Vector2(-0,0),0)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameJustifiction(Point(0, 300, 0), Point(1000, 300, 0), "HEA200","test","left","top",0)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameShapevector(Point(0, 300, 500), Point(1000, 300, 800), "HEA200","test",Vector2(-0,0),45)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameJustifiction(Point(0, 300, 500), Point(1000, 300, 800), "HEA200","test","left","top",-45)) # dakligger deel 1

SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "1852cf784e", SpeckleObj, "Test objects")