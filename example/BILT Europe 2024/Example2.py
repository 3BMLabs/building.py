import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from bp_single_file import *

from exchange.speckle import *
from project.fileformat import *

proj = BuildingPy("BILT Europe 2024",2024)
streamid = CreateStream("speckle.xyz","BILT Europe 2024 2","description") #Create a new stream

f1 = Frame.by_startpoint_endpoint_profile(Point(0,0,0),Point(3000,0,0),"HEA400","HEA400+zeeg 20 mm", BaseSteel)
f2 = Frame.by_startpoint_endpoint_profile(Point(0,2000,0),Point(3000,2000,0),"UNP300","UNP300", BaseSteel)

proj.objects.append([f1,f2])

toSpeckle(proj,streamid,"my first shiny commit")
proj.toIFC("BILT_Example")