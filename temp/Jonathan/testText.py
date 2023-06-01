import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.text import Text

#startpoint
#vector
Text(text="Start", font_family="arial", bounding_box=False, xyz=Point(0, 0, 0), rotation=Vector3(1, 0, 0)).write()
Text(text="213 4", font_family="arial", bounding_box=False, xyz=Point(0, 4000, 0), rotation=Vector3(1, 0, 0)).write()
# project.objects.append(Text2)

project.toSpeckle("054ccc563c")