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
import ijson
from library.material import *
from geometry.mesh import *
import ssl

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

gmlFilePaths = FolderBGT
#gmlFileNames = IN[1]
bboxCenterEW = float(RdY)
bboxCenterNS = float(IN[3])
bboxRadius = float(Bboxwidth) / 2
#includeCrossingElements = IN[5]

# CONSTANTS
scaleFactor = 1000 # m to mm

xpathstrCityObject = 'citygml:cityObjectMember/*[not(imgeo:eindRegistratie)]'
xpathstrObjectPolygons = './/{http://www.opengis.net/gml}Polygon'
xpathstrObjectCoordinates = './/{http://www.opengis.net/gml}exterior//{http://www.opengis.net/gml}posList'
xpathstrSurfaceBoundary = './/{http://www.opengis.net/gml}exterior'
xpathstrSurfaceInnerBoundary = './/{http://www.opengis.net/gml}interior'
xpathstrNodeCoordinates = './/{http://www.opengis.net/gml}posList'
xpathstrNodeID = './/{http://www.geostandaarden.nl/imgeo/2.1}lokaalID'
xpathstrBAGID = './/{http://www.geostandaarden.nl/imgeo/2.1}identificatieBAGPND'
xpathstrNodeDate = './/{http://www.geostandaarden.nl/imgeo/2.1}tijdstipRegistratie'
xpathstrCurveSegments = './/{http://www.opengis.net/gml}segments'

nsMap = {
    'citygml': 'http://www.opengis.net/citygml/2.0',
    'imgeo': 'http://www.geostandaarden.nl/imgeo/2.1',
}

RING_TYPE = '{http://www.opengis.net/gml}Ring'
LINEAR_RING_TYPE = '{http://www.opengis.net/gml}LinearRing'
ARC_TYPE = '{http://www.opengis.net/gml}Arc'
LINE_SEGMENT_TYPE = '{http://www.opengis.net/gml}LineStringSegment'


# print ('INPUTS', gmlFilePath, bboxCenterEW, bboxCenterNS, bboxRadius)

# HELPERS
def tryFloat(input, default):
    try:
        return float(input)
    except:
        return default
        
def flatten(list):
    return [item for sublist in list for item in sublist]

def insideBBox(pointCoords):
    return abs(pointCoords[0] - bboxCenterEW) <= bboxRadius and abs(pointCoords[1] - bboxCenterNS) <= bboxRadius

def pointEquals(pointA, pointB):
    return pointA.X == pointB.X and pointA.Y == pointB.Y

def createTransformedPoint(x, y):
    return Point.ByCoordinates(round((x - bboxCenterEW) * scaleFactor), round((y - bboxCenterNS) * scaleFactor, 0))

def removeDuplicates2D(points):
    result = []
    for point in points:
        alreadyExists = False
        for savedPoint in result:
            if pointEquals(savedPoint, point):
                alreadyExists = True
                break
        if not alreadyExists:
            result.append(point) 
    return result
    
def parseBoundary(xBoundary):
    boundary = None
    boundaryType = xBoundary.getchildren()[0].tag
    
    if boundaryType == RING_TYPE:
        # Parse segments and interprete Arcs and LineSegments (and others?)
        curveSegments = xBoundary.find(xpathstrCurveSegments).getchildren()
        curves = []
        for segment in curveSegments:
            segmentType = segment.tag
            if segmentType == LINE_SEGMENT_TYPE:
                nodeCoordinates = segment.find(xpathstrNodeCoordinates)
                if nodeCoordinates.text:
                    points = []
                    content = nodeCoordinates.text.split(' ')
                    index = 1
                    while index < len(content):
                        points.append(createTransformedPoint(float(content[index-1]), float(content[index])))
                        index += 2
                    preparedPoints = removeDuplicates2D(points)
                    curves.append(PolyCurve.ByPoints(preparedPoints, False))
            elif segmentType == ARC_TYPE:
                nodeCoordinates = segment.find(xpathstrNodeCoordinates)
                if nodeCoordinates.text:
                    points = []
                    content = nodeCoordinates.text.split(' ')
                    index = 1
                    while index < len(content):
                        points.append(createTransformedPoint(float(content[index-1]), float(content[index])))
                        index += 2
                if len(points) ==  3:
                    curves.append(Arc.ByThreePoints(points[0], points[1], points[2]))
                else:
                    print('INVALID ARC', len(points), 'points,', len(content), 'coords')
            else:
                print('UNSUPPORTED RING SEGMENT TYPE:', segmentType, '- PLEASE ADD')
        
        boundary = PolyCurve.ByJoinedCurves(curves)

    elif boundaryType == LINEAR_RING_TYPE:
        nodeCoordinates = xBoundary.find(xpathstrNodeCoordinates)
        if nodeCoordinates.text:
            points = []
            content = nodeCoordinates.text.split(' ')
            index = 1
            while index < len(content):
                points.append(createTransformedPoint(float(content[index-1]), float(content[index])))
                index += 2
            preparedPoints = removeDuplicates2D(points)
            
            boundary = PolyCurve.ByPoints(preparedPoints, True)
                
    else:
        print('UNSUPPORTED GEOMETRY TYPE:', boundaryType, '- PLEASE ADD')
        
    return boundary
    
