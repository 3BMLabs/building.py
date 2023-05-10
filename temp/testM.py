import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from fileformat.fileformat import *
from objects.frame import *
from abstract.text import *
from geometry.point import *


Project = BuildingPy(name="testproject",number="0")

Text1 = Text(text="test", font_family="arial", bounding_box=False, xyz=Point(10, 10, 10), rotation=0)
frame = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(4000,0,0), "IPE600", "IPE", BaseSteel)

Project.objects.append(frame)
Project.objects.append(Text1)


Project.toSpeckle("fa4e56aed4","test 2")