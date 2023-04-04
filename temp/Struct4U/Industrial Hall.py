from exchange.speckle import *
from objects.panel import *
from objects.frame import *
from objects.datum import *
from exchange.struct4U import *
from abstract.vector import *
from abstract.coordinatesystem import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 5000 #extension grid

#INPUT in mm
spac = 7000 #gridspacing 1
n = 6 # number of grids -1

spac_y = 5200 #stramien in dwarsrichting
nw = 5 # n-stramienen dwarsrichting

z = 9000 #height of the structure
afschot = 0

GEVELKOLOM = "IPE330"
HOOFDLIGGER = "HEA700"
RANDLIGGER = "HEA160"
KOPPELLIGGER = "K80/80/5"
HOEKKOLOM = "HEA300"
KOPGEVELKOLOM = "HEA180"
RANDLIGGER_KOPGEVEL = "HEA160"
WVB_DAK = "L70/70/7"
WVB_GEVEL = "S100X5"

#WINDVERBANDEN
wvb = [
    ["K1",2,1],
    ["K2",2,1],
    ["L1",4,1],
    ["L1",8,1],
    ["L2",2,1],
    ["L2",4,1]]


#MODELLERING
x = spac #stramienmaat
y = spac_y*nw #width hall
l = (n+1) * spac

spacX = str(n+1) + "x" + str(spac)  #"13x5400"
spacY = str(nw) + "x" + str(spac_y)  #"4x5400"
grids = GridSystem(spacX,seqX,spacY,seqY,ext)
obj1 = grids[0] + grids[1]

gridsXML = "<Grids>" + "<X>" + spacX + "</X>" + "<X_Lable>" + seqX + "</X_Lable>" + "<Y>" + spacY + "</Y>" + "<Y_Lable>" + seqY + "</Y_Lable>" + "<Z>" + "0 " + str(z) + "</Z>" + "<Z_Lable>" + "+0 h" + "</Z_Lable>" + "</Grids>"

#obj1 = []
#SPANTEN
for i in range(n):
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, z), Point(x, y*0.5, z+afschot), HOOFDLIGGER, "Hoofdligger deel 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y*0.5, z+afschot), Point(x, y, z), HOOFDLIGGER,"Hoofdligger deel 2", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), GEVELKOLOM, "Kolom 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), GEVELKOLOM, "Kolom 2", BaseSteel))
    x = x + spac

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

#WINDVERBANDEN DAK
x = 0

#KOPGEVEL
x = 0
for i in range(2): #VOORZIJDE EN ACHTERZIJDE
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), HOEKKOLOM, "HOEKKOLOM 1", BaseSteel))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), HOEKKOLOM, "HOEKKOLOM 2", BaseSteel))
    ys = spac_y
    for i in range(nw-1):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, 0), Point(x, ys, z), KOPGEVELKOLOM,"KOPGEVELKOLOM", BaseSteel))
        ys = ys + spac_y
    ys = 0
    for i in range(nw):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, z), Point(x, ys+spac_y, z), RANDLIGGER_KOPGEVEL, "RANDLIGGER KOPGEVEL", BaseSteel))
        ys = ys + spac_y
    x = l

wvb = [
    ["K1",2,1],
    ["K2",2,1],
    ["L1",4,1],
    ["L1",8,1],
    ["L2",4,1]]

#WVB in gevel
#Positie 1: K1, K2, L1 of L2: K1 is kopgevel 1, #K2 is kopgevel 2, #L1 is langsgevel 1, L2 is langsgevel 2
#Positie 2: Vaknummer
#Positie 3: Over hoeveel stramien verdelen

for i in wvb: #For loop voor verticale windverbanden rondom
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

#Belastingen


SpeckleObj = translateObjectsToSpeckleObjects(obj1)
#Commit = TransportToSpeckle("struct4u.xyz", "95f9fd2609", SpeckleObj, "Parametric Structure.py")

#ExportXML
Frame1 = "<Frame>"
Project = "<ProjectName>" + "Building.py Industrial Hall" + "</ProjectName>"
ProjectNumber = "<ProjectNumber/>"
ExportDate = "<ExportDateTime>2023-02-17 22:02:38Z</ExportDateTime>"
XMLVersion = "<XMLExportVersion>v4.0.30319</XMLExportVersion>"
Nodes = "<Nodes></Nodes>"
Supports = "<Supports></Supports>"
Grids = "<Grids></Grids>"
Profiles = "<Profiles></Profiles>"
Beamgroup = "<Beamgroup></Beamgroup>"
Beams = "<Beams></Beams>"
Plates = "<Plates></Plates>"
RebarLongitudinal = "<RebarLongitudinal></RebarLongitudinal>"
RebarStirrup = "<RebarStirrup></RebarStirrup>"
Layers = "<Layers><Layer_number>1</Layer_number><Layer_description>Layer 1</Layer_description></Layers>"
Frame2 = "</Frame>"