# STEP 1: Open CityGML/XML Files and find all cityObjects with attributes

cityObjectTypes = []
cityObjectBounds = []
cityObjectIDs = []
cityObjectBAGPandIDs = []
cityObjectDates = []

for fileIndex, gmlFilePath in enumerate(gmlFilePaths):

    cityObjectType = gmlFileNames[fileIndex]
    
    xml = ''
    if os.path.exists(gmlFilePath):
        with open(gmlFilePath, 'r') as gmlFile:
            xml = gmlFile.read()
    
    root = ET.fromstring(xml.encode('utf-8'))
    
    xpathCityObjectsFound = root.xpath(xpathstrCityObject, namespaces=nsMap)
    
    # print('Matches Objects', len(xpathCityObjectsFound), xpathCityObjectsFound[0])
    
    
    # STEP 2: Extract the outlines for each area 
    
    for node in xpathCityObjectsFound:
        
        outerBoundaries = []
        innerBoundaries = []
        
        xCoordinates = node.findall(xpathstrObjectCoordinates)
        inBBox = False if includeCrossingElements else True
        coordinates = []
        for coordNode in xCoordinates:
            if coordNode.text:
                content = coordNode.text.split(' ')
                index = 1
                while index < len(content):
                    coords = [float(content[index-1]), float(content[index])]
                    coordinates.append(coords)
                    index += 2
                    if includeCrossingElements:
                        if not inBBox: # once a point inside BBox is found we can stop checking
                            inBBox = insideBBox(coords)
                    else:
                        if inBBox: # once a point outside BBox is found we can stop checking
                            inBBox = insideBBox(coords)
                            

        if not inBBox:
            continue
            
        # TODO: Check if all boundaries could be treated the same? Ie just find all interior or exterior nodes, add their boundaries to the list and let revit figure out whats outside and inside
        
        # Find all surface members and parse individually
        xSurfaceMembers = node.findall(xpathstrObjectPolygons)
        
        for surfaceMember in xSurfaceMembers:
    
            # Parse Outer Boundary
            xBoundary = surfaceMember.find(xpathstrSurfaceBoundary)
            if xBoundary is not None:
                boundary = parseBoundary(xBoundary)
                if boundary is not None:
                    outerBoundaries.append(boundary)
                
            # Parse Inner Boundary
            xInnerBoundaries = surfaceMember.findall(xpathstrSurfaceInnerBoundary)
            for innerBoundary in xInnerBoundaries:
                boundary = parseBoundary(innerBoundary)
                if boundary is not None:
                    innerBoundaries.append(boundary)
        
        # Return boundaries with corresponding attributes        
        boundaries = outerBoundaries + innerBoundaries
        if len(boundaries) > 0 or type(boundaries) != list:
        
            preparedBoundaries = []
            
            # Solve Overlapping Boundaries
            outerCounter = len(outerBoundaries)
            while len(boundaries) > 0:
                checkingBoundary = boundaries.pop(0)
                checkingIsOuter = outerCounter > 0
                if outerCounter > 0:
                    outerCounter -= 1

                indicesToDelete = []
                outerCounterDifference = 0
                for j in range(0, len(boundaries)):
                    otherBoundary = boundaries[j]
                    if Geometry.DoesIntersect(checkingBoundary, otherBoundary):
                        surface1 = Surface.ByPatch(checkingBoundary)
                        surface2 = Surface.ByPatch(otherBoundary)
                       
                        otherIsOuter = j < outerCounter
                        
                        if (checkingIsOuter and otherIsOuter) or (not checkingIsOuter and not otherIsOuter):
                            print('OUT/OUT or IN/IN INTERSECTION - Merging', len(cityObjectBounds))
                            combinedSurface = Surface.ByUnion([surface1, surface2])
                        else:
                            print('OUT/IN INTERSECTION - Substracting', len(cityObjectBounds))
                            combinedSurface = Surface.Difference(surface1, [surface2]) 
                        try:   
                            checkingBoundary = PolyCurve.ByJoinedCurves(combinedSurface.PerimeterCurves())   
                        except:
                            print('ERROR JOINING CURVES: Probably due to point-like intersection - Removing violating boundary...')
                        finally:
                            indicesToDelete.append(j)
                            if otherIsOuter:
                                outerCounterDifference += 1
                
                # remove merged or breaking boundaries to prevent duplicates and adjust outerCounter
                boundaries = [v for i, v in enumerate(boundaries) if i not in indicesToDelete]
                outerCounter -= outerCounterDifference
                
                preparedBoundaries.append(checkingBoundary.Curves())

        
            bgtID = node.find(xpathstrNodeID).text
            date = node.find(xpathstrNodeDate).text
            
            try:
                bagID = node.find(xpathstrBAGID).text
            except:
                bagID = ''
            
            cityObjectTypes.append(cityObjectType)
            cityObjectBounds.append(preparedBoundaries)
            cityObjectIDs.append(bgtID)
            cityObjectBAGPandIDs.append(bagID)
            cityObjectDates.append(date)
        
        else:
            print('NO BOUNDARY ERROR', len(boundaries))
        
       
# STEP 3: Return Boundary Curves
    
#OUT = [cityObjectTypes, cityObjectBounds, cityObjectIDs, cityObjectBAGPandIDs, cityObjectDates]