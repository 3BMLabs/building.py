from exchange.speckle import *
from exchange.struct4U import *
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

XMLString = XMLExport("<Grids></Grids>", obj)

filepath = "C:/TEMP/CastellatedBeam.xml"

file = open(filepath, "w")
a = file.write(XMLString)

file.close()

print(XMLString)