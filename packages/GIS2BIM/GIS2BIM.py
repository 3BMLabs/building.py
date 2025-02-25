# [included in GIS2BIM singlefile]
# [!not included in GIS2BIM singlefile - start]

# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2021 Maarten Vroegindeweij <maarten@3bm.co.nl>          *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

#Regarding class GeoLocation:
#    This class is based from the code smaple in this paper:
#        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
#    The owner of that website, Jan Philip Matuschek, is the full owner of
#    his intellectual property. This class is simply a Python port of his very
#    useful Java code. All code written by Jan Philip Matuschek and ported by me
#    (which is all of this class) is owned by Jan Philip Matuschek.
#    '''

"""This module provides tools to load GIS information
"""

__title__= "GIS2BIM"
__author__ = "Maarten Vroegindeweij"
__url__ = "https://github.com/DutchSailor/GIS2BIM"

import urllib
import urllib.request
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import json
import math
import re
from zipfile import ZipFile
#from PIL import Image
	
#Common functions

# [!not included in GIS2BIM singlefile - end]

def CreateDirectory(Directory):
    import os
    try:
        os.mkdir(Directory)
    except:
        pass
    return Directory

def GetWebServerData(servertitle, category, parameter):
	#Get webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests'][category]
	test = []
	for i in data:
		test.append(i["title"])
	result = data[test.index(servertitle)][parameter]
	return result

def xmldata(myurl, xPathStrings):
    urlFile = urllib.request.urlopen(myurl)
    tree = ET.parse(urlFile)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    return xPathResults

def GetWebServerDataService(category,service):
	#Get a list with webserverdata from github repository of GIS2BIM(up to date list of GIS-servers & requests)
	Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/GIS2BIM_Data.json"
	url = urllib.request.urlopen(Serverlocation)
	data = json.loads(url.read())['GIS2BIMserversRequests'][category]
	listOfData = []
	for i in data:
		if i["service"] == service:
			listOfData.append(i)
	return listOfData
	
def DownloadURL(folder,url,filename):
    #Download a file to a folder from a given url
    path = folder + filename
    urllib.request.urlretrieve(url,path)
    return path

def GetDataFiles(folder):
    Serverlocation = "https://raw.githubusercontent.com/DutchSailor/GIS2BIM/master/datafiles/map.html"
    url = urllib.request.urlopen(Serverlocation)
    data = json.loads(url.read())['GIS2BIMserversRequests'][category]
    test = []
    for i in data:
        test.append(i["title"])
    result = data[test.index(servertitle)][parameter]
    return result

def downloadUnzip(downloadURL,filepathZIP,folderUNZIP):
    zipresp = urlopen(downloadURL)
    tempzip = open(filepathZIP, "wb")
    tempzip.write(zipresp.read())
    tempzip.close()
    zf = ZipFile(filepathZIP)
    zf.extractall(path = folderUNZIP)
    zf.close()
    return folderUNZIP
	
#GIS2BIM functions

def mortonCode(X,Y,Xmod,Ymod,TileDim):
    #
    x = bin(int(math.floor(((X - Xmod)/TileDim))))
    y = bin(int(math.floor(((Y - Ymod)/TileDim))))
    x = str(x[2:])
    y = str(y[2:])

    res = "".join(i + j for i, j in zip(y, x))
    z=(res)

    z = int(z, 2)
    return z

def checkIfCoordIsInsideBoundingBox(coord, bounding_box):
    #check if coordinate is inside rectangle boundingbox
    min_x = bounding_box[0] - (bounding_box[2] / 2)
    min_y = bounding_box[1] - (bounding_box[2] / 2)
    max_x = bounding_box[0] + (bounding_box[2] / 2)
    max_y = bounding_box[1] + (bounding_box[2] / 2)

    if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
        return True
    else:
        return False

