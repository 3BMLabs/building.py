from exchange.speckle import *
from objects.panel import *
from objects.frame import *
from objects.datum import *
from exchange.struct4U import *
from abstract.vector import *
from abstract.coordinatesystem import *
from objects.analytical import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 2500 #extension grid

#INPUT in mm
spac = 6500 #grid spacing 1
n = 7 # number of grids 1

spac_y = 5200 #grid spacing 2
nw = 4 # number of grids 2

z = 9000 #height of the structure
afschot = 0

GEVELKOLOM = "IPE330"
HOOFDLIGGER = "HEA700"
RANDLIGGER = "HEA160"
KOPPELLIGGER = "HFRHS80x80x5"
HOEKKOLOM = "HEA300"
KOPGEVELKOLOM = "IPE300"
RANDLIGGER_KOPGEVEL = "HEA160"
WVB_DAK = "L70X70X7"
WVB_GEVEL = "S100x5"
FOUNDATIONBEAM = Rectangle("FB 400x600",400,600).curve

#WINDVERBANDEN GEVEL
wvb = [
    ["K1",2,1],
    ["K2",2,1],
    ["L1",4,1],
    ["L1",8,1],
    ["L2",4,1]]


#WINDVERBANDEN DAK
wvbDak = [
    [1,1,1],  #Stramienvak X, Stramienvak Y, 0=R1, 1=R2, 2=R1,R2
    [2,2,1],
    [3,3,1],
    [4,4,1],
    [5,4,0],
    [6,3,0],
    [7,2,0],
    [8,1,0],
    [1, 4, 0],
    [2, 3, 0],
    [3, 2, 0],
    [4, 1, 0],
    [5, 1, 1],
    [6, 2, 1],
    [7, 3, 1],
    [8, 4, 1]
    ]

#MODELERING
x = spac #stramienmaat
y = spac_y*nw #width hall
width = y
l = (n+1) * spac
length = l

spacX = str(n+1) + "x" + str(spac)  #"13x5400"
spacY = str(nw) + "x" + str(spac_y)  #"4x5400"
grids = GridSystem(spacX,seqX,spacY,seqY,ext)
obj1 = grids[0] + grids[1]

#obj1 = []
#SPANTEN
for i in range(n):
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, z), Point(x, y*0.5, z+afschot), HOOFDLIGGER, "Hoofdligger deel 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y*0.5, z+afschot), Point(x, y, z), HOOFDLIGGER,"Hoofdligger deel 2", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), GEVELKOLOM, "Kolom 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), GEVELKOLOM, "Kolom 2", BaseSteel))
    obj1.append(Support.pinned(Point(x, y, 0)))
    obj1.append(Support.pinned(Point(x, 0, 0)))
    x = x + spac

#FOUNDATION BEAM
obj1.append(Frame.byStartpointEndpoint(Point(0,0,0), Point(0,y,0), FOUNDATIONBEAM,"FB 1",0,BaseConcrete))
obj1.append(Frame.byStartpointEndpoint(Point(l,0,0), Point(l,y,0), FOUNDATIONBEAM,"FB 1",0,BaseConcrete))
obj1.append(Frame.byStartpointEndpoint(Point(0,0,0), Point(l,0,0), FOUNDATIONBEAM,"FB 1",0,BaseConcrete))
obj1.append(Frame.byStartpointEndpoint(Point(0,y,0), Point(l,y,0), FOUNDATIONBEAM,"FB 1",0,BaseConcrete))


#RANDLIGGERS & KOPPELKOKERS
x = 0
for i in range(n+1): #elk stramienvak + 1
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, z), Point(x+spac, 0, z), RANDLIGGER, "Randligger 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, z), Point(x+spac, y, z), RANDLIGGER, "Randligger 2", BaseSteel))
    ys = spac_y
    for i in range(nw-1):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, z), Point(x+spac, ys, z), KOPPELLIGGER,"Koppelkoker", BaseSteel))
        ys = ys + spac_y
    x = x + spac

