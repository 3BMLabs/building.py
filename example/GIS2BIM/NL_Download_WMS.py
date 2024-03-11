from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from packages.GIS2BIM.GIS2BIM_NL_helpers import *
import math
#Download a lot of WMS

#SETTINGS
GISProject = BuildingPy("test")
tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL,"Dordrecht", "lange geldersekade", "2")
Bboxwidth = 200 #m

#BOUNDINGBOX
RdX = lst[0]
RdY = lst[1]
GISBbox = GisRectBoundingBox().Create(RdX,RdY,Bboxwidth,Bboxwidth,0)

folderWMS = tempfolder + "WMS/"
CreateDirectory(folderWMS)

WMSList = [
["Luchtfoto 2016", 500, 500, NLPDOKLuchtfoto2016],
["Luchtfoto 2017", 500, 500, NLPDOKLuchtfoto2017],
["Luchtfoto 2018", 500, 500, NLPDOKLuchtfoto2018],
["Luchtfoto 2019", 500, 500, NLPDOKLuchtfoto2019],
["Luchtfoto 2020", 500, 500, NLPDOKLuchtfoto2020],
["Luchtfoto 2021", 500, 500, NLPDOKLuchtfoto2020],
["Luchtfoto actueel", 500, 500, NLPDOKLuchtfotoActueel],
["Luchtfoto actueel_5x5km", 5000, 5000, NLPDOKLuchtfotoActueel],
["Luchtfoto actueel_100x100km", 100000, 100000, NLPDOKLuchtfotoActueel],
["Ruimtelijke plannen bouwvlak", 500, 500, NLRuimtelijkeplannenBouwvlak],
["Ruimtelijke plannen enkelbestemming", 500, 500, NLRuimtelijkeplannenEnkelbestemming],
["Natura2000", 500, 500, NLNatura2000],
["Natura2000_20x20km", 20000, 20000, NLNatura2000],
["Geluidskaart alle bronnen", 500, 500, NLGeluidskaartAlleBronnen],
["Geluidskaart alle bronnen_5x5km", 5000, 5000, NLGeluidskaartAlleBronnen],
["Geluidskaart wegverkeer", 500, 500, NLRIVMGeluidskaartldenwegverkeer],
["Geluidskaart wegverkeer_5x5km", 5000, 5000, NLRIVMGeluidskaartldenwegverkeer],
["Geluidskaart spoor", 500, 500, NLRIVMGeluidskaartldenspoor],
["Geluidskaart spoor_5x5km", 5000, 5000, NLRIVMGeluidskaartldenspoor],
["Risicocontour basisnet", 500, 500, NLRisicocontourbasisnet],
["Risicocontour basisnet_5x5km", 5000, 5000, NLRisicocontourbasisnet],
["Risicocontour EV", 500, 500, NLRisicocontourEV],
["Risicocontour EV_5x5km", 5000, 5000, NLRisicocontourEV],
["Risicocontour EV brand", 500, 500, NLRisicocontourEVbrand],
["Risicocontour EV brand_5x5km", 5000, 5000, NLRisicocontourEVbrand],
["Risicocontour EV explosie", 500, 500, NLRisicocontourEVexplosie],
["Risicocontour EV explosie_5x5km", 5000, 5000, NLRisicocontourEVexplosie]
]

for i in WMSList:
    Width = i[1]
    Height = i[2]
    pixHeight = math.floor(2500 * (Height/Width))
    ServerPrefix = i[3]
    Filelocation = folderWMS + i[0] + ".png"
    BBox = GisRectBoundingBox().Create(RdX,RdY,Width,Height,2)
    WMSRequest(ServerPrefix,BBox.boundingBoxString,Filelocation,2500,pixHeight)