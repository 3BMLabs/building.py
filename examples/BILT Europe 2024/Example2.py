


from construction.beam import *
from construction.floor import *
from exchange.speckle import *
from project.fileformat import *

project = BuildingPy("BILT Europe 2024",2024)
streamid = CreateStream("speckle.xyz","BILT Europe 2024 2","description")

f1 = Beam.by_startpoint_endpoint_profile(Point(0,0,0),Point(3000,0,0),"HEA400","HEA400+zeeg 20 mm", BaseSteel)
f2 = Beam.by_startpoint_endpoint_profile(Point(0,2000,0),Point(3000,2000,0),"UNP300","UNP300", BaseSteel)
project.objects.append([f1,f2])

#inclusive floor
floor_instance = Floor()
floor_instance.points = [Point(0, 0, 0), Point(10, 0, 0), Point(18, 5, 0), Point(0, 5, 0)]
project.objects.append(floor_instance)


toSpeckle(project,streamid,"my first shiny commit")
project.to_IFC("BILT_Example")