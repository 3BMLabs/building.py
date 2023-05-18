import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import Point
from objects.objectcollection import *
from project.fileformat import *


WurksPedestal().byPoint(Point(100,200,0), 300, 90)
WorkPlane().create()


project.toSpeckle("fa4e56aed4")