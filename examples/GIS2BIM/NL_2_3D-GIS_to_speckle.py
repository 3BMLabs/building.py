import sys, os, math
from pathlib import Path
import time



from packages.GIS2BIM.GIS2BIM_CityJSON import *
from library.material import *
from geometry.mesh import *
from NL_1_Download_GIS_data import *
from exchange.speckle import CreateStream
import webbrowser
# Parse CityJSON Files and send geometry to Speckle
# Download files using NL_1_Download_GIS_data.py

# SETTINGS
GISProject = BuildingPy(ProjectName)
StreamID = CreateStream(GISProject.speckleserver,ProjectName,"3D GIS") #Create new specklestream
print(StreamID)
#StreamID = "2e64d634c9" # Speckle Stream ID
folderBAG3D = tempfolder + "BAG3D/"
cityJSONFolder = tempfolder + "cityJSON/"
maximumLoD = 2.2

# BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX, RdY, Bboxwidth, Bboxwidth, 0)
start = time.time()

# 3D Kadaster Basisvoorziening
filePaths = []
for file in os.listdir(cityJSONFolder):
    if file.endswith(".json"):
        filepath = os.path.join(cityJSONFolder, file)
        filePaths.append(filepath)

result = cityJSONParser(filePaths, GISBbox, 2.2)

# 3D BAG
filePaths = []
for file in os.listdir(folderBAG3D):
    if file.endswith(".json"):
        filepath = os.path.join(folderBAG3D, file)
        filePaths.append(filepath)

for i in filePaths:
    cityjson_res = cityJSONParserBAG3D(i, RdX, RdY, 2.2, Bboxwidth, Bboxwidth)
    buildings = cityjson_res[0]
    names = cityjson_res[1]
    for i, j in zip(buildings, names):
        name = j
        m = Mesh().by_coords(i, name, BaseBuilding, False)
        GISProject.objects.append(m)

# 3D KADASTER BASISVOORZIENING
def Kadaster3DBasisvoorziening(resultparser, GISProject):
    # 3D KADASTER BASISVOORZIENING

    resultparser = result

    # 0 buildings LOD 1
    # for i in example[0]:
    #    geom = i["geometry"]
    #    name = i["attributes"]["cadastre_id"]
    #    m = MeshPB().by_coords(geom, name, BaseBuilding, True)
    #    GISProject.objects.append(m)

    # 1 bridges
    for i in result[1]:
        geom = i
        name = "bridge"
        m = Mesh().by_coords(geom, name, BaseInfra, False)
        GISProject.objects.append(m)

    # 2 roads
    for i in result[2]:
        geom = i
        name = "roads"
        m = Mesh().by_coords(geom, name, BaseRoads, False)
        GISProject.objects.append(m)

    # 3 railways
    for i in result[3]:
        geom = i
        name = "railways"
        m = Mesh().by_coords(geom, name, BaseInfra, False)
        GISProject.objects.append(m)

    # 4 landuses
    for i in result[4]:
        geom = i
        name = "landuses"
        m = Mesh().by_coords(geom, name, BaseGreen, False)
        GISProject.objects.append(m)

    # 5 plantcovers
    for i in result[5]:
        geom = i
        name = "plantcovers"
        m = Mesh().by_coords(geom, name, BaseGreen, False)
        GISProject.objects.append(m)

    # 6 waterways
    for i in result[6]:
        geom = i
        name = "waterways"
        m = Mesh().by_coords(geom, name, BaseWater, True)
        GISProject.objects.append(m)

    # 7 waterbodies
    for i in result[7]:
        geom = i
        name = "waterbodies"
        m = Mesh().by_coords(geom, name, BaseWater, False)
        GISProject.objects.append(m)

    # 8 generics
    for i in result[8]:
        geom = i
        name = "generics"
        m = Mesh().by_coords(geom, name, BaseOther, False)
        GISProject.objects.append(m)

    # 9 reliefs
    for i in result[9]:
        geom = i
        name = "generics"
        m = Mesh().by_coords(geom, name, BaseOther, False)
        GISProject.objects.append(m)


Kadaster3DBasisvoorziening(result, GISProject)

GISProject.to_speckle(StreamID, ProjectName)

end = time.time()
print('Execution time:', end - start, 'seconds')
url = "https://" + GISProject.speckleserver + "/streams/" + StreamID
webbrowser.open(url, new=2)
