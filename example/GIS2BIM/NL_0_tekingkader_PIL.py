from packages.GIS2BIM.GIS2BIM import *
from packages.GIS2BIM.GIS2BIM_NL import *
from PIL import Image, ImageDraw, ImageFont, ImageColor
from geometry.geometry2d import *
import datetime

#CONVERT PDF-titlesheet to png
import glob, sys, pymupdf
from glob import glob
from os import path
def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))


def dateToday():
    from datetime import date
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d-%m-%Y")
    return d1


def gmlcoordTo2DPoints(gmlstr: str):
    coord = []
    for x in gmlstr.split(" "):
        coords = x.split(",")
        coord.append(Point2D(x=float(coords[0]), y=float(coords[1])))
    return coord


def toPix(point1, Xmin, Ymin, TotalWidth, TotalHeight, ImgWidthPix, ImgHeightPix):
    # Give a pixel on an image
    x = point1.x
    y = point1.y
    xpix = math.floor(((x - Xmin) / TotalWidth) * ImgWidthPix)
    ypix = ImgHeightPix - math.floor(((y - Ymin) / TotalHeight) * ImgHeightPix)  # min vanwege coord stelsel Image.Draw
    return xpix, ypix


def pointsToPILLine(imgdrawobj, color: str, width: float, pnts, dx, dy, TotalTileWidthM, TotalTileHeightM, imgwidthpix,
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

def pdfToImage():
    filepathpdf = "C:/Users/mikev/Documents/GitHub/building.py/example/GIS2BIM/A3-leeg.pdf"
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = pymupdf.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

    doc = pymupdf.open(filepathpdf)  # open document
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save(filepathnew)  # store image as a PNG

filepathnew = "C:/Users/mikev/Documents/GitHub/building.py/example/GIS2BIM/A3-leeg.png"
filepathnew2 = "C:/Users/mikev/Documents/GitHub/building.py/example/GIS2BIM/BAG+kadaster.png"

background = Image.open(filepathnew)

# 1 Start image
imgwidthpix = background.width
imgheightpix = background.height

print(imgwidthpix)
print(imgheightpix)

# 2 Tekeningkader invullen
sheetname = "Kadaster+BAG"
projectnr = "1985"
projectnaam = "Projectnaam"
datum = dateToday()
auteur = "M.D. Vroegindeweij"
opdrachtgever = "Ingenieursbureau 4BM"
schaal = "1:500"
lettertype = 'C:/Users/mikev/Documents/GitHub/building.py/example/GIS2BIM//swissc.ttf'

imgdraw = ImageDraw.Draw(background)
imgdraw.text((100,1435), sheetname, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,60))
imgdraw.text((100,1530), projectnaam, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,60))
imgdraw.text((1600,1500), projectnr, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,30))
imgdraw.text((1600,1550), datum, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,30))
imgdraw.text((1920,1500), auteur, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,30))
imgdraw.text((1800,1600), opdrachtgever, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,30))
imgdraw.text((1260,1600), schaal, fill='black', stroke_width=1,font=ImageFont.truetype(lettertype,30))

# Get GIS-data
from packages.GIS2BIM.GIS2BIM_NL import *
from project.fileformat import *
from exchange.GIS2BIM import *
from geometry.mesh import MeshPB
from library.material import *

# SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL, "Dordrecht", "werf van schouten", "501")

# INSTELLINGEN GEBASEERD OP EEN A3-formaat 1:500
scale = "1:500"
BboxWidth = 200  # Meter
BboxHeight = 120  # Meter
PixWidthBbox = 2272 # Pixels
PixHeightBbox = 1362 # Pixels

# MODEL/DRAWING SETTINGS
Centerline2 = ["Center Line 2", [2, 1, 1, 1], 500]  # Rule: line, whitespace, line whitespace etc., scale

# BASE VALUES
RdX = lst[0]
RdY = lst[1]
BoundingBox = GIS2BIM.GisRectBoundingBox().Create(RdX, RdY, BboxWidth, BboxHeight, 0)
Bbox = BoundingBox.boundingBoxString

# Aerialphoto
fileLocationWMS = tempfolder + "luchtfoto_2020_2.png"
a = GIS2BIM.WMSRequest(GIS2BIM.GetWebServerData("NL_PDOK_Luchtfoto_2020_28992", "webserverRequests", "serverrequestprefix"), Bbox, fileLocationWMS,1500, 1500)

# img = imagePyB().by_file(fileLocationWMS,Bboxwidth*1000,Bboxwidth*1000,0,0,0)

# KADASTRALE GRENZEN
curvesCadaster = GIS2BIM.PointsFromWFS(NLPDOKCadastreCadastralParcels, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY,1000, 2) #M
BPCurvesCadaster = WFSCurvesToBPCurves(curvesCadaster)

ind = 0
LinesCadastrePattern = WFSCurvesToBPCurvesLinePattern(curvesCadaster, Centerline2)

for i in LinesCadastrePattern:
    try:
        P1 = toPix(i.start, -BboxWidth*1000*0.5, -BboxHeight*1000*0.5, BboxWidth*1000, BboxHeight*1000, imgwidthpix, imgheightpix)
        P2 = toPix(i.end, -BboxWidth*1000*0.5, -BboxHeight*1000*0.5, BboxWidth*1000, BboxHeight*1000, imgwidthpix, imgheightpix)
        imgdraw.line([P1, P2], fill="grey", width=1)
    except:
        pass
    ind = ind + 1

# GEBOUWEN
curvesBAG = GIS2BIM.PointsFromWFS(NLPDOKBAGBuildingCountour, Bbox, NLPDOKxPathOpenGISposList, -RdX, -RdY, 1000,2)
BPCurvesBAG = WFSCurvesToBPCurves(curvesBAG)

for PCurve in BPCurvesBAG:
    pntlst = PCurve.points
    ind = 0
    for i in pntlst:
        try:
            P1 = toPix(pntlst[ind], -BboxWidth*1000*0.5, -BboxHeight*1000*0.5, BboxWidth*1000, BboxHeight*1000, imgwidthpix, imgheightpix)
            P2 = toPix(pntlst[ind + 1], -BboxWidth*1000*0.5, -BboxHeight*1000*0.5, BboxWidth*1000, BboxHeight*1000, imgwidthpix, imgheightpix)
            imgdraw.line([P1, P2], fill="red", width=4)
        except:
            pass
        ind = ind + 1

# Save file
background.save(filepathnew2, "PNG")
background.show()

