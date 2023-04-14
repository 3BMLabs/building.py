from objects.frame import *
from objects.datum import *
from objects.analytical import *
from exchange.struct4U import *
from abstract.coordinatesystem import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 2000 #extension grid

#INPUT in mm
spac_x = 3500 #grid spacing X
nx = 6 # number of grids X

spac_y = 3500 #grid spacing Y
ny = 5 # number of grids Y
floorthickness = 200

width = spac_x * nx

height = spac_y * ny
spacX = "0 " + str(nx) + "x" + str(spac_x)  #example "13x5400"
spacY = "0 " + str(ny) + "x" + str(spac_y)  # example "4x5400"
grids = GridSystem(spacX, seqX, spacY, seqY, ext)
obj = grids[0] + grids[1] #list with objects

#Concretefloor
obj.append(Panel.byPolyCurveThickness(
    Rect(Vector3(0,0,0),width,height),
    floorthickness,
    0,
    "Concrete Floor",
    BaseConcrete.colorint))

#Supports
x = 0
y = 0
for i in range(nx):
    for j in range(ny):
        sup = Support()
        sup.Point = Point(x,y,0)

x = 0
for i in range(nx+1):
    y = 0
    for j in range(ny+1):
        sup = Support()
        sup.Point = Point(x, y, 0)
        sup.Tz = "S"
        sup.Kz = 35000
        obj.append(sup)
        y = y + spac_y
    x = x + spac_x

#Loads

#Load cases
LC1 = LoadCase()
LC1.Number = 1
LC1.Description = "Dead Load"
LC1.Type = 0

LC2 = LoadCase()
LC2.Number = 2
LC2.Description = "Chessboard 1"
LC2.Type = 1
LC2.psi0 = 0.4
LC2.psi1 = 0.5
LC2.psi2 = 0.3

LC3 = LoadCase()
LC3.Number = 3
LC3.Description = "Chessboard 2"
LC3.Type = 1
LC3.psi0 = 0.4
LC3.psi1 = 0.5
LC3.psi2 = 0.3

obj.append(LC1)
obj.append(LC2)
obj.append(LC3)

#Surfaceload

obj.append(ChessBoardSurfaceLoadsRectangle(0,0,spac_x*2,spac_y*2,6,6,spac_x,spac_y,1,-20,obj))

print(obj)
#sys.exit()
#Export to Speckle
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "de68169deb", SpeckleObj, "4 Concrete Floor")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Concrete floor with loads")
xmlS4U.addGrids(spacX,seqX,spacY,seqY,0) # Grids
xmlS4U.addLoadCasesCombinations()
xmlS4U.addSurfaceLoad(obj)
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/4 Concrete Floor/Concrete Floor.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()