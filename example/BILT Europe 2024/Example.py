from bp_single_file import *
from exchange.speckle import *

#if you use Speckle, Speckle Manager should be installed

proj = BuildingPy("BILT Europe 2024",2024)
proj.round = True

#streamid = CreateStream("speckle.xyz","BILT Europe 2024 2","description") #Create a new stream
streamid = "741e99afbe"
#print(streamid)Example.py

p1 = Point(0,0,0)
p2 = Point(3000,1000,1000)

l1 = Line(p1,p2)

print(l1.length)

p1 = Point2D(0,0)
p2 = Point2D(300,0)
#PolyCurve.by

Frame1 = Frame.by_startpoint_endpoint_profile(Point(0,0,0),Point(3000,0,0),"HEA400","HEA400+zeeg 20 mm", BaseSteel)

proj.objects.append(Frame1)

toSpeckle(proj,streamid,"my first shiny commit")