from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *

#Download GIS-files

#SETTINGS
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "werf van schouten", "501")
Bboxwidth = 1000 #m

#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX,RdY,Bboxwidth,Bboxwidth,0)

#CREATE FOLDERS
folderBAG3D = tempfolder + "BAG3D/"
folderCityJSON = tempfolder + "cityJSON/"
CreateDirectory(folderBAG3D)
CreateDirectory(folderCityJSON)

#BAG3D DOWNLOAD
res = BAG3DDownload(GISBbox.boundingBoxString, folderBAG3D)
kaartbladenres = kaartbladenBbox(GISBbox)

#CITYJSON DOWNLOAD
for i in kaartbladenres:
    downloadlink = NLPDOKKadasterBasisvoorziening3DCityJSONVolledig + i[0] + "_2020_volledig.zip"
    downloadUnzip(downloadlink, folderCityJSON + i[0] +".zip", folderCityJSON)

#BGT DOWNLOAD

