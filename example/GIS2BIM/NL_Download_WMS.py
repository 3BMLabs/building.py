from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
import math
#Download a lot of WMS

#SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "lange geldersekade", "2")
Bboxwidth = 200 #m

#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX,RdY,Bboxwidth,Bboxwidth,0)

