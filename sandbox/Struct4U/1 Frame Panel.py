from construction.beam import *
from exchange.struct4U import *
from construction.analytical import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

obj = []

#BEAMS
obj.append(Beam.by_startpoint_endpoint(Point(0,0,0), Point(2000,0,0), Rectangle("400x600", 400,600).curve,"400x600",0,BaseConcrete))  #Concrete Beam
obj.append(Beam.by_startpoint_endpoint_profile_shapevector(Point(0,1000,0),Point(2000,1000,0),"HEA400","HEA400",Vector2(0,0),0,BaseSteel)) #Steel Beam

obj.append( #List with elements to Speckle
    Beam.by_startpoint_endpoint_profile_shapevector(  #Function to create a Frame/Beam
        Point(0,2000,0), #Startpoint
        Point(2000,2000,0), #Endpoint
        "UNP400", #Steel profile name, can be hea400, he400a, HEA400, HEA 400 etc.
        "UNP400-beam",
        Vector2(0,0),
        45, #
        BaseSteel))


#PANELS/ PLATES IN XFEM4U
obj.append(Panel.by_polycurve_thickness(
    PolyCurve.by_points(
        [Point(4000,0,0),
         Point(6000,0,0),
         Point(6000,2000,0),
         Point(4000,2000,0),
         Point(4000,0,0)]),
    200,
    0,
    "Plate"
    ,BaseConcrete.colorint))

SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "558206cfda", SpeckleObj, "Examples.py")
