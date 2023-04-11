import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))


from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata

# Export all steelprofiles to Speckle
lst = []
for item in jsondata:
    for i in item.values():
        lst.append(i[0]["synonyms"][0])
        print(i)
ToSpeckle = []
height = 3000

ToSpeckle.append(Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(0, 0, height), "L100/100/10", "L100/100/10",BaseSteel))


SpeckleObj = translateObjectsToSpeckleObjects(ToSpeckle)

Commit = TransportToSpeckle("3bm.exchange", "ceae170aaf", SpeckleObj, "Library of building.py")