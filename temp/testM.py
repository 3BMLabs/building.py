import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from project.fileformat import *
from objects.frame import *
from abstract.text import *
from geometry.point import *


Project = BuildingPy(name="testproject",number="0")

Text1 = Text(text="test", font_family="arial", bounding_box=False, xyz=Point(10, 10, 10), rotation=0)
frame = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(4000,0,0), "IPE600", "IPE", BaseSteel)

ln = Line(start= Point(0,0,0), end = Point(0,3000,0))
diam = 250
startpnt = ln.end
endpnt = Point.translate(ln.end, Vector3(0, diam, 0))

#endpnt = Point.translate(ln.end, Vector3.scale(Vector3.normalize(Vector3.byLine(ln)),diam))
midpnt1 = Point.translate(ln.end, Vector3(diam/2,diam/2,0))
midpnt2 = Point.translate(ln.end, Vector3(-diam/2,diam/2,0))
fac = 1000
#part1 = Arc(startPoint = startpnt, midPoint = midpnt1, endPoint = endpnt)
part1 = Arc(startPoint = Point(0,3000/fac,0), midPoint = Point(50/fac,3050/fac,0), endPoint = Point(0,3100/fac,0))
part2 = Arc(startPoint = Point(0,3000/fac,0), midPoint = Point(-50/fac,3050/fac,0), endPoint = Point(0,3100/fac,0))
Text2 = Text(text="A", font_family="arial", bounding_box=False, xyz=Point(0,-6000, 5), rotation=0)
Text2.character_offset = 50
Text2.space_between = 350


Project.objects.append(frame)
Project.objects.append(Text1)
Project.objects.append(Text2)

Project.objects.append(ln)
Project.objects.append(part1)
Project.objects.append(part2)


Project.toSpeckle("e77454f5e0","test 2")