def TransformCRS_epsg(SourceCRS, TargetCRS, X, Y):
    # transform coordinates between different Coordinate Reference Systems using EPSG-server
    X = str(X)
    Y = str(Y)
    requestURL = "https://epsg.io/trans?" + "&s_srs=" + SourceCRS + "&t_srs=" + TargetCRS + "&x=" + X + "&y=" + Y + "&format=json"
    req = urllib.request.Request(requestURL, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    data = json.loads(webpage)
    X = data["x"]
    Y = data["y"]
    return X,Y

def GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers):
#group X and Y Coordinates of polylines
    posLists = tree.findall(xPathString)
    xyPosList = []
    for posList in posLists:
        dataPosList = posList.text
        coordSplit = dataPosList.split()
        try:
            if float(coordSplit[2]) == 0:
                XYZCountDimensions = 3
            else:XYZCountDimensions = 2
        except:
            XYZCountDimensions = 2
        x = 0
        coordSplitXY = []
        for j in range(0, int(len(coordSplit) / XYZCountDimensions)):
            xy_coord = (round((float(coordSplit[x])+dx)*scale,DecimalNumbers), round((float(coordSplit[x+1])+dy)*scale,DecimalNumbers))
            coordSplitXY.append(xy_coord)
            x +=XYZCountDimensions
        xyPosList.append(coordSplitXY)
    return xyPosList

def CreateBoundingBox(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxString = str(XLeft) + "," + str(YBottom) + "," + str(XRight) + "," + str(YTop)
    return boundingBoxString

class GisRectBoundingBox:
    def __init__(self):
        
        self.origX = 0
        self.origY = 0
        self.XLeft = 0
        self.XRight = 0
        self.YBottom = 0
        self.YTop = 0
        self.width = 0
        self.height = 0
        self.boundingBoxString = ""
        self.boundingBoxString2 = ""
        self.boundingBoxStringPolygon = ""
        self.boundingBoxXY = []
        self.z = 0

    def Create(self,CoordinateX,CoordinateY,Width,Height,DecimalNumbers):
        #Create boundingbox object based on a center point
        self.origX = CoordinateX
        self.origY = CoordinateY
        self.XLeft = round(CoordinateX - 0.5 * Width, DecimalNumbers)
        self.XRight = round(CoordinateX + 0.5 * Width, DecimalNumbers)
        self.YBottom = round(CoordinateY - 0.5 * Height, DecimalNumbers)
        self.YTop = round(CoordinateY + 0.5 * Height, DecimalNumbers)
        self.width = Width
        self.height = Height
        self.boundingBoxString = str(self.XLeft) + "," + str(self.YBottom) + "," + str(self.XRight) + "," + str(self.YTop)
        self.boundingBoxString2 = str(self.XLeft) + "%2C" + str(self.YBottom) + "%2C" + str(self.XRight) + "%2C" + str(self.YTop)
        self.boundingBoxStringPolygon = "(" + str(self.XLeft) + ' ' + str(self.YTop) + ',' + str(self.XRight) + ' ' + str(self.YTop) + ',' + str(
            self.XRight) + ' ' + str(self.YBottom) + ',' + str(self.XLeft) + ' ' + str(self.YBottom) + ',' + str(self.XLeft) + ' ' + str(
            self.YTop) + ')'
        self.boundingBoxXY = [self.XLeft,self.YBottom,self.XRight,self.YTop]
        return self

def CreateBoundingBoxPolygon(CoordinateX,CoordinateY,BoxWidth,BoxHeight,DecimalNumbers):
#Create Boundingboxstring for use in webrequests.
    XLeft = round(CoordinateX-0.5*BoxWidth,DecimalNumbers)
    XRight = round(CoordinateX+0.5*BoxWidth,DecimalNumbers)
    YBottom = round(CoordinateY-0.5*BoxHeight,DecimalNumbers)
    YTop = round(CoordinateY+0.5*BoxHeight,DecimalNumbers)
    boundingBoxStringPolygon = "(" + str(XLeft) + ' ' + str(YTop) + ',' + str(XRight) + ' ' + str(YTop) + ',' + str(XRight) + ' ' + str(YBottom) + ',' + str(XLeft) + ' ' + str(YBottom) + ',' + str(XLeft) + ' ' + str(YTop) + ')'
    return boundingBoxStringPolygon
		
def PointsFromWFS(serverName,boundingBoxString,xPathString,dx,dy,scale,DecimalNumbers):
# group X and Y Coordinates
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers)
    return xyPosList
	
