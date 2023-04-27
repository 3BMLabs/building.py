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

startPoint = Point(0,0,0)
midPoint = Point(70,181,0)
endPoint = Point(47,374,0)

a = Arc(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint)
b = Arc(Point(100,0,0), Point(100/math.sqrt(2),100/math.sqrt(2),0), Point(0,100,0))

count = 15
#intv = Interval.bystartendcount(0, 1, count)
#obj = Arc.pointsAtParameter(b,intv)

obj = Arc.pointsAtParameter(a,count)

prof = profiledataToShape("HEA200")


pc2 = prof.prof.curve #2D polycurve
pc = PolyCurve.byPolyCurve2D(pc2)

#test = PolyCurve.segment(pc,10)
#print(test)

#sys.exit()
obj.append(pc)
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("3bm.exchange", "f140e5ec07", SpeckleObj, "Shiny commit 180")
