import os
import sys
sys.path.append("C:/Users/iedereen/Documents/GitHub/building.py")
from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
import ssl

#SETTINGS BASIS
GISProject = BuildingPy("test")
ProjectDrive = "E:/"
ProjectFolder = ProjectDrive + "GIS2BIM/"
City = "Lekkerkerk"
Street = "Voorstraat"
HouseNumber = "172"
ProjectName = City + "_" + Street  + "_" + HouseNumber
lst = NL_GetLocationData(NLPDOKServerURL, City, Street, HouseNumber)
Bboxwidth = 200#m
#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
Bbox = GIS2BIM.CreateBoundingBox(RdX,RdY,Bboxwidth,Bboxwidth,0)
print(Bbox)

def CreateFolder(Folder):
    if not os.path.isdir(Folder):
        print(Folder + ": " + str(os.path.isdir(Folder)))
        os.mkdir(Folder)

#Createprojectfolders
MainProjectFolder =  ProjectFolder + ProjectName
CreateFolder(MainProjectFolder)
FolderOBJ = MainProjectFolder  + "/OBJ"
CreateFolder(FolderOBJ)
FolderImages = MainProjectFolder  + "/Images"
CreateFolder(FolderImages)
FolderBGT = MainProjectFolder  + "/BGT"
CreateFolder(FolderBGT)
FolderCityJSON = MainProjectFolder  + "/CityJSON"
CreateFolder(FolderCityJSON)
FolderAHN = MainProjectFolder  + "/AHN"
CreateFolder(FolderAHN )

#CITYJSON DOWNLOAD
def DownloadCityJSON():
    kaartbladenres = kaartbladenBbox(Bbox, FolderCityJSON)
    print(kaartbladenres)
    for i in kaartbladenres:
        downloadlink = NLPDOKKadasterBasisvoorziening3DCityJSONVolledig + i[0] + "_2020_volledig.zip"
        print(downloadlink)
        downloadUnzip(downloadlink, FolderCityJSON + i[0] +".zip", FolderCityJSON)

def WMSRequestNew(serverName,boundingBoxString,fileLocation,pixWidth,pixHeight):
    # perform a WMS OGC webrequest( Web Map Service). This is loading images.
    context = ssl._create_unverified_context()
    myrequestURL = serverName + boundingBoxString
    myrequestURL = myrequestURL.replace("width=3000", "width=" + str(pixWidth))
    myrequestURL = myrequestURL.replace("height=3000", "height=" + str(pixHeight))
    resource = urllib.request.urlopen(myrequestURL, context=context)
    output1 = open(fileLocation, "wb")
    output1.write(resource.read())
    output1.close()
    return fileLocation, resource, myrequestURL

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    """Recursively search for values of key in JSON tree."""
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results

def GetWebServerDataCategorised(obj1, obj2, obj3):
	#Get webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data_Categorised.json"
	url = urllib.request.urlopen(Serverlocation)
	jsonData = json.loads(url.read())[obj1][obj2][obj3]
	return jsonData

#WMS
jsonobj=GetWebServerDataCategorised("GIS2BIMserversRequests", "NLwebserverRequests", "NLWMS")
serverrequestprefix= extract_values(jsonobj, 'serverrequestprefix')
title = extract_values(jsonobj, 'title')
print("ItemsToDownload: " + str(len(serverrequestprefix)))
print(FolderImages)
for i in range(len(serverrequestprefix)):
    itemserverrequestprefix=serverrequestprefix[i]
    itemtitle=title[i]
    print(itemtitle)
    WMSRequestNew(itemserverrequestprefix, Bbox, FolderImages + "/"+ itemtitle +".png", 1500, 1500)