def PointsFromGML(filePath,xPathString,dx,dy,scale,DecimalNumbers):
    # group X and Y Coordinates
    tree = ET.parse(filePath)
    xyPosList = GML_poslistData(tree,xPathString,dx,dy,scale,DecimalNumbers)
    return xyPosList

def DataFromWFS(serverName,boundingBoxString,xPathStringCoord,xPathStrings,dx,dy,scale,DecimalNumbers):
    # group textdata from WFS
    myrequesturl = serverName + boundingBoxString
    urlFile = urllib.request.urlopen(myrequesturl)
    tree = ET.parse(urlFile)
    xyPosList = GML_poslistData(tree,xPathStringCoord,dx,dy,scale,DecimalNumbers)
    xPathResults = []
    for xPathString in xPathStrings:
        a = tree.findall(xPathString)
        xPathResulttemp2 = []
        for xPathResult in a:
            xPathResulttemp2.append(xPathResult.text)
        xPathResults.append(xPathResulttemp2)
    xPathResults.insert(0,xyPosList)
    return xPathResults

def checkIfCoordIsInsideBoundingBox(coord, min_x, min_y, max_x, max_y):
    if min_x <= float(coord[0]) <= max_x and min_y <= float(coord[1]) <= max_y:
        return True
    else:
        return False

def filterGMLbbox(tree,xPathString,bbx,bby,BoxWidth,BoxHeight,scale):

    # Bounding box definition
    bounding_box = [bbx, bby, BoxWidth,BoxHeight]
    min_x = bounding_box[0] - (bounding_box[2]/2)
    min_y = bounding_box[1] - (bounding_box[3]/2)
    max_x = bounding_box[0] + (bounding_box[2]/2)
    max_y = bounding_box[1] + (bounding_box[3]/2)

    # get data from xml
    root = tree.getroot()

    # for loop to get each element in an array
    XMLelements = []
    for elem in root.iter():
        XMLelements.append(elem)

    xpathfound = root.findall(xPathString)

    # for loop to get all polygons in an array
    polygons = []
    for x in xpathfound:
        if x.text:
            try:
                polygons.append(x.text.split(" "))
            except:
                polygons.append("_none_")
        else:
            polygons.append("_none_")

    # for loop to get x,y coords and filter polygons inside Bounding Box
    xyPolygons = []
    for newPolygon in polygons:
        polygon_is_inside_bounding_box = False
        x = 0
        xyPolygon = []
        for i in range(0, int(len(newPolygon) / 2)):
            xy_coord = [newPolygon[x], newPolygon[x + 1]]
            xy_coord_trans = [round((float(newPolygon[x])-bbx)*scale), round((float(newPolygon[x + 1])-bby)*scale)]
            xyPolygon.append(xy_coord_trans)
            x += 2
            if checkIfCoordIsInsideBoundingBox(xy_coord, min_x, min_y, max_x, max_y):
                polygon_is_inside_bounding_box = True
        if polygon_is_inside_bounding_box:
            xyPolygons.append(xyPolygon)
    return xyPolygons
	
def WMSRequest(serverName,boundingBoxString,fileLocation,pixWidth,pixHeight):
    # perform a WMS OGC webrequest( Web Map Service). This is loading images.
    myrequestURL = serverName + boundingBoxString
    myrequestURL = myrequestURL.replace("width=3000", "width=" + str(pixWidth))
    myrequestURL = myrequestURL.replace("height=3000", "height=" + str(pixHeight))
    resource = urllib.request.urlopen(myrequestURL)
    output1 = open(fileLocation, "wb")
    output1.write(resource.read())
    output1.close()
    return fileLocation, resource, myrequestURL

