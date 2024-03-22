from packages.GIS2BIM.GIS2BIM_NL import *
from project.fileformat import *
from exchange.GIS2BIM import *
from geometry.mesh import MeshPB
from library.material import *
from abstract.image import *

# Description
# This script creates lines for the BGT

# SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL, "Dordrecht", "werf van schouten", "501")
Bboxwidth = 500  # Meter

# MODEL/DRAWING SETTINGS
Centerline2 = ["Center Line 2", [8, 4, 4, 4], 500]  # Rule: line, whitespace, line whitespace etc., scale

# BASE VALUES
RdX = lst[0]
RdY = lst[1]
Bbox = GIS2BIM.CreateBoundingBox(RdX, RdY, Bboxwidth, Bboxwidth, 0)

DownloadBGT = bgtDownloadURL(RdX,RdY,Bboxwidth,Bboxwidth,60)
