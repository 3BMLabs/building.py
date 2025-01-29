from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from exchange.GIS2BIM import *
from geometry.mesh import Mesh
#from packages.GIS2BIM.GIS2BIM_Blender import *
from library.material import *
from exchange.image_to_mesh import *
import sys

# Description
# This script creates lines for the cadastral parcels and a mesh for a building footprint for any building in
# the Netherlands based on an address.

# SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL, "Dordrecht", "werf van schouten", "501")
Bboxwidth = 300  # Meter

# MODEL/DRAWING SETTINGS
Centerline2 = ["Center Line 2", [8, 4, 4, 4], 250]  # Rule: line, whitespace, line whitespace etc., scale

# BASE VALUES
RdX = lst[0]
RdY = lst[1]
Bbox = CreateBoundingBox(RdX, RdY, Bboxwidth, Bboxwidth, 0)

NLPDOKCadastreCadastralParcels = "http://service.pdok.nl/kadaster/kadastralekaart/wfs/v5_0?service=WFS&version=2.0.0&request=GetFeature&typeName=perceel&bbox="

# Aerialphoto
#fileLocationWMS = tempfolder + "luchtfoto_2020_2.png"
#a = GIS2BIM.WMSRequest(GIS2BIM.GetWebServerData("NL_PDOK_Luchtfoto_2020_28992", "webserverRequests","serverrequestprefix"), Bbox, fileLocationWMS,1500, 1500)

# img = imagePyB().by_file(fileLocationWMS,Bboxwidth*1000,Bboxwidth*1000,0,0,0)
# GISProject.objects.append(img)

# KADASTRALE GRENZEN
curvesCadaster = GIS2BIM.PointsFromWFS(NLPDOKCadastreCadastralParcels, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY,
                                       1000, 2)
# for i in WFSCurvesToBPCurvesLinePattern(curvesCadaster, Centerline):
for i in WFSCurvesToBPCurves(curvesCadaster):
    for j in i.curves:
        GISProject.objects.append(j)

    # linepattern
    #j = polycurve_to_pattern(i,Centerline2)
    #for k in j:
    #    GISProject.objects.append(k)

# GEBOUWEN
curvesBAG = GIS2BIM.PointsFromWFS(NLPDOKBAGBuildingCountour, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY, 1000, 2)
BPCurvesBAG = WFSCurvesToBPCurves(curvesBAG)
# for i in WFSCurvesToBPCurves(curvesBAG):
#     GISProject.objects.append(i)

for i in BPCurvesBAG:
    m = Mesh().by_polycurve(i, "BAG:pand", BaseBuilding)
    GISProject.objects.append(m)

#GISProject.toSpeckle("30185b86c3", "Kadaster")