def MortonCode(X,Y,Xmod,Ymod,TileDimension):
    # convert a x and y coordinate to a mortoncode
    x = bin(int(math.floor(((X - Xmod)/TileDimension))))
    y = bin(int(math.floor(((Y - Ymod)/TileDimension))))
    x = str(x[2:])
    y = str(y[2:])
    res = "".join(i + j for i, j in zip(y, x))
    z=(res)
    z = int(z, 2)
    return z

def NominatimAPI(inputlist):
    #get lat/lon via an adress using Nominatim API
    URLpart1 = "https://nominatim.openstreetmap.org/search/"
    URLpart2 = "%20".join(inputlist)
    URLpart3 = "?format=xml&addressdetails=1&limit=1&polygon_svg=1"
    URL = URLpart1 + URLpart2 + URLpart3
    req = urllib.request.Request(URL)
    resp = urllib.request.urlopen(req)
    content = resp.read().decode('utf8')
    try:
        lst = re.split('lat=| lon=| display_name=',content)
        lat = lst[1][1:-1]
        lon = lst[2][1:-1]
    except:
        lat = None
        lon = None
    return lat, lon

def LatLonZoomToTileXY(lat,lon,zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    TileX = int((lon + 180.0) / 360.0 * n)
    TileY = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

    return TileX, TileY

def TMSBboxFromTileXY(TileX,TileY,zoom):
    n = 2.0 ** zoom
    W_deg = TileX / n * 360.0 - 180.0
    N_rad = math.atan(math.sinh(math.pi * (1 - 2 * TileY / n)))
    N_deg = math.degrees(N_rad)
    E_deg = (TileX+1) / n * 360.0 - 180.0
    S_rad = math.atan(math.sinh(math.pi * (1 - 2 * (TileY+1) / n)))
    S_deg = math.degrees(S_rad)

    return S_deg,W_deg,N_deg,E_deg

def TMS_WMTSCombinedMapFromLatLonBbox(lat,lon,bboxWidth,bboxHeight,zoomL,pixels,TMS_WMTS,ServerName):
    #With lat/lon and bbox tilenumbers are calculated then downloaded from given server and merged into 1 images and cropped afterwards to given boundingbox

    #Create Boundingbox lat/lon
    loc = GeoLocation.from_degrees(lat,lon)
    radiusWidth = bboxWidth/2000
    SW_locWidth = loc.bounding_locations(radiusWidth)[0]
    NE_locWidth = loc.bounding_locations(radiusWidth)[1]
    radiusHeight = bboxHeight/2000
    SW_locHeight = loc.bounding_locations(radiusHeight)[0]
    NE_locHeight = loc.bounding_locations(radiusHeight)[1]

    #GetUniqueTileX/TileY list
    TileXYBottomLeft = LatLonZoomToTileXY(SW_locHeight[0],SW_locWidth[1],zoomL)
    TileXYTopRight = LatLonZoomToTileXY(NE_locHeight[0],NE_locWidth[1],zoomL)

    #Get TileX/TileY orderlist for URLlists
    rangex = list(range(TileXYBottomLeft[0], TileXYTopRight[0]+1))
    rangey1 = list(range(TileXYTopRight[1], TileXYBottomLeft[1]+1))
    rangey = rangey1[::-1]
    minx = min(rangex)
    miny = min(rangey)
    maxx = max(rangex)
    maxy = max(rangey)

    #Get Bbox from TopRight/BottomLeft
    BboxTileBottomLeft = TMSBboxFromTileXY(minx,maxy,zoomL)
    BboxTileTopRight = TMSBboxFromTileXY(maxx,miny,zoomL)

    # Calculate total width of tiles and deltax/y of boundingbox
    GeoLocationBottomLeft = GeoLocation.from_degrees(BboxTileBottomLeft[0],BboxTileBottomLeft[1])
    GeoLocationTopLeft = GeoLocation.from_degrees(BboxTileTopRight[2],BboxTileBottomLeft[1])
    GeoLocationTopRight = GeoLocation.from_degrees(BboxTileTopRight[2],BboxTileTopRight[3])

    TotalWidthOfTiles = 1000*GeoLocation.distance_to(GeoLocationTopLeft,GeoLocationTopRight,GeoLocation.EARTH_RADIUS)
    TotalHeightOfTiles = 1000*GeoLocation.distance_to(GeoLocationBottomLeft,GeoLocationTopLeft,GeoLocation.EARTH_RADIUS)

    #deltax Left, Width difference between bbox and TotalWidthOfTiles
    GeoLocationBottomLeftBbox = GeoLocation.from_degrees(SW_locHeight[0],SW_locWidth[1])
    GeoLocationBottomBboxLeftTiles = GeoLocation.from_degrees(SW_locHeight[0],BboxTileBottomLeft[1])
    dx = 1000*GeoLocation.distance_to(GeoLocationBottomBboxLeftTiles,GeoLocationBottomLeftBbox,GeoLocation.EARTH_RADIUS)

    #deltay Bottom, Height difference between bbox and TotalHeightOfTiles
    GeoLocationBottomTilesLeftBbox = GeoLocation.from_degrees(BboxTileBottomLeft[0],SW_locWidth[1])
    dy = 1000*GeoLocation.distance_to(GeoLocationBottomTilesLeftBbox,GeoLocationBottomLeftBbox,GeoLocation.EARTH_RADIUS)

    x = rangex
    y = rangey
    n = len(rangey)
    xl1=[]
    for i in x:
        xl1.append([i]*n)

    xl2=[]
    for sublist in xl1:
        for item in sublist:
            xl2.append(item)
    yl1=[]
    for i in x:
        yl1.append(y)
    yl2=[]
    for sublist in yl1:
        for item in sublist:
            yl2.append(item)

    tilesX = xl2
    tileY = yl2

    #Create URLs for image
    ServerName = ServerName.replace("{z}",str(zoomL))
    URLlist = []

    for i,j in zip(tilesX,tileY):
        URLlist.append(ServerName.replace("{y}",str(j)).replace("{x}",str(i)))

    #Download TileImages
    TileImages = []
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    for i in URLlist:
        TileImages.append(Image.open(urllib.request.urlopen(i)))

    #Create new image to concatenate the tileimages in.
    widthImg = len(rangex)*pixels
    heightImg = len(rangey)*pixels

    img = Image.new('RGB', (widthImg,heightImg))

    LPx=[]
    n=0
    for i in rangex:
        LPx.append(n*pixels)
        n=n+1

    LPy=[]
    n=0
    for i in rangey:
        LPy.append(n*pixels)
        n=n+1

    LPx2=[]
    n=len(LPy)
    for i in LPx:
        LPx2.append([i]*n)

    LPx3=[]
    for sublist in LPx2:
        for item in sublist:
            LPx3.append(item)

    LPy2=[]
    #n=len(LPy)
    for i in LPx:
        LPy2.append(LPy)

    LPy3=[]
    for sublist in LPy2:
        for item in sublist:
            LPy3.append(item)

    LPy4=LPy3[::-1]

    if TMS_WMTS:
        for i,j,k in zip(TileImages,LPy3,LPx3):
            img.paste(i,(j,k))
    else:
        for i,j,k in zip(TileImages,LPx3,LPy4):
            img.paste(i,(j,k))

    #Crop Image
    deltaHeight = TotalHeightOfTiles- bboxHeight
    dxM = dx
    dyM = deltaHeight-dy
    ImageWidthNew=(bboxWidth/TotalWidthOfTiles)*widthImg
    ImageHeightNew=(bboxHeight/TotalHeightOfTiles)*heightImg
    dxImage=-int((dxM/TotalWidthOfTiles)*widthImg)
    dyImage=-int((dyM/TotalHeightOfTiles)*heightImg)

    imgNew = Image.new('RGB', (int(ImageWidthNew),int(ImageHeightNew)))
    imgNew.paste(img,(dxImage,dyImage))

    return imgNew,widthImg,heightImg

class GeoLocation:
    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)
    EARTH_RADIUS = 6378.1  # kilometers

    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)

    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(rad_lat)
        deg_lon = math.degrees(rad_lon)
        return deg_lat, deg_lon

    def __init__(
            self,
            rad_lat,
            rad_lon,
            deg_lat,
            deg_lon
    ):
        self.rad_lat = float(rad_lat)
		
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self._check_bounds()

    def __str__(self):
        degree_sign = u'\N{DEGREE SIGN}'
        return ("{0:.20f}, {1:.20f}").format(
            self.deg_lat, self.deg_lon, self.rad_lat, self.rad_lon)

    def _check_bounds(self):

        if (self.rad_lat < GeoLocation.MIN_LAT
            or self.rad_lat > GeoLocation.MAX_LAT
            or self.rad_lon < GeoLocation.MIN_LON
            or self.rad_lon > GeoLocation.MAX_LON):
            raise Exception("Illegal arguments")

    def distance_to(self, other, radius=EARTH_RADIUS):

        '''

        Computes the great circle distance between this GeoLocation instance
        and the other.
        '''

        return radius * math.acos(
            math.sin(self.rad_lat) * math.sin(other.rad_lat) +
            math.cos(self.rad_lat) *
            math.cos(other.rad_lat) *
            math.cos(self.rad_lon - other.rad_lon)
        )

    def bounding_locations(self, distance, radius=EARTH_RADIUS):

        '''
        Computes the bounding coordinates of all points on the surface
        of a sphere that has a great circle distance to the point represented
        by this GeoLocation instance that is less or equal to the distance argument.

        Param:
            distance - the distance from the point represented by this GeoLocation
                       instance. Must be measured in the same unit as the radius
                       argument (which is kilometers by default)
            radius   - the radius of the sphere. defaults to Earth's radius.
        Returns a list of two GeoLoations - the SW corner and the NE corner - that
        represents the bounding box.
        '''

        if radius < 0 or distance < 0:
            raise Exception("Illegal arguments")

        # angular distance in radians on a great circle

        rad_dist = distance / radius
        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist

        if min_lat > GeoLocation.MIN_LAT and max_lat < GeoLocation.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))
            min_lon = self.rad_lon - delta_lon
            if min_lon < GeoLocation.MIN_LON:
                min_lon += 2 * math.pi
            max_lon = self.rad_lon + delta_lon

            if max_lon > GeoLocation.MAX_LON:
                max_lon -= 2 * math.pi

        # a pole is within the distance
        else:

            min_lat = max(min_lat, GeoLocation.MIN_LAT)
            max_lat = min(max_lat, GeoLocation.MAX_LAT)
            min_lon = GeoLocation.MIN_LON
            max_lon = GeoLocation.MAX_LON

        return [GeoLocation.from_radians(min_lat, min_lon),
                GeoLocation.from_radians(max_lat, max_lon)]

