import os
import sys
sys.path.append("C:/Users/iedereen/Documents/GitHub/building.py")
from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *

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
    kaartbladenres = kaartbladenBbox(GISBbox, FolderCityJSON)
    print(kaartbladenres)
    for i in kaartbladenres:
        downloadlink = NLPDOKKadasterBasisvoorziening3DCityJSONVolledig + i[0] + "_2020_volledig.zip"
        print(downloadlink)
        downloadUnzip(downloadlink, FolderCityJSON + i[0] +".zip", FolderCityJSON)

def GetWebServerDataCategorised():
	#Get webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data_Categorised.json"
	url = urllib.request.urlopen(Serverlocation)
	jsonData = json.loads(url.read())['GIS2BIMserversRequests']["NLwebserverRequests"]["NLWMS"]
	return jsonData

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

def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

def GetWebServerDataCategorisedService(category,service):
	#Get a list with webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests']
	listOfData = []
	for i in data:
		if i["service"] == service:
			listOfData.append(i)
	return listOfData

#WMS
jsonobj=GetWebServerDataCategorised()
serverrequestprefix= extract_values(jsonobj, 'serverrequestprefix')
title = extract_values(jsonobj, 'title')
print("itemstodownload: " + str(len(serverrequestprefix)))
for i in range(len(serverrequestprefix)):
    itemserverrequestprefix=serverrequestprefix[i]
    itemtitle=title[i]
    #print(itemtitle + " : " + itemserverrequestprefix + Bbox)
    #def WMSRequest(serverName,boundingBoxString,fileLocation,pixWidth,pixHeight):

    print(FolderImages + "/"+ itemtitle +".png")
    #GIS2BIM.WMSRequest(itemserverrequestprefix, Bbox, FolderImages + "/"+ itemtitle +".png", 2000, 2000)