from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *

#Download GIS-files

#SETTINGS
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "werf van schouten", "501")
Bboxwidth = 1000 #m

#Download settings
DownloadBAG3D = False
Download3DBasisvoorzieningKadaster = False
DownloadWMS = False
DownloadBGT = True

#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX,RdY,Bboxwidth,Bboxwidth,0)

#BAG3D DOWNLOAD
if DownloadBAG3D is True:
    folderBAG3D = tempfolder + "BAG3D/"
    CreateDirectory(folderBAG3D)
    res = BAG3DDownload(GISBbox.boundingBoxString, folderBAG3D)
else:
    pass

#CITYJSON DOWNLOAD
if Download3DBasisvoorzieningKadaster is True:
    folderCityJSON = tempfolder + "cityJSON/"
    CreateDirectory(folderCityJSON)
    kaartbladenres = kaartbladenBbox(GISBbox)
    for i in kaartbladenres:
        downloadlink = NLPDOKKadasterBasisvoorziening3DCityJSONVolledig + i[0] + "_2020_volledig.zip"
        downloadUnzip(downloadlink, folderCityJSON + i[0] +".zip", folderCityJSON)
else:
    pass

#BGT DOWNLOAD
if DownloadBGT is True:
    folderBGT = tempfolder + "BGT/"
    CreateDirectory(folderBGT)
    BGTURL = bgtDownloadURL(RdX, RdY, Bboxwidth, Bboxwidth, 60)
    downloadUnzip(BGTURL,folderBGT + "BGT.zip", folderBGT)
else:
    pass
