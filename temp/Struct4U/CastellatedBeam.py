from exchange.speckle import *
from objects.panel import *
from objects.frame import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

nm = "IPE600 Castellated Beam"
b = 220
tw = 12
tf = 19
h = 750 #height beam
h1 = 150 #height above opening
h2 = h-2*h1 #height of the opening
dh = h2/2
b = 350 #minimum width of the opening
b2 = 550 #maximum width of the opening
db = (b2-b)/2 #delta width of the opening
spac = 850 #spacing of the openings
b4 = spac-b2 #width in between

l = 15000

VX = Vector3(1,0,0)
VY = Vector3(0,1,0)
VZ = Vector3(0,0,1)

obj = []


#Middle
xval = 0
n = int(l/spac)+ 2
pnts = []
pnts2 = [] #bottompart

for i in range(n):
    pnts.append(Point(xval ,0, h / 2))
    pnts2.append(Point(xval ,0, h / 2))
    xval = xval + b4
    pnts.append(Point(xval, 0, h / 2))
    pnts2.append(Point(xval, 0, h / 2))
    xval = xval + db
    pnts.append(Point(xval, 0, h / 2 + dh))
    pnts2.append(Point(xval, 0, h / 2 - dh))
    xval = xval + b
    pnts.append(Point(xval, 0, h / 2 + dh))
    pnts2.append(Point(xval, 0, h / 2 - dh))
    xval = xval + db


pnts.append(Point(xval, 0, h / 2))
pnts2.append(Point(xval, 0, h / 2))
xval = xval + b4
pnts.append(Point(xval, 0, h / 2))
pnts.append(Point(xval, 0, h))
pnts.append(Point(0, 0, h))
pnts.append(Point(0, 0, h / 2))

pnts2.append(Point(xval, 0, h / 2))
pnts2.append(Point(xval, 0, 0))
pnts2.append(Point(0, 0, 0))
pnts2.append(Point(0, 0, h / 2))

pnts3 = pnts2.reverse()
crv = PolyCurve.byPoints(pnts)
crv2 = PolyCurve.byPoints(pnts2)

#Topplate
top = PolyCurve.byPoints([
    Point(0, -b/2, h),
    Point(0, b/2, h),
    Point(xval, b/2, h),
    Point(xval, -b/2, h),
    Point(0, -b/2, h)])
#Bottomplate
bottom = top.translate(Vector3(0,0,-h))

#crv = PolyCurve.byPoints([
#    Point(0,0,h/2),
#    Point(l,0,h/2),
#    Point(l,0,h),
#    Point(0,0,h),
#    Point(0,0,h/2)
#])

obj.append(Panel.byPolyCurveThickness(top,tf,-tf,"top",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(bottom,tf,0,"bottom",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(crv,tw,0,"middle",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(crv2,tw,0,"middle",rgb_to_int([192, 192, 192])))
#obj.append(Panel.byPolyCurveThickness(crv,tw,tw/2,"middle",rgb_to_int([192, 192, 192])))

SpeckleObj = translateObjectsToSpeckleObjects(obj)


#Commit = TransportToSpeckle("struct4u.xyz", "eb801b33ca", SpeckleObj, "Castellated Beam")


#ExportXML
Frame1 = "<Frame>"
Project = "<ProjectName>" + "Building.py Castellated Beam" + "</ProjectName>"
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



#Number of nodes:
n = 0
Nodes = []
Plates = []
plateN = 0

Nodes.append("<Nodes>")
Plates.append("<Plates>")
for i in obj:
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
        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(i.start.x) + "</X>")
        Nodes.append("<Y>" + str(i.start.y) + "</Y>")
        Nodes.append("<Z>" + str(i.start.z) + "</Z>")
        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(i.end.x) + "</X>")
        Nodes.append("<Y>" + str(i.end.y) + "</Y>")
        Nodes.append("<Z>" + str(i.end.z) + "</Z>")
    elif nm == 'Grid':
        message = 'Hello'
Nodes.append("</Nodes>")
Plates.append("</Plates>")

Nodes = ''.join(str(N) for N in Nodes)
Plates = ''.join(str(P) for P in Plates)

XMLString = Frame1 + Project + ProjectNumber + ExportDate + XMLVersion + Nodes + Supports + Grids + Profiles + Beamgroup + Beams + Plates + RebarLongitudinal + RebarStirrup + Layers + Frame2

filepath = "C:/TEMP/CastellatedBeam.xml"

file = open(filepath, "w")
a = file.write(XMLString)

file.close()

print(XMLString)