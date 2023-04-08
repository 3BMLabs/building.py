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

height = spac_y*ny
spacX = str(nx+1) + "x" + str(spac_x)  #example "13x5400"
spacY = str(ny+1) + "x" + str(spac_y)  # example "4x5400"
grids = GridSystem(spacX, seqX, spacY, seqY, ext)
obj = grids[0] + grids[1] #list with objects

#Concretefloor
obj.append(Panel.byPolyCurveThickness(
    PolyCurve.byPoints(
        [Point(0,0,0),
         Point(width,0,0),
         Point(width,height,0),
         Point(0,height,0),Point(0,0,0)]),
    floorthickness,
    0,
    "Betonvloer",
    BaseConcrete.colorint))

#Supports
sup = Support(Number = 0)
Line
#Export to Speckle
SpeckleObj = translateObjectsToSpeckleObjects(obj)
#Commit = TransportToSpeckle("struct4u.xyz", "de68169deb", SpeckleObj, "Parametric Structure.py")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Industrial Hall")
xmlS4U.addGrids(spacX,seqX,spacY,seqY,0) # Grids
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/Concrete Floor/Concrete Floor.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()