import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape

# Export all steelprofiles to Speckle
lst = []
for item in jsondata:
    for i in item.values():
        lst.append(i[0]["synonyms"][0])
ToSpeckle = []

test = profiledataToShape("HEA200")
#sys.exit()
#3D Frames
x = 0
y = 0
spacing = 1000
height = 2000
count = 0
row = 25

#Mat = Material.byNameColor("Steel", Color().RGB([237, 237, 237]))

for i in lst:
    Mat = BaseSteel
    try:
        ToSpeckle.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, height), i, i, Mat))
        x = x + spacing
        count = count + 1
        if count > row:
            count = 0
            y = y + spacing
            x = 0
        else:
            pass
    except:
        print(i)

ToSpeckle.append(Frame.byStartpointEndpointProfileName(Point(0,0,0),Point(4000,0,0),"HEA200","HEA200",BaseSteel))

SpeckleObj = translateObjectsToSpeckleObjects(ToSpeckle)

Commit = TransportToSpeckle("3bm.exchange", "ceae170aaf", SpeckleObj, "Library of building.py")