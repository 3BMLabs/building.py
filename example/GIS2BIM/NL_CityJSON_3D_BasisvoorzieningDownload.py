from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
import os

#Download CityJSON Files of 3D Basisvoorziening

#SETTINGS
GISProject = BuildingPy("test")
ProjectDrive = "E:/"
ProjectFolder = ProjectDrive + "GIS2BIM/"
city = "Lekkerkerk"
street = "Voorstraat"
housenumber = "172"
ProjectName = city + "_" + street  + "_" + housenumber
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "werf van schouten", "501")
Bboxwidth = 200#m

#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX,RdY,Bboxwidth,Bboxwidth,0)

#Createprojectfolders
def CreateFolders(FolderList):
    for Folder in FolderList:
        os.mkdir(ProjectFolder + Folder + ProjectName + "/" + Folder)

#CITYJSON DOWNLOAD
def DownloadCityJSON():
    kaartbladenres = kaartbladenBbox(GISBbox)
    print(kaartbladenres)
    for i in kaartbladenres:
        downloadlink = NLPDOKKadasterBasisvoorziening3DCityJSONVolledig + i[0] + "_2020_volledig.zip"
        print(downloadlink)
        downloadUnzip(downloadlink, folderCityJSON + i[0] +".zip", folderCityJSON)

CreateFolders