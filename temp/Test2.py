import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from objects.frame import *
from exchange.struct4U import *
from objects.analytical import *
from specklepy.objects.geometry import Extrusion as SpeckleExtrusion

plc1 = PolyCurve.byPoints([
    Point(0,0,0),
    Point(1000,0,0),
    Point(1000,1000,0),
    Point(0,0,0)
])

ln = Line(start=Point(500,500,0), end=Point(500,500,5000))
p1 = Point(500,500,0)
p2 = Point(500,500,5000)

obj = translateObjectsToSpeckleObjects([plc1,p1,p2])

class Profile(Base):
    # Hoofdclass waar alle objecten uit het model in gezet worden.
    Profile = None

Prof = Profile(Profile=obj[0])

print(obj[0])
#sys.exit()

E1 = SpeckleExtrusion(profile = Prof, pathStart = obj[1], pathEnd = obj[2])

sobj = [plc1,E1]

Commit = TransportToSpeckle("3bm.exchange", "9f6c454216", sobj, "Extrusion test")