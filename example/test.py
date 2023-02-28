import sys
from exchange.speckle import *
from geometry.curve import *
from geometry.point import *

from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Arc as SpeckleArc
from specklepy.objects.primitive import Interval as SpeckleInterval
from specklepy.objects.geometry import Extrusion
from specklepy.objects.geometry import Polycurve
from specklepy.objects.geometry import Polyline
from specklepy.objects.encoding import CurveArray, CurveTypeEncoding, ObjectArray


#PolyCurve test

Rectangle = 1000
P1 = SpecklePoint.from_coords(0,0,0)
P2 = SpecklePoint.from_coords(1000,0,0)
P3 = SpecklePoint.from_coords(1000,1000,0)
P4 = SpecklePoint.from_coords(0,1000,0)

Line1 = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(Rectangle, 0, 0), units = "mm")
Line2 = SpeckleLine(start = SpecklePoint.from_coords(Rectangle, 0, 0), end = SpecklePoint.from_coords(Rectangle, Rectangle, 0), units = "mm")
Line3 = SpeckleLine(start = SpecklePoint.from_coords(Rectangle, Rectangle, 0), end = SpecklePoint.from_coords(0, Rectangle, 0), units = "mm")
Line4 = SpeckleLine(start = SpecklePoint.from_coords(0, Rectangle, 0), end = SpecklePoint.from_coords(0, 0, 0), units = "mm")

#curvs = [Line1,Line2,Line3,Line4]
#crvArray = CurveArray.from_curves(curvs)

#ply = Polycurve.from_list(crvArray)

ply = Polyline.from_points([P1,P2,P3,P4,P1])
#ply.units = "mm"

#Test Extrusion

startpnt = SpecklePoint.from_coords(0,0,0)
endpnt = SpecklePoint.from_coords(0,0,3000)
cvr = SpeckleLine(start = startpnt, end = endpnt)

testextru = Extrusion(profile=ply, pathCurve=cvr, pathStart=startpnt, pathEnd=endpnt)

#Test
frm2 = []

#frm2.append(Line1)
#frm2.append(Line2)
#frm2.append(Line3)
#frm2.append(Line4)
#frm2.append(ply)
frm2.append(testextru)

#Rechte lijn

test = Line(Point(0,0,0),Point(2000,0,0))

speckletest = LineToSpeckleLine(test)

#frm2.append(speckletest)
#frm2.append(arcie)
#frm2.append(arcie2)

SpeckleHost = "speckle.xyz" # struct4u.xyz
StreamID = "bd36f755cd" #c4cc12fa6f
SpeckleObjects = [frm2]
Message = "Shiny commit 140"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)

sys.exit()

#ARC MAKEN LUKT NOG NIET.
V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector
X  = SpeckleVector.from_coords(1000, 0, 0)
Y = SpeckleVector.from_coords(0, 1000, 0)
Orig = SpecklePoint.from_coords(0, 0, 0)

pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)
int = SpeckleInterval(start=0, end=5, totalChildrenCount=1)

#ARC LUKT NOG NIET
arcie = SpeckleArc(
    startPoint=SpecklePoint.from_coords(0, 0, 0),
    midPoint=SpecklePoint.from_coords(1000, 0, 0),
    endPoint=SpecklePoint.from_coords(2000, 500, 0),
    plane=pln,
    interval=int,
    units="mm"
)

arcie2 = SpeckleArc(
    radius=2.3,
    startAngle=22.1,
    endAngle=44.5,
    angleRadians=33,
    startPoint=SpecklePoint.from_coords(0, 0, 0),
    midPoint=SpecklePoint.from_coords(100, 0, 0),
    endPoint=SpecklePoint.from_coords(100, 50, 0),
    plane=pln,
    interval=int,
    units="mm"
)


"COLORS"
from library import profile
from objects.frame import *
#    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
# list structure of verts is x y z x y z x y z
#    faces = [3, 0, 1, 2, 3, 2, 3, 5]
# list structure of faces is [number of verts], vert.index, vert.index, vert.index, vert2.index. enz.
# first number is number of vertices.
# then

test = SpeckleMesh(
    vertices= [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000],
    faces= [3, 0, 1, 2, 3, 2, 3, 5],
    colors=[111, 222], #list even groot als aantal faces
    name = "test",
    units = "mm"
    )

#test

test2 = findProfile("UNP200")

print(test2)

frm = Frame()
frm.byStartpointEndpointProfileName(Point(0,0,0), Point(2000,2000,1000), "UNP200", "test")
#frm.byStartpointEndpoint(Point(0,0,0), Point(3000,3000,1000), test2[0].curve, "test")
frm2 = SpeckleMeshByMesh(frm)

print(frm2.colors)
print(frm2.vertices)








"TESTING PART OF PROFILES"
from exchange.XFEM4U.xfem4unames import *
from library.profile import *

#print("Hello World")
from exchange.XFEM4U.xfem4unames import *
from objects.frame import *
from library.profile import *

#XFEM4U function to match a profile name with the building.py type

"Test of LAngle"
#test = matchprofile("L70X70X7")
#test5 = LAngle("L70/7", 70, 70, 7, 7, 9, 4.5, 19.7, 19.7).curve
#print(test5)

"Test of Rectangle Hollow Section"
#test2 = matchprofile("HFRHS150X150X8")
#test3 = matchprofile("K150/8")
#test4 = matchprofile("K150/150/8")
#test5 = findProfile(test2)

#Test of rectangle section
#test10 = matchprofile("S80X15")
#test11 = findProfile(test10)

#jsonFile = "C:/Users/mikev/Documents/GitHub/building.py/library/profile_database/steelprofile.json"
#jsonFileStr = open(jsonFile, "r").read()

#name = "UNP200"
#data = helper.findjson(name, jsonFileStr)[0]
#data.insert(0, name)  # voeg profilename toe aan de lijst
#d1 = data[:-1]

#print(d1)

#prof = CChannelSlopedFlange(d1[0],d1[1],d1[2],d1[3],d1[4],d1[5],d1[6],d1[7],d1[8],d1[9])
#print(prof)

#Test of UNP
#est10 = matchprofile("UNP200")
#test11 = findProfile("UNP200")
#print(test10)
#print(test11)

#print(profileNames)

#Load 2D PolyCurve
#sys.exit()

#start = Point(0,0,0)
##end = Point(1000,1000,1000)
##profile_name = "HEA200"
#frame = Frame()

#frame.byStartpointEndpointProfileName(start, end, "HEA200", "HEA200 tralalala")
#print(test)