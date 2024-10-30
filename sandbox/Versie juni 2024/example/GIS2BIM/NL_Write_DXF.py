from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from packages.GIS2BIM import *
from project.fileformat import *
from exchange.GIS2BIM import *

from geometry.mesh import Mesh
from library.material import *
import ezdxf

# Description
# This script creates lines for the cadastral parcels and a mesh for a building footprint for any building in
# the Netherlands based on an address.

#DXF SETTINGS
doc = ezdxf.new('R2010')
msp = doc.modelspace() # add new entities to the modelspace

# SETTINGS
GISProject = BuildingPy("DXF Kadaster")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL, "Dordrecht", "werf van schouten", "501")
Bboxwidth = 500  # Meter
folderKadaster = tempfolder + "kadaster/"
CreateDirectory(folderKadaster)
dxfFile = folderKadaster + "GIS2BIM_kadaster.dxf"

# MODEL/DRAWING SETTINGS
Centerline2 = ["Center Line 2", [8, 4, 4, 4], 500]  # Rule: line, whitespace, line whitespace etc., scale

# BASE VALUES
RdX = lst[0]
RdY = lst[1]
Bbox = GIS2BIM.CreateBoundingBox(RdX, RdY, Bboxwidth, Bboxwidth, 0)

# KADASTRALE GRENZEN
curvesCadaster = GIS2BIM.PointsFromWFS(NLPDOKCadastreCadastralParcels, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY, 1000, 2)
# for i in WFSCurvesToBPCurvesLinePattern(curvesCadaster, Centerline):
for i in WFSCurvesToBPCurves(curvesCadaster):
    GISProject.objects.append(i)

# GEBOUWEN
curvesBAG = GIS2BIM.PointsFromWFS(NLPDOKBAGBuildingCountour, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY, 1000,2)
BPCurvesBAG = WFSCurvesToBPCurves(curvesBAG)

for i in WFSCurvesToBPCurves(curvesBAG):
    GISProject.objects.append(i)
    n = 0
    try:
     for j in i.points:
         start = Point.to_matrix(i.points[n])
         end = Point.to_matrix(i.points[n+1])
         msp.add_line(start, end)
         n = n + 1
    except:
        pass

doc.saveas(dxfFile)