import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.curve import *
from abstract.interval import *
from abstract.coordinatesystem import *
from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from library.profile import *

startPoint = Point(0, 0, 0)
midPoint = Point(70, 181, 0)
endPoint = Point(47, 374, 0)

a = Arc(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint)
b = Arc(Point(100,0,0), Point(100/math.sqrt(2),100/math.sqrt(2),0), Point(0,100,0))

count = 15
#intv = Interval.bystartendcount(0, 1, count)
#obj = Arc.pointsAtParameter(b,intv)

prof = profiledataToShape("IPE300")
pc2 = prof.prof.curve #2D polycurve
pc = PolyCurve.byPolyCurve2D(pc2)
test = PolyCurve.segment(pc,10)
pc2Dback = test.toPolyCurve2D()

test = profiledataToShape("HEA200").polycurve2d
test2 = PolyCurve.byPolyCurve2D(test)

obj = []
obj.append(test2)
obj.append(Frame.byStartpointEndpointProfileName(Point(0,0,0),Point(4000,0,0),"HEA200","testbeam", BaseSteel))
#obj.append(Frame.byStartpointEndpointProfileName(Point(0,1000,0),Point(4000,1000,0),"IPE300","testbeam2",BaseSteel))

#Frame.byStartpointEndpoint(Point(1000,0,0),Point(5000,0,0),pc2Dback,"test",0,BaseSteel))
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("3bm.exchange", "f140e5ec07", SpeckleObj, "Shiny commit 180")
