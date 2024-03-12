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

Height = 3300
Radius = 1000
NumberOfTreads = 20
DegreesSpiral = 360
RadiasSpiral = 100
ThicknessSteel = 5
HeightTreadSupportStart = 80
HeightTreadSupportEnd = 40
ThicknessTread = 10
obj = []

deg = 0
x = 0
dz = Height / NumberOfTreads
z = dz
p2 = Point(x, Radius, z)
ddeg = DegreesSpiral / NumberOfTreads

p1 = Point(0, RadiasSpiral, z)
p11 = Point.translate(p1,Vector3(0,0,-HeightTreadSupportStart))
p4 = Point(0, Radius, z)
p41 = Point.translate(p4,Vector3(0,0,-HeightTreadSupportEnd))

p2 = Point.rotateXY(p1, ddeg * 0.5, 0)
p3 = Point.rotateXY(p1, -ddeg * 0.5, 0)
p5 = Point.rotateXY(p4, ddeg * 0.5, 0)
p6 = Point.rotateXY(p4, -ddeg * 0.5, 0)
TreadCurve = PolyCurve.byPoints([p2,p5,p6,p3,p2])
TreadSupportCurve = PolyCurve.byPoints([p1,p4,p41,p11,p1])

SpiralSegmentCurve = PolyCurve.byPoints([p3, p2, Point.translate(p2,Vector3(0,0,Height)),Point.translate(p3,Vector3(0,0,Height)),p3])

for i in range(NumberOfTreads):
    obj.append(Panel.byPolyCurveThickness(TreadCurve, ThicknessTread, 0, "Tread", BaseSteel.colorint))
    obj.append(Panel.byPolyCurveThickness(TreadSupportCurve, ThicknessSteel, 0, "SupportTread", BaseSteel.colorint))
    obj.append(Panel.byPolyCurveThickness(SpiralSegmentCurve, ThicknessSteel, 0, "SpiralSegment", BaseSteel.colorint))

    TreadCurve = TreadCurve.rotate(ddeg, dz)
    TreadSupportCurve = TreadSupportCurve.rotate(ddeg, dz)
    SpiralSegmentCurve = SpiralSegmentCurve.rotate(ddeg, 0)

SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "a4d620a049", SpeckleObj, "Parametric Spiral Staircase.py")

#Export to XFEM4U XML String

xmlS4U = xmlXFEM4U()
xmlS4U.addBeamsPlates(obj)
xmlS4U.addProject("Struct4U Parametric Stair")
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/mikev/Documents/GitHub/Struct4U/6 Stair Plates/stair.xml"
file = open(filepath, "w")
a = file.write(XMLString)

file.close()
