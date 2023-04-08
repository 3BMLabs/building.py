from objects.frame import *
from objects.datum import *
from exchange.struct4U import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 2000 #extension grid

#INPUT in mm
width = 5000
length = 7000
height = 2600
floorThickness = 200
wallThickness = 160

#Grids
grids = GridSystem("0 " + str(width), seqX, "0 " + str(length), seqY, ext)
obj = grids[0] + grids[1] #list with objects

#Concretefloor
obj.append(Panel.byPolyCurveThickness(
    PolyCurve.byPoints(
        [Point(0,0,0),
         Point(width,0,0),
         Point(width,length,0),
         Point(0,length,0),Point(0,0,0)]),
    floorThickness,
    0,
    "Floor",
    BaseConcrete.colorint))
obj.append(Panel.byPolyCurveThickness(PolyCurve.byPoints([Point(0,0,0),Point(width,0,0),Point(width,0,height),Point(0,0,height),Point(0,0,0)]),wallThickness,0,"Wall 1",BaseConcrete.colorint)) # Wall 1
obj.append(Panel.byPolyCurveThickness(PolyCurve.byPoints([Point(0,length,0),Point(width,length,0),Point(width,length,height),Point(0,length,height),Point(0,length,0)]),wallThickness,0,"Wall 2",BaseConcrete.colorint)) # Wall 2
obj.append(Panel.byPolyCurveThickness(PolyCurve.byPoints([Point(0,0,0),Point(0,length,0),Point(0,length,height),Point(0,0,height),Point(0,0,0)]),wallThickness,0,"Wall 3",BaseConcrete.colorint)) # Wall 3
obj.append(Panel.byPolyCurveThickness(PolyCurve.byPoints([Point(width,0,0),Point(width,length,0),Point(width,length,height),Point(width,0,height),Point(width,0,0)]),wallThickness,0,"Wall 4",BaseConcrete.colorint)) # Wall 4


#Export to Speckle
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "9fd1692151", SpeckleObj, "Parametric Structure.py")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Concrete Basement")
xmlS4U.addGrids(spacX,seqX,spacY,seqY,0) # Grids
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/Concrete Basement/Concrete Basement.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()