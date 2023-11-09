import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.struct4U import *
from objects.analytical import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

obj = []

#BEAMS
# obj.append(Frame.byStartpointEndpoint(Point(0,0,0), Point(2000,0,0), "UNP400", "UNP400-beam", 0, BaseConcrete))  #Concrete Beam
# obj.append(Frame.byStartpointEndpointProfileNameShapevector(Point(0,1000,0),Point(2000,1000,0),"HEA400","HEA400",Vector2(0,0),0,BaseSteel)) #Steel Beam

# obj.append(Panel.byBaselineHeight(Line(start=Point(4000,0,0),end=Point(4000,2000,0)),2500,250,"test",BaseConcrete.colorint))  #Panel as Wall
# obj.append(Frame.byStartpointEndpoint(Point(0,0,0),Point(2000,0,0),Rectangle("400x600",400,600).curve,"400x600",0,BaseConcrete))  #Concrete Beam
obj.append(Frame.byStartpointEndpointProfileName(Point(0,2000,0),Point(2000,2000,0),"HEA400","HEA400",BaseSteel))  #Steel Beam



# #PANELS/ PLATES IN XFEM4U
# obj.append(Panel.byPolyCurveThickness(
#     PolyCurve.byPoints(
#         [Point(4000,0,0),
#          Point(6000,0,0),
#          Point(6000,2000,0),
#          Point(4000,2000,0),
#          Point(4000,0,0)]),
#     200,
#     0,
#     "Plate"
#     ,BaseConcrete.colorint))

SpeckleHost = "3bm.exchange"
StreamID = "3e0d8773b3"
SpeckleObjects = obj
Message = "Elements"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)
