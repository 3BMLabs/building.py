import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

import xml.etree.ElementTree as ET
tree = ET.parse("temp/test135.xml")
root = tree.getroot()

from exchange.speckle import *
from geometry.curve import Line
from geometry.point import Point
from objects.frame import Frame
from exchange.XFEM4U.xfem4unames import *


def getGridDistances(Grids):
    GridsNew = []
    distance = 0.0
    #GridsNew.append(distance)
    for i in Grids:
        #del Grids[0]
        if "x" in i:
            spl = i.split("x")
            count = int(spl[0])
            width = float(spl[1])
            for i in range(count):
                distance = distance + width
                GridsNew.append(distance)
        else:
            distance = distance + float(i)
            GridsNew.append(distance)
    return GridsNew

#List for SpeckleObjects
obj = []

#GRIDS
GridEx = 1000

GridsX = root.findall(".//Grids/X")[0].text.split()
GridsX = getGridDistances(GridsX)
Xmax = max(GridsX)
GridsXLable = root.findall(".//Grids/X_Lable")[0].text.split()
GridsY = root.findall(".//Grids/Y")[0].text.split()
GridsY = getGridDistances(GridsY)
Ymax = max(GridsY)
GridsYLable = root.findall(".//Grids/Y_Lable")[0].text.split()
GridsZ = root.findall(".//Grids/Z")[0].text.split()
GridsZ = getGridDistances(GridsZ)
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
X = root.findall(".//Nodes/X")
Y = root.findall(".//Nodes/Y")
Z = root.findall(".//Nodes/Z")

XYZ = []

#Put points in 3D
for h,i,j,k in zip(n,X,Y,Z):
    Pnt = Point(float(i.text), float(j.text), float(k.text))
    #Pnt.id = int(h.text)
    XYZ.append(Pnt)

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")


for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
    profile_name = ProfileName[int(k.text)-1].text
    if profile_name == None:
        pass
    else:
        frame = Frame()
        start = XYZ[int(i.text)-1]
        end = XYZ[int(j.text)-1]
        profile = matchprofile(profile_name)
        try:
            frame.byStartpointEndpointProfileName(start, end, profile, profile_name + "-" + l.text)
        except:
            pass
        test = SpeckleMeshByMesh(frame)
        obj.append(test)

#PLATES

PlatesNumber = root.findall(".//Plates/Number")
PlatesNodes = root.findall(".//Plates/Node")

PlatePoints = []
# for loop to get each element in an array

rootPlates = root.findall(".//Plates")

XMLelements = []
for elem in rootPlates:
    XMLelements.append(elem.text)

print(XMLelements)

#HOE NODES TE GROEPEREN

for i in PlatesNodes:
    PlatePoints.append(XYZ[int(i.text)-1])


SpeckleHost = "3bm.exchange" # struct4u.xyz
StreamID = "55758e05ae" #c4cc12fa6f
SpeckleObjects = obj
Message = "Github 2023"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)