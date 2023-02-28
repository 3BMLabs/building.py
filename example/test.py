from geometry.flat import Point2D
from exchange.speckle import *
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline
from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Arc as SpeckleArc

#Speckle Point
SpecklePoint.from_coords(0, 0, 0)

#Speckle Line
Line = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(800, 1000, 1000))

#Speckle Vector
#V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector

#Speckle Plane
V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector
X = SpeckleVector.from_coords(1000, 0, 0)
Y = SpeckleVector.from_coords(0, 1000, 0)
Orig = SpecklePoint.from_coords(0, 0, 0)
#pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)

#Speckle Polyline
P1 = SpecklePoint.from_coords(0,0,0)
P2 = SpecklePoint.from_coords(1000,0,0)
P3 = SpecklePoint.from_coords(2000,0,0)
P4 = SpecklePoint.from_coords(2000,1000,0)

ply = Polyline.from_points([P1,P2,P3,P4])

#-1762845660


Messie = SpeckleMesh(vertices = [0,0,0,1000,0,0,1000,1000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh") #, units = "mm"
Messie2 = SpeckleMesh(vertices = [1000,1000,0,1000,1000,1000,2000,2000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh", colors = [-1762845660,-1762845660,-1762845660]) #, units = "mm"

#    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
# list structure of verts is x y z x y z x y z
#    faces = [3, 0, 1, 2, 3, 2, 3, 5]

#pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)
#int = SpeckleInterval(start=0, end=5, totalChildrenCount=1)

#ARC LUKT NOG NIET
#arcie = SpeckleArc(
#    startPoint=SpecklePoint.from_coords(0, 0, 0),
#    midPoint=SpecklePoint.from_coords(1000, 0, 0),
#    endPoint=SpecklePoint.from_coords(2000, 500, 0),
#    plane=pln,
#    interval=int,
#    units="mm"
#)

obj = []
obj.append(ply)
obj.append(Line)
obj.append(Messie)
obj.append(Messie2)


#sys.exit()

SpeckleHost = "speckle.xyz"  # struct4u.xyz
StreamID = "ca31cc7a2f"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)


