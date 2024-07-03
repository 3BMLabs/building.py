from objects.frame import *
from exchange.struct4U import *
from objects.analytical import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

obj = []

#BEAMS
obj.append(Frame.by_startpoint_endpoint(Point(0,0,0),Point(2000,0,0),Rectangle("400x600",400,600).curve,"400x600",0,BaseConcrete))  #Concrete Beam
obj.append(Frame.by_startpoint_endpoint_profile(Point(0,2000,0),Point(2000,2000,0),"HEA400","HEA400",BaseSteel))  #Steel Beam

#SURFACE LOAD
obj.append(SurfaceLoad.by_load_case_polycurve_q(
    1,
    Rect(Vector3(0,0,0),2000,2000),
    2.5)
)

#PANELS/ PLATES IN XFEM4U
obj.append(Panel.by_baseline_height(Line(start=Point(4000,0,0),end=Point(4000,2000,0)),2500,250,"test",BaseConcrete.colorint))  #Panel as Wall
obj.append(Panel.by_polycurve_thickness(
    PolyCurve.by_points([Point(6000,0,0),Point(8000,0,0),Point(8000,2000,0),Point(6000,2000,0),Point(6000,0,0)]),
    200,0,"Plate",BaseConcrete.colorint))

#SUPPORTS
obj.append(Support.pinned(Point(0,0,0)))
obj.append(Support.pinned(Point(2000,0,0)))
obj.append(Support.pinned(Point(0,2000,0)))
obj.append(Support.pinned(Point(2000,2000,0)))

#LOADPANELS
LP = LoadPanel()
LP.PolyCurve = Rect(Vector3(0,0,0),2000,2000)
LP.SurfaceType = "Wall"
LP.Description = "test"
LP.LoadBearingDirection = "Y"

obj.append(LP)

SpeckleObj = translateObjectsToSpeckleObjects(obj)
#Commit = TransportToSpeckle("struct4u.xyz", "dc2ae20e64", SpeckleObj, "Examples.py")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Examples of building.py")
xmlS4U.addPanels(obj) #add Load Panels
xmlS4U.addSurfaceLoad(obj)

xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/Examples buildingpy/Example.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()