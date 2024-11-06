import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from construction.frame import *
from exchange.scia import *
from exchange.struct4U import *

from construction.analytical import *
from project.fileformat import *

start_list = [Point(302,192,0),Point(382,102,3000),Point(10000,392,0),Point(3029,0,0)]
end_list = [Point(0,0,0),Point(382,1023,391),Point(10000,392,2000),Point(3092,2913,3921)]
profile_name = "HEA100"

for start, end in zip(start_list, end_list):
    frame1 = Frame.by_startpoint_endpoint_profile(start, end, "HEA100", "None", BaseSteel)
    project.objects.append(frame1)


xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(project.objects) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Industrial Hall")
xmlS4U.convert_panels_to_xml() #add Load Panels
xmlS4U.addGrids() # Grids
xmlS4U.addSurfaceLoad()

xmlS4U.XML()
XMLString = xmlS4U.xmlstr

# filepath = "C:/Users/Jonathan/Desktop/test.xml"
# file = open(filepath, "w")
# a = file.write(XMLString)
# file.close()

# project.toSpeckle("7603a8603c")