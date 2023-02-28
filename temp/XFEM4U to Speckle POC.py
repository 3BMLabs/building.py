import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

import xml.etree.ElementTree as ET
#tree = ET.parse("C:/TEMP/test134.xml")
tree = ET.parse("C:/Users/mikev/Documents/GitHub/building.py/temp/testplates.xml")

root = tree.getroot()

from exchange.speckle import *
from geometry.curve import Line
from geometry.curve import *
from geometry.point import Point
from specklepy.objects.geometry import Polyline as SpecklePolyLine
from objects.frame import Frame
from exchange.XFEM4U.xfem4unames import *
from exchange.Struct4U import XMLImportgetGridDistances
from objects.panel import Panel

#List for SpeckleObjects
obj = []

#GRIDS
GridEx = 1000

GridsX = root.findall(".//Grids/X")[0].text.split()
GridsX = XMLImportgetGridDistances(GridsX)
Xmax = max(GridsX)
GridsXLable = root.findall(".//Grids/X_Lable")[0].text.split()
GridsY = root.findall(".//Grids/Y")[0].text.split()
GridsY = XMLImportgetGridDistances(GridsY)
Ymax = max(GridsY)
GridsYLable = root.findall(".//Grids/Y_Lable")[0].text.split()
GridsZ = root.findall(".//Grids/Z")[0].text.split()
GridsZ = XMLImportgetGridDistances(GridsZ)
GridsZLable = root.findall(".//Grids/Z_Lable")[0].text.split()
Zmax = max(GridsZ)

from geometry.curve import *

grids = []
for i in GridsX:
    grids.append(Line(Point(i, -GridEx, 0),Point(i, Ymax+GridEx, 0)))

for i in GridsY:
    grids.append(Line(Point(-GridEx, i, 0),Point(Xmax+GridEx, i, 0)))

for i in GridsZ:
    grids.append(Line(Point(0, 0, i) , Point(0, Xmax, i)))

for i in grids:
    line = LineToSpeckleLine(i) #Grid to SpeckleLine
    obj.append(line)


#POINTS
n = root.findall(".//Nodes/Number")
nodenumbers = []
for i in n:
    nodenumbers.append(i.text)

X = root.findall(".//Nodes/X")
Y = root.findall(".//Nodes/Y")
Z = root.findall(".//Nodes/Z")

XYZ = []

#Put points in 3D
for h,i,j,k in zip(n,X,Y,Z):
    Pnt = Point(float(i.text.replace(",", "." )), float(j.text.replace(",", "." )), float(k.text.replace(",", "." )))
    #Pnt.id = int(h.text)
    XYZ.append(Pnt)

def getXYZ(nodenumber):
    rest = nodenumbers.index(nodenumber)
    return(rest)

test = getXYZ("176")

print(test)

#print(XYZ)
#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")

#PLATES

PlatesNumber = root.findall(".//Plates/Number")
PlatesNodes = root.findall(".//Plates/Node")

# for loop to get each element in an array

rootPlates = root.findall(".//Plates")

#XMLImportPlates(root):

PlatesTags = []
PlatesValues = []
for elements in root:
    if elements.tag == "Plates":
        for element in elements:
            PlatesTags.append(element.tag)
            PlatesValues.append(element.text)

#Iedere plate met nodes in een sublijst stoppen
    #plate
        #nodes

ind = [i for i, x in enumerate(PlatesTags) if x == "Number"] # indices where a new plate starts.

platesIndices = []
platesValues = []
platesNodes = []
count = 0
for x in ind:
    count = count + 1
    try:
        platesIndices.append(PlatesTags[x:ind[count]])
        platesValues.append(PlatesValues[x:ind[count]])
        platesNodes.append(PlatesValues[x+1:ind[count]-5])
    except:
        platesIndices.append(PlatesTags[x::]) # voor de laatste item uit de lijst, anders out of range
        platesValues.append(PlatesValues[x::]) # voor de laatste item uit de lijst, anders out of range
        platesNodes.append(PlatesValues[x+1:-5])

print(platesNodes)

#HOE NODES TE GROEPEREN
Perimeter = []
obj2 = []

for i in platesNodes:
    PlatePoints = []
    for j in i:
        PlatePoints.append(PointToSpecklePoint(XYZ[getXYZ(j)]))
    PlatePoints.append(PlatePoints[0])
    ply = SpecklePolyLine.from_points(PlatePoints)
    obj2.append(ply)

print(obj2)

#aanname: vlak vlak
# op basis van 3 punten een plane maken --> Vector.
# transformatie naar nulpunt
# Nee beter is om een extrusion: by.3d polycurve -->
#
Panel.byPolyCurveThickness()

# def byPolyCurveThickness(self, polycurve2D, thickness, start, directionvector, name):
#     self.directionvector = directionvector
#     self.name = name
#     self.thickness = thickness
#     self.start = start
#     self.extrusion = Extrusion().byPolyCurveHeightVector(PolyCurve2D, self.thickness, CSGlobal, start,
#                                                          self.directionvector)
#     self.numberFaces = self.extrusion[2]
#     self.verts = self.extrusion[0]
#     self.faces = self.extrusion[1]

#sys.exit()

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
SpeckleObjects = obj2
Message = "Shiny Commit"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)