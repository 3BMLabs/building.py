from construction.frame import *
from exchange.struct4U import *
from construction.analytical import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

project = BuildingPy("Industrial Hall","7")

#INPUT
spac_x = 6500 #grid spacing 1
n = 7 # number of grids 1
spac_y = 6000 #grid spacing 2
nw = 4 # number of grids 2
strX = str(n+1) + "x" + str(spac_x)
strY = str(nw) + "x" + str(spac_y)

#GRIDS
grids = GridSystem.by_spacing_labels(strX,seqChar,strY,seqNumber,2500).write(project)
z = 9000 #height of the structure
afschot = 0

#PROFILES
GEVELKOLOM = "IPE330"
HOOFDLIGGER = "HEA800"
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
y = spac_y*nw #width hall
width = y
spac = spac_x
l = (n+1) * spac
length = l

#SPANTEN
for i in range(n):
    f1 = Frame.by_startpoint_endpoint_profile(Point(spac_x, 0, z), Point(spac_x, y * 0.5, z + afschot), HOOFDLIGGER, HOOFDLIGGER, BaseSteel).write(project)
    FrameTag.by_frame(f1).write(project)
    Frame.by_startpoint_endpoint_profile(Point(spac_x, y * 0.5, z + afschot), Point(spac_x, y, z), HOOFDLIGGER, HOOFDLIGGER, BaseSteel).write(project)
    k1 = Frame.by_startpoint_endpoint_profile(Point(spac_x, 0, 0), Point(spac_x, 1, z), GEVELKOLOM, GEVELKOLOM, BaseSteel).write(project)
    ColumnTag.by_frame(k1).write(project)
    k2 = Frame.by_startpoint_endpoint_profile(Point(spac_x, y, 0), Point(spac_x, y+1, z), GEVELKOLOM, GEVELKOLOM, BaseSteel).write(project)
    ColumnTag.by_frame(k2).write(project)
    spac_x = spac_x + spac

#FOUNDATION BEAM
fb1 = Frame.by_startpoint_endpoint(Point(0,0,0), Point(0,y,0), FOUNDATIONBEAM,"FB 400x600",0,BaseConcrete).write(project)
fb2 = Frame.by_startpoint_endpoint(Point(l,0,0), Point(l,y,0), FOUNDATIONBEAM,"FB 400x600",0,BaseConcrete).write(project)
fb3 = Frame.by_startpoint_endpoint(Point(0,0,0), Point(l,0,0), FOUNDATIONBEAM,"FB 400x600",0,BaseConcrete).write(project)
fb4 = Frame.by_startpoint_endpoint(Point(0,y,0), Point(l,y,0), FOUNDATIONBEAM,"FB 400x600",0,BaseConcrete).write(project)
FrameTag.by_frame(fb1).write(project)
FrameTag.by_frame(fb2).write(project)
FrameTag.by_frame(fb3).write(project)
FrameTag.by_frame(fb4).write(project)

#RANDLIGGERS & KOPPELKOKERS
spac_x = 0
for i in range(n+1): #elk stramienvak + 1
    rl1 = Frame.by_startpoint_endpoint_profile(Point(spac_x, 0, z), Point(spac_x + spac, 0, z), RANDLIGGER, RANDLIGGER, BaseSteel).write(project)
    FrameTag.by_frame(rl1).write(project)

    rl2 = Frame.by_startpoint_endpoint_profile(Point(spac_x, y, z), Point(spac_x + spac, y, z), RANDLIGGER, RANDLIGGER, BaseSteel).write(project)
    FrameTag.by_frame(rl2).write(project)

    ys = spac_y
    for i in range(nw-1):
        kk = Frame.by_startpoint_endpoint_profile(Point(spac_x, ys, z), Point(spac_x + spac, ys, z), KOPPELLIGGER, KOPPELLIGGER, BaseSteel).write(project)
        FrameTag.by_frame(kk).write(project)
        ys = ys + spac_y
    spac_x = spac_x + spac

#KOPGEVEL
spac_x = 0
for i in range(2): #VOORZIJDE EN ACHTERZIJDE
    hk1 = Frame.by_startpoint_endpoint_profile(Point(spac_x, 0, 0), Point(spac_x, 1, z), HOEKKOLOM, HOEKKOLOM, BaseSteel).write(project)
    ColumnTag.by_frame(hk1).write(project)

    hk2 = Frame.by_startpoint_endpoint_profile(Point(spac_x, y, 0), Point(spac_x, y+1, z), HOEKKOLOM, HOEKKOLOM, BaseSteel).write(project)
    ColumnTag.by_frame(hk2).write(project)

    ys = spac_y
    for i in range(nw-1):
        hk3 = Frame.by_startpoint_endpoint_profile(Point(spac_x, ys, 0), Point(spac_x, ys+1, z), KOPGEVELKOLOM, KOPGEVELKOLOM, BaseSteel).write(project)
        ColumnTag.by_frame(hk3).write(project)

        ys = ys + spac_y
    ys = 0
    for i in range(nw):
        rb1 = Frame.by_startpoint_endpoint_profile(Point(spac_x, ys, z), Point(spac_x, ys + spac_y, z), RANDLIGGER_KOPGEVEL, RANDLIGGER_KOPGEVEL, BaseSteel).write(project)
        ys = ys + spac_y
        FrameTag.by_frame(rb1).write(project)

    spac_x = l

#WVB in gevel #Positie 1: K1, K2, L1 of L2: K1 is kopgevel 1, #K2 is kopgevel 2, #L1 is langsgevel 1, L2 is langsgevel 2 #Positie 2: Vaknummer #Positie 3: Over hoeveel stramien verdelen

for i in wvb: #For loop for vertical bracing
    if i[0] == "K1": #kopgevel 1
        Frame.by_startpoint_endpoint_profile(Point(0, (i[1]-1) * spac_y, 0), Point(0, (i[1]) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
        Frame.by_startpoint_endpoint_profile(Point(0, (i[1]) * spac_y, 0), Point(0, (i[1]-1) * spac_y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
    elif i[0] == "K2":
        spac_x = l
        Frame.by_startpoint_endpoint_profile(Point(spac_x, (i[1] - 1) * spac_y, 0), Point(spac_x, (i[1]) * spac_y, z), WVB_GEVEL, "WVB KOPGEVEL", BaseSteel).write(project)
        Frame.by_startpoint_endpoint_profile(Point(spac_x, (i[1]) * spac_y, 0), Point(spac_x, (i[1] - 1) * spac_y, z), WVB_GEVEL, "WVB KOPGEVEL", BaseSteel).write(project)
    elif i[0] == "L1":
        Frame.by_startpoint_endpoint_profile(Point((i[1]-1) * spac, 0, 0), Point((i[1]) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
        Frame.by_startpoint_endpoint_profile(Point((i[1]) * spac, 0, 0), Point((i[1]-1) * spac, 0, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
    elif i[0] == "L2":
        Frame.by_startpoint_endpoint_profile(Point((i[1] - 1) * spac, y, 0), Point((i[1]) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
        Frame.by_startpoint_endpoint_profile(Point((i[1]) * spac, y, 0), Point((i[1] - 1) * spac, y, z), WVB_GEVEL,"WVB KOPGEVEL", BaseSteel).write(project)
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
    Frame.by_startpoint_endpoint_profile(
        Point(x1, y1, z),
        Point(x2, y2, z),
        WVB_DAK,"WVB DAK", BaseSteel).write(project)

project.toSpeckle("dca7c22b3e")