def download_image(url, index, results):
    import requests
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    results[index] = img


def download_images(urls):
    results = [None] * len(urls)
    threads = []

    for index, url in enumerate(urls):
        thread = threading.Thread(target=download_image, args=(url, index, results))
        thread.start()
        threads.append(thread)

    # Wacht tot alle threads zijn voltooid
    for thread in threads:
        thread.join()

    return results


def TMS(zoom_level, rdx, rdy, width, layer, downloadimage: bool):
    zoomlevels = [zoom_level]
    boundingbox_widths = [width]
    layers = [layer]

    zoomleveldata = {0: 3440.640,
                     1: 1720.320,
                     2: 860.160,
                     3: 430.080,
                     4: 215.040,
                     5: 107.520,
                     6: 53.720,
                     7: 26.880,
                     8: 13.440,
                     9: 6.720,
                     10: 3.360,
                     11: 1.680,
                     12: 0.840,
                     13: 0.420,
                     14: 0.210,
                     15: 0.105,
                     16: 0.0575}

    pixel_width = 256
    xcorner = -285401.92
    ycorner = 903402.0

    Resolutions = []
    for x in zoomlevels:
        Resolutions.append(zoomleveldata[x])

    TileColumns = []
    TileRows = []
    DeltaX = []
    DeltaY = []

    for x in Resolutions:
        a = pixel_width * x
        # TileColumns.append(Rdx-Xcorner)
        # TileRows.append(a)
        TileY = (ycorner - rdy) / a
        TileX = (rdx - xcorner) / a
        TileYRound = int(TileY)
        TileXRound = int(TileX)
        TilePercentageY = TileX - TileXRound
        TilePercentageX = TileY - TileYRound
        DeltaYM = TilePercentageY * pixel_width * x
        DeltaXM = TilePercentageX * pixel_width * x

        TileRows.append(TileYRound)
        TileColumns.append(TileXRound)
        DeltaY.append(DeltaYM)
        DeltaX.append(DeltaXM)

    UniqueTileColumns = []
    UniqueTileRows = []
    TileColumns2 = []
    TileRows2 = []

    for x, j, k, l in zip(TileColumns, TileRows, boundingbox_widths, Resolutions):
        TileWidth = pixel_width * l
        c = math.ceil(k / TileWidth)
        b = math.ceil(c / 2) * 2
        UniqueTileColumns.append(range(int((x - b / 2)), 1 + int(x + b / 2)))
        UniqueTileRows.append(range((int(j - b / 2)), 1 + int(j + b / 2)))

    for x in UniqueTileColumns:
        # de list:
        a = []

        counter = len(x)

    for j in x:  # elke unieke tile
        a.append(x)

    flatA = []

    for sublist in a:
        for item in sublist:
            flatA.append(item)

    TileColumns2.append(flatA)
    counter = 0

    for x in UniqueTileRows:
        # de list:
        a = []
        counter = len(x)

        for j in x:  # elke unieke tile
            a.append([int(j)] * counter)

        flatA = []

        for sublist in a:
            for item in sublist:
                flatA.append(item)

        TileRows2.append(flatA)
        counter = 0

    TotalTileWidth = []
    TotalTileHeight = []
    TileColumnMin = min(UniqueTileColumns[0])
    TileColumnsMax = max(UniqueTileColumns[0])
    TileRowsMin = min(UniqueTileRows[0])
    TileRowsMax = max(UniqueTileRows[0])
    TileWidthHeight = (903401.92 - 22598.08) * pow(0.5, zoom_level)
    Rdxmin = TileColumnMin * TileWidthHeight - 285401.92
    # LET OP: WMTS TILING KOMT VAN BOVEN DAAROM HIERONDER MAX I.P.V. MIN
    Rdymin = 903401.92 - TileRowsMax * TileWidthHeight - TileWidthHeight

    # 22598.08
    for x, j in zip(Resolutions, UniqueTileColumns):
        a = len(j) * pixel_width * x
        TotalTileWidth.append(a)

    for x, j in zip(Resolutions, UniqueTileRows):
        a = len(j) * pixel_width * x
        TotalTileHeight.append(a)

    Rdxmax = Rdxmin + TotalTileWidth[0]
    Rdymax = Rdymin + TotalTileHeight[0]
    print(Rdxmin - rdx)
    print(Rdymin - rdy)

    # string1 = "http://geodata.nationaalgeoregister.nl/tiles/service/wmts?&request=GetTile&VERSION=1.0.0&LAYER="
    string1 = "https://service.pdok.nl/lv/bgt/wmts/v1_0?request=GetTile&service=WMTS&VERSION=1.0.0&LAYER="
    string3 = "&STYLE=default&TILEMATRIXSET=EPSG:28992&TILEMATRIX=EPSG:28992:"
    string34 = "&TILEROW="
    string5 = "&TILECOL="
    string7 = "&FORMAT=image/png8";

    urlList = []

    for x, j, k, z in zip(TileColumns2, TileRows2, layers, zoomlevels):
        a = []

        for l, m in zip(x, j):
            b = string1 + str(k) + string3 + str(z) + string34 + str(m) + string5 + str(l) + string7
            a.append(b)
        urlList.append(a)

    bitmaps2 = []

    if downloadimage:
        for x in urlList:
            bitmaps = download_images(x)
            # for j in i:
            #  response = requests.get(j)
            #  img = Image.open(BytesIO(response.content))
            #  bitmaps.append(img)
            #  print(img)
            # DIT MOET SNELLER, RETERTRAAG
            bitmaps2.append(bitmaps)
            combined_bitmaps = []
            for a, b, c in zip(bitmaps2, UniqueTileColumns, UniqueTileRows):
                total_width = len(b) * pixel_width
                total_height = len(c) * pixel_width
                img = Image.new('RGB', (total_width, total_height))
                lpx = []
                n = 0
                for l in j:
                    lpx.append(n * pixel_width)
                    n = n + 1

                LPy = []
                n = 0
                for x in c:
                    LPy.append(n * pixel_width)
                    n = n + 1

                LPx2 = []
                n = len(LPy)
                for x in lpx:
                    LPx2.append([x] * n)

                LPx3 = []
                for sublist in LPx2:
                    for item in sublist:
                        LPx3.append(item)

                LPy2 = []
                for x in lpx:
                    LPy2.append(LPy)

                LPy3 = []
                for sublist in LPy2:
                    for item in sublist:
                        LPy3.append(item)

                LPy4 = reversed(LPy3)

                for m, n, o in zip(a, LPy3, LPx3):
                    img.paste(m, (n, o))
                combined_bitmaps.append(img)
                return combined_bitmaps[0], TotalTileWidth[0], TotalTileHeight[0], Rdxmin, Rdymin, Rdxmax, Rdymax
    else:
        return (
        TotalTileWidth[0], TotalTileHeight[0], TileColumnMin, TileColumnsMax, TileRowsMin, TileRowsMax, Rdxmin, Rdymin,
        Rdxmax, Rdymax, TileWidthHeight)


def toPix(point1, Xmin, Ymin, TotalWidth, TotalHeight, ImgWidthPix, ImgHeightPix):
    # Give a pixel on an image
    x = point1.x
    y = point1.y
    xpix = math.floor(((x - Xmin) / TotalWidth) * ImgWidthPix)
    ypix = ImgHeightPix - math.floor(((y - Ymin) / TotalHeight) * ImgHeightPix)  # min vanwege coord stelsel Image.Draw
    return xpix, ypix


def pointToPILLine(imgdrawobj, color: str, width: float, pnts, dx, dy, TotalTileWidthM, TotalTileHeightM, imgwidthpix,
                   imgheightpix):
    ind = 0
    for i in pnts:
        try:
            P1 = toPix(pnts[ind], dx, dy, TotalTileWidthM, TotalTileHeightM, imgwidthpix,
                       imgheightpix)
            P2 = toPix(pnts[ind + 1], dx, dy, TotalTileWidthM, TotalTileHeightM, imgwidthpix,
                       imgheightpix)
            imgdrawobj.line([P1, P2], fill=color, width=width)
        except:
            pass
        ind = ind + 1
        return P1, P2
