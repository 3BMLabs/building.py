from objects.frame import *
from exchange.speckle import *
from objects.datum import *

# GridSystem
seqX = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC"
seqY = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24"
ext = 5000 #offset stramien

#INPUT in mm
spac = 7000 #stramien in langsrichting
n = 10 # aantal stramienvakken

spac_y = 5200 #stramien in dwarsrichting
nw = 5 # n-stramienen dwarsrichting

z = 9000 #hoogte hal
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
y = spac_y*nw #breedte hal
l = (n+1) * spac

spacX = str(n+1) + "x" + str(spac)  #"13x5400"
spacY = str(nw) + "x" + str(spac_y)  #"4x5400"
grids = GridSystem(spacX,seqX,spacY,seqY,ext)
obj1 = grids[0] + grids[1]

#obj1 = []
#SPANTEN
for i in range(n):
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, z), Point(x, y*0.5, z+afschot), HOOFDLIGGER, "Hoofdligger deel 1")) # dakligger deel 1
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y*0.5, z+afschot), Point(x, y, z), HOOFDLIGGER,"Hoofdligger deel 2"))  # dakligger deel 2
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), GEVELKOLOM, "Kolom 1")) # kolom 1
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), GEVELKOLOM, "Kolom 2"))  # kolom 2
    x = x + spac

#RANDLIGGERS & KOPPELKOKERS
x = 0
for i in range(n+1): #elk stramienvak + 1
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, z), Point(x+spac, 0, z), RANDLIGGER, "Randligger 1"))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, z), Point(x+spac, y, z), RANDLIGGER, "Randligger 2"))
    ys = spac_y
    for i in range(nw-1):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, z), Point(x+spac, ys, z), KOPPELLIGGER,"Koppelkoker"))
        ys = ys + spac_y
    x = x + spac

#WINDVERBANDEN DAK
x = 0

#KOPGEVEL
x = 0
for i in range(2): #VOORZIJDE EN ACHTERZIJDE
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, 0, 0), Point(x, 0, z), HOEKKOLOM, "HOEKKOLOM 1"))
    obj1.append(Frame.byStartpointEndpointProfileName(Point(x, y, 0), Point(x, y, z), HOEKKOLOM, "HOEKKOLOM 2"))
    ys = spac_y
    for i in range(nw-1):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, 0), Point(x, ys, z), KOPGEVELKOLOM,"KOPGEVELKOLOM"))
        ys = ys + spac_y
    ys = 0
    for i in range(nw):
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, ys, z), Point(x, ys+spac_y, z), RANDLIGGER_KOPGEVEL, "RANDLIGGER KOPGEVEL"))
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
        obj1.append(Frame.byStartpointEndpointProfileName(Point(0, (i[1]-1) * spac_y, 0), Point(0, (i[1]) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL"))
        obj1.append(Frame.byStartpointEndpointProfileName(Point(0, (i[1]) * spac_y, 0), Point(0, (i[1]-1) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL"))
    elif i[0] == "K2":
        x = l
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, (i[1]-1) * spac_y, 0), Point(x, (i[1]) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL"))
        obj1.append(Frame.byStartpointEndpointProfileName(Point(x, (i[1]) * spac_y, 0), Point(x, (i[1]-1) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL"))
    elif i[0] == "L1":
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]-1) * spac, 0, 0), Point((i[1]) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL"))
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]) * spac, 0, 0), Point((i[1]-1) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL"))
    elif i[0] == "L2":
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1] - 1) * spac, y, 0), Point((i[1]) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL"))
        obj1.append(Frame.byStartpointEndpointProfileName(Point((i[1]) * spac, y, 0), Point((i[1] - 1) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL"))
    else:
        pass

#Belastingen



SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "95f9fd2609", SpeckleObj, "Parametric Structure.py")