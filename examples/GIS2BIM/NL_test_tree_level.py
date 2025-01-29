from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from geometry.curve import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
import math

#SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "lange geldersekade", "2")
Bboxwidth = 200 #m

# meshlst = [[[[8252, 2129, 1520], [-6735, 1188, 1520], [8753, -5855, 1520]]], [[[-6735, 1188, 1520], [-6234, -6796, 1520], [8753, -5855, 1520]]], [[[8252, 2129, 870], [8753, -5855, 1520], [8753, -5855, 870]]], [[[8252, 2129, 870], [8252, 2129, 1520], [8753, -5855, 1520]]], [[[8753, -5855, 870], [-6234, -6796, 1520], [-6234, -6796, 870]]], [[[8753, -5855, 870], [8753, -5855, 1520], [-6234, -6796, 1520]]], [[[-6234, -6796, 870], [-6735, 1188, 1520], [-6735, 1188, 870]]], [[[-6234, -6796, 870], [-6234, -6796, 1520], [-6735, 1188, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 1520], [8252, 2129, 870]]], [[[-6735, 1188, 870], [-6735, 1188, 1520], [8252, 2129, 1520]]], [[[-6735, 1188, 870], [8252, 2129, 870], [8753, -5855, 870]]], [[[-6234, -6796, 870], [-6735, 1188, 870], [8753, -5855, 870]]]]

center = Point(0,0,1000)
straal = 500
segments = 15

dx = 0
dy = 0
dz = 0


alpha = -90

#Single curv
pnts = []
for i in range(segments+1):
    x = straal * math.cos(math.radians(alpha)) + dx
    z = straal * math.sin(math.radians(alpha)) + dz
    alpha = alpha + 180/segments
    y = dy
    pnt = Point(x,y,z)
    pnts.append(pnt)
    #GISProject.objects.append(pnt)

pnts_rot = []

angle = 0
for j in range(segments+1):
    for i in pnts:
        pnt = Point.rotate_XY(i,angle,0)
        GISProject.objects.append(pnt)
    angle = angle + 360/segments

GISProject.to_speckle("cc80144920")

