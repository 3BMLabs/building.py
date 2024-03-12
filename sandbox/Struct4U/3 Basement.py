from objects.datum import *
from exchange.struct4U import *
from library.material import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# GridSystem
seqX = "A B C D E"
seqY = "1 2 3 4 5"
ext = 2000 #extension grid

#INPUT in mm
width = 5000
length = 8500
height = 2600
floorThickness = 200
wallThickness = 160

#Grids
xstr = "0 " + str(width)
ystr = "0 " + str(length)
grids = GridSystem(xstr, seqX, ystr, seqY, ext)
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
Commit = TransportToSpeckle("struct4u.xyz", "9fd1692151", SpeckleObj, "Parametric Concrete Basement")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Concrete Basement")
xmlS4U.addLoadCasesCombinations()
xmlS4U.addGrids(xstr,seqX,ystr,seqY,0) # Grids
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/3 Concrete Basement/Concrete Basement.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()