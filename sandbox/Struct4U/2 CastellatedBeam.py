from exchange.struct4U import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

nm = "IPE600 Castellated Beam"
b = 220 #width
tw = 12
tf = 19
h = 750 #height beam
h1 = 150 #height above opening
b1 = 350 #minimum width of the opening
b2 = 550 #maximum width of the opening
spac = 850 #spacing of the openings
l = 15000 #length

def CastellatedBeam(b,h,h1,b1,b2,spac,l):
    h2 = h-2*h1 #height of the opening
    dh = h2/2
    db = (b2-b1)/2 #delta width of the opening
    b4 = spac-b2 #width in between

    VX = Vector3(1,0,0)
    VY = Vector3(0,1,0)
    VZ = Vector3(0,0,1)

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
    return top, bottom, crv, crv2

CB = CastellatedBeam(b,h,h1,b1,b2,spac,l)

obj = []

obj.append(Panel.byPolyCurveThickness(CB[0],tf,-tf,"top",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(CB[1],tf,0,"bottom",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(CB[2],tw,0,"middle",rgb_to_int([192, 192, 192])))
obj.append(Panel.byPolyCurveThickness(CB[3],tw,0,"middle",rgb_to_int([192, 192, 192])))

SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle("struct4u.xyz", "eb801b33ca", SpeckleObj, "Castellated Beam")

#Export to XFEM4U XML String
xmlS4U = xmlXFEM4U()
xmlS4U.addBeamsPlates(obj)
xmlS4U.addProject("Castellated Beam")
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/2 Castellated Beam/Castellated Beam.xml"
file = open(filepath, "w")
a = file.write(XMLString)

file.close()