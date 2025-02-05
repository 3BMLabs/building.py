import sys
import os
from pathlib import Path



from project.fileformat import *
from construction.beam import Beam
from construction.analytical import *
from construction.panel import *
from construction.datum import *
from library.profile import *
from exchange.struct4U import *
from library.material import *
from exchange.speckle import *

project = BuildingPy("Struct4U Example file","0")

height = 3200

#CREATE GRIDSYSTEM
gridinput =  ["0 1000 1000",seqChar,"0 4x3600",seqNumber,"0"]

#CONCRETE BEAM

project.objects.append(Beam().by_startpoint_endpoint(Point(0,0,0),Point(0,14400,0),Rectangle("350x500",350,500).curve,"350x500",0,BaseConcrete))
project.objects.append(Beam.by_startpoint_endpoint(Point(0,14400,0),Point(2000,14400,0),Rectangle("350x500",350,500).curve,"350x500",0,BaseConcrete))

project.objects.append(Beam.by_startpoint_endpoint_rect(Point(0,14400,0),Point(2000,14400,0)))


#STEEL COLUMN
project.objects.append(Beam.by_startpoint_endpoint_profile_shapevector(Point(2000,14400,0),Point(2000,14400,height),"HEA160","HEA160",Vector2(0,0),0,BaseSteel,"Frame"))

#STEEL FRAMES
x = 1000
y = 0
for i in range(5):
    project.objects.append(Beam.by_startpoint_endpoint_profile_shapevector(Point(0,y,0),Point(0,y,height),"HEA180","HEA180",Vector2(0,0),90,BaseSteel,"Frame")) # column
    project.objects.append(Beam.by_startpoint_endpoint_profile_shapevector(Point(0,y,height),Point(x,y,height),"HEA180","HEA180",Vector2(0,0),0,BaseSteel,"Frame")) # beam
    x = x + 250
    y = y + 3600

#LOADS
#PLATE IN XFEM4U
project.objects.append(Panel.by_polycurve_thickness(
    PolyCurve.by_points(
        [Point(0,0,height),
         Point(0,14400,height),
         Point(2000,14400,height),
         Point(1000,0,height),
         Point(0,0,height)]),
    100,
    0,
    "Plate"
    ,BaseConcrete.colorint))

#CREATE XML-FILE
pathxml = "C:/Users/Jonathan/Desktop/TEMP/test1.xml"
createXFEM4UXML(project,pathxml,gridinput)

OpenXMLXFEM4U(pathxml)

#project.toSpeckle("7603a8603c", "My shiny commit for Struct4U")