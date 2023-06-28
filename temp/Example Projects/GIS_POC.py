from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *

from geometry.geometry2d import *
from geometry.curve import *
from geometry.solid import *
def gmlcoordTo2DPoints(gmlstr: str):
    coord = []
    for i in gmlstr.split(" "):
        coords = i.split(",")
        coord.append(Point2D(x=float(coords[0]),y=float(coords[1])))
    return coord

def gmlToBuildingPyCurve(gml):
    PCurves = []
    for i in gml:
        pnts = []
        for j in i:
            pnts.append(Point2D(j[0], j[1]))
        plycrve2D = PolyCurve2D.byPoints(pnts)
        PC3 = PolyCurve.byPolyCurve2D(plycrve2D)
       # Project.objects.append(PC3)
        PCurves.append(PC3)
    return PCurves

Project = BuildingPy(name="GIS test",number="0")

Plaats = "Dordrecht"
Straat = "zuidendijk"
Nummer = "315"
Width = 500
Height = 500

loc = NL_GetLocationData(NLPDOKServerURL,Plaats,Straat,Nummer)
bbox = CreateBoundingBox(loc[0], loc[1], Width, Height,2)

pntsCadaster = PointsFromWFS(NLPDOKCadastreCadastralParcels,bbox,NLPDOKxPathOpenGISposList,-loc[0],-loc[1],1000,0)
gmlToBuildingPyCurve(pntsCadaster)

pntsBAG = PointsFromWFS(NLPDOKBAGBuildingCountour,bbox,NLPDOKxPathOpenGISposList,-loc[0],-loc[1],1000,0)
PC3 = gmlToBuildingPyCurve(pntsBAG)





for i in PC3:
    verts = []
    faces = []
    numberFaces = 0
    n = 0  # number of verts
    count = 0
    pnts = i.points
    for j in pnts:
         #number in list
        try:
            faces.append(2)
            faces.append(n)
            n = n + 1
            faces.append(n)
            verts.append(j.x)
            verts.append(j.y)
            verts.append(j.z)
            numberFaces = numberFaces + 1
            count = count + 1
            verts.append(pnts[count].x)
            verts.append(pnts[count].y)
            verts.append(pnts[count].z)
        except:
            pass
    ex = Extrusion()
    ex.verts = verts
    ex.faces = faces
    ex.numberFaces = numberFaces
    ex.name = "GIS"
    ex = Extrusion()
    ex.verts = verts
    ex.faces = faces
    ex.numberFaces = numberFaces
    ex.name = "GIS"
    Project.objects.append(ex)
    print(verts)
    print(faces)

#sys.exit()

#self.countVertsFaces = 0  # total number of verts per face (not the same as total verts)
Project.toSpeckle("e77454f5e0","test 2")
