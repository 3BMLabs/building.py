
# Test text

from fileformat.fileformat import *
from objects.frame import *
from abstract.text import *

Project = BuildingPy(name="testproject",number="0")


Text1 = Text(text="PyBuildingSystem1", font_family="arial", bounding_box=False, xyz=[0, 0, 0], rotation=90).write()

frame = Frame.byStartpointEndpointProfileName(Point(0,0,0), Point(4000,0,0), "IPE600", "IPE", BaseSteel)

Project.objects.append(frame)
Project.objects.append(Text1)


Project.toSpeckle("a5de7fe769","test 2")