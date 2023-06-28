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

obj = []

lst = ["HEA220",
"UNP260",
"K100/6.3",
"B42.4/2.6",
"INP140",
#"T140",
"UPE180",
"S50/10",
"R30",
#"L40/5"
]

p1 = Point(0,0,0)
p2 = Point(0,0,1000)
v1 = Vector3(500,0,0)
for i in lst:
    p1 = Point.translate(p1,v1)
    p2 = Point.translate(p2, v1)
    obj.append(Frame.byStartpointEndpointProfileName(p1, p2, i, i, BaseSteel))


shape = Round("30",15).curve
p1 = Point.translate(p1, v1)
p2 = Point.translate(p2, v1)

obj.append(Frame.byStartpointEndpoint(p1,p2,shape,"30",0,BaseSteel))
SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle("3bm.exchange", "c367421102", SpeckleObj, "Library of building.py")