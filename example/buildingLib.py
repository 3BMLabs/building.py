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

ToSpeckle = []

#3D Frames
x = 0
y = 0
spacing = 1000
height = 1500
count = 0
row = 25
for i in lst:
    ToSpeckle.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, height), i, i))
    x = x + spacing
    count = count + 1
    if count > row:
        count = 0
        y = y + spacing
        x = 0
    else:
        pass
#sys.exit()

#sys.exit()


SpeckleObj = translateObjectsToSpeckleObjects(ToSpeckle)

Commit = TransportToSpeckle("3bm.exchange", "ceae170aaf", SpeckleObj, "Library of building.py")