from exchange.Struct4U import *
from exchange.speckle import *
from abstract.plane import *
import xml.etree.ElementTree as ET

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

#tree = ET.parse("C:/TEMP/test134.xml")
tree = ET.parse("C:/Users/mikev/Documents/GitHub/building.py/temp/testplates.xml")
root = tree.getroot()

#List for SpeckleObjects
obj = []

#TODO: Lines and Grids units
#TODO: Plates dikte
#TODO: Create Plate

#LoadGrid and create in Speckle
Grids = XMLImportGrids(tree,1000)

XYZ = XMLImportNodes(tree)

Plates = XMLImportPlates(tree)


obj.append(Plates)
obj.append(Grids)

Points = Plates[1][3]

V1 =Vector3.byTwoPoints(Points[0],Points[1]) #Vector op basis van punt 0 en 1
V2 =Vector3.byTwoPoints(Points[-2],Points[-1]) #Vector op basis van laatste punt en een na laatste punt

p1 = Plane.byTwoVectorsOrigin(V1,V2,Points[0])

from geometry.solid import *
from geometry.curve import *

for i in Plates[1]:
    E = Extrusion.byPolyCurveHeight(PolyCurve.byPoints(i), 200, 0)
    Especk = SpeckleMesh(vertices= E.verts, faces=E.faces)
    obj.append(Especk)

#sys.exit()
#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")


# for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
#     profile_name = ProfileName[int(k.text)-1].text
#     if profile_name == None:
#         pass
#     else:
#         frame = Frame()
#         start = XYZ[int(i.text)-1]
#         end = XYZ[int(j.text)-1]
#         profile = matchprofile(profile_name)
#         try:
#             frame.byStartpointEndpointProfileName(start, end, profile, profile_name + "-" + l.text)
#         except:
#             pass
#         test = SpeckleMeshByMesh(frame)
#         obj.append(test)




SpeckleHost = "3bm.exchange" # struct4u.xyz
StreamID = "f1cf8ffd65" #c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny Commit"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)