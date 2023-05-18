import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import Point
from objects.objectcollection import *
from project.fileformat import *


i = WurksPedestal().byPoint(Point(0,0,100), 200)
k = WurksPedestal().byPoint(Point(0,200,0), 300)
wp = WorkPlane().create

for j in i:
    project.objects.append(j)

for j in k:
    project.objects.append(j)

project.objects.append(wp)


project.toSpeckle("fa4e56aed4")