from objects.panel import *
from geometry.curve import *
from geometry.point import *
from exchange.speckle import *

speckleObjects = [] #Objects to send to Speckle

test = PolyCurve.byPoints([Point(0,0,0),Point(1000,0,0),Point(1000,1000,0),Point(0,1000,0)])
panel = Panel.byPolyCurveThickness(test,200,100,"test")

#Especk = SpeckleMesh(vertices= panel.extrusion.verts, faces=panel.extrusion.faces)
#speckleObjects.append(Especk)

print(test.curves)


SpeckleHost = "3bm.exchange" # struct4u.xyz
StreamID = "9548edd190" #c4cc12fa6f
SpeckleObjects = speckleObjects
Message = "Shiny Commit"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)