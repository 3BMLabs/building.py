from bp_single_file import *
from exchange.speckle import *

#if you use Speckle, Speckle Manager should be installed

proj = project("BILT Europe 2024",2024)
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
p3 = Point2D(300,300)
p4 = Point2D(0,300)

pc2d1 = PolyCurve2D.by_points([p1,p2,p3,p4])

l1 = Line2D(p1,p2)
l2 = Line2D(p2,p3)
l3 = Line2D(p3,p4)
l4 = Arc2D(p4,Point2D(-50,150),p1)

pc2d2 = PolyCurve2D.by_joined_curves([l1,l2,l3,l4])

Frame1 = Frame.by_startpoint_endpoint_profile(Point(0,0,0),Point(3000,0,0),"HEA400","HEA400+zeeg 20 mm", BaseSteel)
Frame2 = Frame.by_point_height_rotation(Point(0,1000,0),3000,pc2d1,"my shiny profile 1",0,BaseConcrete,)
Frame3 = Frame.by_point_height_rotation(Point(0,2000,0),3000,pc2d2,"my shiny profile 2",0,BaseConcrete,)

proj.objects.append([Frame1, Frame2, Frame3])

toSpeckle(proj,streamid,"my first shiny commit")
