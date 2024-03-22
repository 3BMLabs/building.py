import os
import sys
sys.path.append("../building.py")
#print(sys.path)
from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
from packages.GIS2BIM.GIS2BIM_CityJSON import *
import time
from library.material import *
from geometry.mesh import *
import json
from zipfile import ZipFile
import requests

def GetWebServerDataSettings(SettingsfileLocation):
    #get settings
    url = urllib.request.urlopen(SettingsfileLocation)
    jsonData = json.loads(url.read())['Settings']
    #print(jsonData)
    return jsonData

def CreateFolder(Folder):
    #check and ccreate folders
    if not os.path.isdir(Folder):
        #print(Folder + ": " + str(os.path.isdir(Folder)))
        os.mkdir(Folder)

def BGTDownloadnew(targetDirectory, shouldDownload, polygonString):
    TIMEOUT = 30 # seconds
    baseURL = "https://api.pdok.nl"
    downloadRequestURL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
    if shouldDownload:
        # STEP 1: Request Download
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        data = {
            "featuretypes": ["bak", "begroeidterreindeel", "bord", "buurt", "functioneelgebied", "gebouwinstallatie", "installatie", "kast", "kunstwerkdeel", "mast", "onbegroeidterreindeel", "ondersteunendwaterdeel", "ondersteunendwegdeel", "ongeclassificeerdobject", "openbareruimte", "openbareruimtelabel", "overbruggingsdeel", "overigbouwwerk", "overigescheiding", "paal", "pand", "put", "scheiding", "sensor", "spoor", "stadsdeel", "straatmeubilair", "tunneldeel", "vegetatieobject", "waterdeel", "waterinrichtingselement", "waterschap", "weginrichtingselement", "wijk", "wegdeel"],
            "format": "citygml",
            "geofilter": "POLYGON({polygon})".format(polygon = polygonString)
        }
        
        response = requests.post(downloadRequestURL, headers=headers, json=data)
        
        # STEP 2: Check Status until Ready
        jsondata = json.loads(response.text)
        statusURL = baseURL + jsondata["_links"]["status"]["href"]
        
        timer = 0
        while timer < TIMEOUT:
            statusResponse = requests.get(statusURL).text
            statusData = json.loads(statusResponse)
            status = statusData['status']
            
            if status == "COMPLETED":
                downloadURL = baseURL + statusData["_links"]["download"]["href"]
                break
        
            print('STILL WAITING', status, statusData['progress'])
            time.sleep(1)
            timer += 1
        
        # STEP 3: Remove potentially old files
        if os.path.exists(targetDirectory): 
            for file in os.listdir(targetDirectory):
                os.remove(targetDirectory + file)
        else:
            os.mkdir(targetDirectory)
        
        # STEP 3: Download ZIP Package
        download = requests.get(downloadURL)  
        downloadedArchive = targetDirectory + 'download.zip'
        with open(downloadedArchive, 'wb') as f:
            f.write(download.content)
        
        # STEP 4: Extract Package
        zf = ZipFile(downloadedArchive)
        zf.extractall(path = targetDirectory)
        zf.close()        
        
        # STEP 5: Remove Archive
        if os.path.exists(downloadedArchive):
            os.remove(downloadedArchive)
        else:
            print("ERROR: DOWNLOAD FILE DOES NOT EXIST - CAN'T BE DELETED")

    else:
        print('SKIPPING DOWNLOAD')

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
FolderBGT = MainProjectFolder  + "/BGT/"
FolderCityJSON = MainProjectFolder  + "/CityJSON/"
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
GISProject = BuildingPy(settings["BuildingpyName"])
polygonString = GIS2BIM.CreateBoundingBoxPolygon(RdX, RdY, 200, 200,2)

BGTDownloadnew(FolderBGT, True, polygonString)