#KOPGEVEL
x = 0
for i in range(2): #VOORZIJDE EN ACHTERZIJDE
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), HOEKKOLOM, "HOEKKOLOM 1", BaseSteel))
    obj1.append(Support.pinned(Point(x, 0, 0)))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), HOEKKOLOM, "HOEKKOLOM 2", BaseSteel))
    obj1.append(Support.pinned(Point(x, y, 0)))
    ys = spac_y
    for i in range(nw-1):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, 0), Point(x, ys, z), KOPGEVELKOLOM,"KOPGEVELKOLOM", BaseSteel))
        obj1.append(Support.pinned(Point(x, ys, 0)))
        ys = ys + spac_y
    ys = 0
    for i in range(nw):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, z), Point(x, ys+spac_y, z), RANDLIGGER_KOPGEVEL, "RANDLIGGER KOPGEVEL", BaseSteel))
        ys = ys + spac_y
    x = l

#WVB in gevel
#Positie 1: K1, K2, L1 of L2: K1 is kopgevel 1, #K2 is kopgevel 2, #L1 is langsgevel 1, L2 is langsgevel 2
#Positie 2: Vaknummer
#Positie 3: Over hoeveel stramien verdelen

for i in wvb: #For loop for vertical bracing
    if i[0] == "K1": #kopgevel 1
        obj1.append(Frame.byStartpointEndpointProfileName(Point(0, (i[1]-1) * spac_y, 0), Point(0, (i[1]) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
        obj1.append(Frame.byStartpointEndpointProfileName(Point(0, (i[1]) * spac_y, 0), Point(0, (i[1]-1) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
    elif i[0] == "K2":
        x = l
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, (i[1]-1) * spac_y, 0), Point(x, (i[1]) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, (i[1]) * spac_y, 0), Point(x, (i[1]-1) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
    elif i[0] == "L1":
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]-1) * spac, 0, 0), Point((i[1]) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]) * spac, 0, 0), Point((i[1]-1) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
    elif i[0] == "L2":
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1] - 1) * spac, y, 0), Point((i[1]) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]) * spac, y, 0), Point((i[1] - 1) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel))
    else:
        pass

    #[1,1,1],  #Stramienvak X, Stramienvak Y, 0=R1, 1=R2, 2=R1,R2

for i in wvbDak:
    x1 = (i[0]-1)*spac
    x2 = i[0]*spac
    y1 = (i[1]-1)*spac_y
    y2 = i[1] * spac_y
    if i[2] == 0:
        x1t = x1
        x1 = x2
        x2 = x1t
    else:
        x1 = x1
    obj1.append(Frame.byStartpointEndpointProfileName(
        Point(x1, y1, z),
        Point(x2, y2, z),
        WVB_DAK,"WVB DAK", BaseSteel))

def LoadPanels(width,length,z):
    #LoadPanels
    LPRoof = LoadPanel()
    LPRoof.Description = "Roof"
    LPRoof.LoadBearingDirection = "X"
    LPRoof.PolyCurve = Rect(Vector3(0,0,z),width,length)
    obj1.append(LPRoof)

    LPWall1 = LoadPanel()
    LPWall1.Description = "Kopgevel 1"
    LPWall1.LoadBearingDirection = "X"
    LPWall1.PolyCurve = RectXY(Vector3(0,0,0),width,z)
    obj1.append(LPWall1)

    LPWall2 = LoadPanel()
    LPWall2.Description = "Kopgevel 2"
    LPWall2.LoadBearingDirection = "X"
    LPWall2.PolyCurve = RectXY(Vector3(0,length,0),width,z)
    obj1.append(LPWall2)

    LPWall3 = LoadPanel()
    LPWall3.Description = "Langsgevel 1"
    LPWall3.LoadBearingDirection = "X"
    LPWall3.PolyCurve = RectYZ(Vector3(0,0,0),length,z)
    obj1.append(LPWall3)

    LPWall4 = LoadPanel()
    LPWall4.Description = "Langsgevel 1"
    LPWall4.LoadBearingDirection = "X"
    LPWall4.PolyCurve = RectYZ(Vector3(width,0,0),length,z)

    obj1.append(LPWall4)

LoadPanels(length,width,z)


SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "95f9fd2609", SpeckleObj, "7 Industrial Hall.py")

#Export to XFEM4U XML String

xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(obj1) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Industrial Hall")
xmlS4U.addPanels(obj1) #add Load Panels
xmlS4U.addGrids(spacX,seqX,spacY,seqY,z) # Grids
xmlS4U.addSurfaceLoad(obj1)
xmlS4U.addLoadCasesCombinations()
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/7 Industrial Hall/Hall.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()