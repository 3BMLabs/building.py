from packages.GIS2BIM import GIS2BIM
from packages.GIS2BIM.GIS2BIM_NL import *
from project.fileformat import *
from exchange.GIS2BIM import *

from geometry.curve import *

GISProject = BuildingPy("test")

lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "werf van schouten", "501")
RdX = lst[0]
RdY = lst[1]
Bboxwidth = 500 #m
bboxString = GIS2BIM.CreateBoundingBox(RdX,RdY,Bboxwidth,Bboxwidth,0)

curvesCadaster = GIS2BIM.PointsFromWFS(NLPDOKCadastreCadastralParcels,bboxString,NLPDOKxPathOpenGISposList,-RdX,-RdY,1000,2)
curvesBAG = GIS2BIM.PointsFromWFS(NLPDOKBAGBuildingCountour,bboxString,NLPDOKxPathOpenGISposList,-RdX,-RdY,1000,2)

#KADASTRALE GRENZEN
for i in WFSCurvesToBPCurves(curvesBAG):
    GISProject.objects.append(i)

GISProject.toSpeckle("30185b86c3","Kadaster")
