from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from project import fileformat
from construction.datum import *
from geometry.systemsimple import *

project = BuildingPy("Project test BuildingPy","0")

#Beam1 = Frame.by_startpoint_endpoint_profile(Point(0,0,0),Point(3000,0,0),"HEA200","HEA200",BaseSteel)

Beam2 = Frame.by_startpoint_endpoint_profile(Point(0,0,500),Point(0,0,1000),"HEA200","test",BaseSteel)
#test = searchProfile("SHS60/60/4.0")

#print(test.shape_coords)
#project.objects.append(Beam1)

#project.toSpeckle("f66b54f6c4")