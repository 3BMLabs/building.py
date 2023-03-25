from abstract.color import *
from library.material import *
from objects.frame import *
from exchange.speckle import *

obj1 = []
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(1000, 0, 0), "L70/70/7", "test", BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 100, 0), Point(1000, 100, 0), "L70/70/7", "test", BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 300, 0), Point(1000, 300, 0), "HEA200", "test", BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameShapevector(Point(0, 300, 0), Point(1000, 300, 0), "HEA200","test",Vector2(-0,0),0, BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameJustifiction(Point(0, 300, 0), Point(1000, 300, 0), "HEA200","test","left","top",0, BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameShapevector(Point(0, 300, 500), Point(1000, 300, 800), "HEA200","test",Vector2(-0,0),45, BaseSteel)) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameJustifiction(Point(0, 300, 500), Point(1000, 300, 800), "HEA200","test","left","top",-45, BaseSteel))
obj1.append(Frame.byStartpointEndpoint(Point(3000, 0, 0), Point(6000, 0, 0),Rectangle("400x500", 500, 400).curve.curves,"Betonbalk 400x500", BaseConcrete))

obj1.append(Frame.byStartpointEndpoint(Point(2000, 0, 0), Point(2000, 0, 1500),Rectangle("38x184", 184, 38).curve,"SLS 38x184", BaseTimber))
obj1.append(Frame.byStartpointEndpoint(Point(2600, 0, 0), Point(2600, 0, 1500),Rectangle("38x184", 184, 38).curve,"SLS 38x184", BaseTimber))

SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "1852cf784e", SpeckleObj, "Test objects")

