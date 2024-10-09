import os
import sys
sys.path.append("../building.py")
#print(sys.path)
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
=======
from packages.GIS2BIM.GIS2BIM_CityJSON import *
import time
import ijson
from library.material import *
from geometry.mesh import *
import certifi
import ssl


def CreateFolder(Folder):
    #check and ccreate folders
    if not os.path.isdir(Folder):
        print(Folder + ": " + str(os.path.isdir(Folder)))
        os.mkdir(Folder)

#CITYJSON DOWNLOAD

def DownloadCityJSON():
    kaartbladenres = kaartbladenBbox(Bbox, FolderCityJSON)
=======
def DownloadCityJSON(Bbox, FolderCityJSON):
    kaartbladenres = kaartbladenBbox(Bbox)

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
=======
def GetWebServerDataSettings(SettingsfileLocation):
    #get settings
    url = urllib.request.urlopen(SettingsfileLocation)
    jsonData = json.loads(url.read())['Settings']
    print(jsonData)
    return jsonData

def DownloadWMSBasis(Bbox, FolderImages):
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

def Kadaster3DBasisvoorziening(result, GISProject):
    #3D KADASTER BASISVOORZIENING

    resultparser = result

    # 0 buildings LOD 1
    #for i in example[0]:
    #    geom = i["geometry"]
    #    name = i["attributes"]["cadastre_id"]
    #    m = MeshPB().by_coords(geom, name, BaseBuilding, True)
    #    GISProject.objects.append(m)

    # 1 bridges
    for i in result[1]:
        geom = i
        name = "bridge"
        m = MeshPB().by_coords(geom, name, BaseInfra, False)
        GISProject.objects.append(m)

    # 2 roads
    for i in result[2]:
        geom = i
        name = "roads"
        m = MeshPB().by_coords(geom, name, BaseRoads, False)
        GISProject.objects.append(m)

    # 3 railways
    for i in result[3]:
        geom = i
        name = "railways"
        m = MeshPB().by_coords(geom, name, BaseInfra, False)
        GISProject.objects.append(m)

    # 4 landuses
    for i in result[4]:
        geom = i
        name = "landuses"
        m = MeshPB().by_coords(geom, name, BaseInfra, False)
        GISProject.objects.append(m)

    # 5 plantcovers
    for i in result[5]:
        geom = i
        name = "plantcovers"
        m = MeshPB().by_coords(geom, name, BaseGreen, False)
        GISProject.objects.append(m)

    # 6 waterways
    for i in result[6]:
        geom = i
        name = "waterways"
        m = MeshPB().by_coords(geom, name, BaseWater, True)
        GISProject.objects.append(m)

    # 7 waterbodies
    for i in result[7]:
        geom = i
        name = "waterbodies"
        m = MeshPB().by_coords(geom, name, BaseWater, False)
        GISProject.objects.append(m)

    # 8 generics
    for i in result[8]:
        geom = i
        name = "generics"
        m = MeshPB().by_coords(geom, name, BaseOther, False)
        GISProject.objects.append(m)

    # 9 reliefs
    for i in result[9]:
        geom = i
        name = "generics"
        m = MeshPB().by_coords(geom, name, BaseOther, False)
        GISProject.objects.append(m)

def Create3DKadasterBasisvoorziening(GISBbox,FolderCityJSON):
    #3D Kadaster Basisvoorziening
    filePaths = []
    for file in os.listdir(FolderCityJSON):
        if file.endswith(".json"):
            filepath = os.path.join(FolderCityJSON, file)
            filePaths.append(filepath)
    return(cityJSONParser(filePaths,GISBbox, 2.2))

def Create3DBag(Folder, RdX,RdY,LOD,Bboxwidth):
    #3D BAG files
    filePaths = []
    for file in os.listdir(Folder):
        if file.endswith(".json"):
            filepath = os.path.join(Folder, file)
            filePaths.append(filepath)
            print(filepath)
    #3D BAG parse
    for i in filePaths:
        cityjson_res = cityJSONParserBAG3D(i,RdX,RdY,LOD,Bboxwidth,Bboxwidth)
        buildings = cityjson_res[0]
        names = cityjson_res[1]
        for i,j in zip(buildings, names):
            name = j
            m = MeshPB().by_coords(i, name, BaseBuilding, False)
            GISProject.objects.append(m)

settings = GetWebServerDataSettings('https://raw.githubusercontent.com/jochem25/settings/main/GIS2BIM_project1.json')
ProjectDrive = settings["Projectdrive"]
ProjectFolder = ProjectDrive + settings["Mainfolder"]
City = settings["City"]
Street = settings["Adress"]
HouseNumber = settings["Housenumber"]
MaximumLoD = 2.2
Bboxwidth = int(settings["Bbox"])
ProjectName = City + "_" + Street  + "_" + str(HouseNumber)
#createfolders
folders = []
MainProjectFolder =  ProjectFolder + ProjectName
FolderOBJ = MainProjectFolder  + "/OBJ"
FolderImages = MainProjectFolder  + "/Images"
FolderBGT = MainProjectFolder  + "/BGT"
FolderCityJSON = MainProjectFolder  + "/CityJSON"
FolderAHN = MainProjectFolder  + "/AHN"
folderBAG3D = MainProjectFolder + "/BAG3D"
folders.extend((FolderOBJ,FolderImages,FolderBGT,FolderCityJSON,FolderAHN,folderBAG3D))
for folder in folders:
    CreateFolder(folder)
lst = NL_GetLocationData(NLPDOKServerURL, City, Street, str(HouseNumber))
#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
Bbox = GIS2BIM.CreateBoundingBox(RdX,RdY,Bboxwidth,Bboxwidth,0)
GISBbox = GisRectBoundingBox().Create(RdX, RdY, 200, 200, 0)
print(GISBbox)
GISProject = BuildingPy(settings["BuildingpyName"])

start = time.time()
print(folderBAG3D)
#BAG3DDownload(GISBbox.boundingBoxString, folderBAG3D)
Create3DBag(folderBAG3D, RdX,RdY,2.2,Bboxwidth)

print(FolderCityJSON)
#DownloadCityJSON(GISBbox, FolderCityJSON)
Kadaster3DBasisvoorziening(Create3DKadasterBasisvoorziening(GISBbox, FolderCityJSON),GISProject)

GISProject.toSpeckle("6b2055857b", "3D Kadaster Basisvoorziening en 3D BAG")

end = time.time()
print('Execution time:', end - start, 'seconds')
