from construction.beam import *
from exchange.struct4U import *
from abstract.vector import *
from abstract.coordinatesystem import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

Height = 3000
Radius = 1200
NumberOfTreads = 16
DegreesSpiral = 270
Column = "K150/150/10"
Tread = "S120/10"
obj = []

obj.append(Beam.by_startpoint_endpoint_profile(Point(0,0,0),Point(0,0,Height),Column,"spiral",BaseSteel)) #Spiral

deg = 0
x = 0
y = Radius
dz = Height / NumberOfTreads
z = dz
p2 = Point(x, y, z)
ddeg = DegreesSpiral / NumberOfTreads

for i in range(NumberOfTreads):
    obj.append(Beam.by_startpoint_endpoint_profile_justification(Point(0, 0, z), p2, Tread, "Tread","Center","Center",0, BaseSteel))  # Treads
    p2 = Point.rotate_XY(p2, ddeg, dz)
    z = z + dz

SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "4bb051dcbb", SpeckleObj, "Parametric Spiral Staircase.py")

#Export to XFEM4U XML String

xmlS4U = xmlXFEM4U()
xmlS4U.addBeamsPlates(obj)
xmlS4U.addProject("Struct4U Parametric Stair")
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/5 Stair Beams/stair.xml"
file = open(filepath, "w")
a = file.write(XMLString)

file.close()