Grids = gridsXML


#Number of nodes:
n = 0
Nodes = []
Plates = []
Beams = []
Beamgroup = []
Profiles = []
plateN = 0 # Numbering plates
beamsN = 0 # Numbering beams
beamsGN = 0 #Numbering beamgroup
profN = 0 # Numbering profiles
Nodes.append("<Nodes>")
Plates.append("<Plates>")
Beams.append("<Beams>")
Beamgroup.append("<Beamgroup>")

Profiles.append("<Profiles>")

for i in obj1:
    nm = i.__class__.__name__
    if nm == 'Panel':
        plateN = plateN + 1
        Plates.append("<Number>" + str(plateN) + "</Number>")
        for j in i.origincurve.points:
            n = n + 1
            Nodes.append("<Number>" + str(n) + "</Number>")
            Nodes.append("<X>" + str(j.x) + "</X>")
            Nodes.append("<Y>" + str(j.y) + "</Y>")
            Nodes.append("<Z>" + str(j.z) + "</Z>")
            Plates.append("<Node>" + str(n) + "</Node>")
        Plates.append("<h>" + str(i.thickness) + "</h>")
        Plates.append("<Material_type>" + "c9a5876f475cefab7cc11281b017914a1" + "</Material_type>") #material nog uitlezen
        Plates.append("<Material>" + "C20/25" + "</Material>") #material nog uitlezen
        Plates.append("<Z>" + "0" + "</Z>")
        Plates.append("<Top_Center_Bottom>" + "Center" + "</Top_Center_Bottom>")

    elif nm == 'Frame':
        profN = profN + 1
        Profiles.append("<Number>" + str(profN) + "</Number>")
        Profiles.append("<Profile_name>" + i.profileName + "</Profile_name>")
        if i.material.name == "BaseSteel":
            Profiles.append("<Material_type>" + "0" + "</Material_type>")
            Profiles.append("<Material>" + "S235" + "</Material>")
        else:
            Profiles.append("<Material_type>" + "0" + "</Material_type>")
            Profiles.append("<Material>" + "S235" + "</Material>")
        Profiles.append("<Angle>" + "0" + "</Angle>")

        beamsGN = beamsGN + 1
        Beamgroup.append("<Number>" + str(beamsGN) + "</Number>")

        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(i.start.x) + "</X>")
        Nodes.append("<Y>" + str(i.start.y) + "</Y>")
        Nodes.append("<Z>" + str(i.start.z) + "</Z>")

        Beamgroup.append("<Startnode>" + str(n) + "</Startnode>")

        beamsN = beamsN + 1
        Beams.append("<Number>" + str(beamsN) + "</Number>")
        Beams.append("<Beamgroupnumber>" + str(beamsGN) + "</Beamgroupnumber>")
        Beams.append("<From_node_number>" + str(n) + "</From_node_number>")

        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(i.end.x) + "</X>")
        Nodes.append("<Y>" + str(i.end.y) + "</Y>")
        Nodes.append("<Z>" + str(i.end.z) + "</Z>")

        Beamgroup.append("<Endnode>" + str(n) + "</Endnode>")

        Beams.append("<To_node_number>" + str(n) + "</To_node_number>")
        Beams.append("<Angle>" + str(i.rotation) + "</Angle>")
        Beams.append("<Angle_profile>" + "0" + "</Angle_profile>")
        Beams.append("<Profile_number>" + str(profN) + "</Profile_number>")
        Beams.append("<Z>" + str(i.ZOffset) + "</Z>")
        Beams.append("<Top_Center_Bottom>" + i.YJustification + "</Top_Center_Bottom>")
    elif nm == 'Grid':
        message = 'Hello'

Nodes.append("</Nodes>")
Plates.append("</Plates>")
Beams.append("</Beams>")
Profiles.append("</Profiles>")
Beamgroup.append("</Beamgroup>")

Nodes = ''.join(str(N) for N in Nodes)
Plates = ''.join(str(P) for P in Plates)
Beams = ''.join(str(B) for B in Beams)
Beamgroup = ''.join(str(BP) for BP in Beamgroup)
Profiles = ''.join(str(Pr) for Pr in Profiles)

XMLString = Frame1 + Project + ProjectNumber + ExportDate + XMLVersion + Nodes + Supports + Grids + Profiles + Beamgroup + Beams + Plates + RebarLongitudinal + RebarStirrup + Layers + Frame2

filepath = "C:/TEMP/hall.xml"
file = open(filepath, "w")
a = file.write(XMLString)

file.close()

print(XMLString)