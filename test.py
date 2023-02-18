



"COLORS"
from exchange.speckle import *
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

test2 = findProfile("UNP200")

print(test2)

frm = Frame()
frm.byStartpointEndpointProfileName(Point(0,0,0), Point(2000,2000,1000), "UNP200", "test")
#frm.byStartpointEndpoint(Point(0,0,0), Point(3000,3000,1000), test2[0].curve, "test")
frm2 = SpeckleMeshByMesh(frm)

print(frm2.colors)
print(frm2.vertices)



#sys.exit()
SpeckleHost = "speckle.xyz" # struct4u.xyz
StreamID = "a2ff034164" #c4cc12fa6f
SpeckleObjects = [frm2]
Message = "Shiny commit 140"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)






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