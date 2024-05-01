import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project.fileformat import *
from geometry.curve import *
from geometry.point import Point
from geometry.geometry2d import Point2D, Line2D, Arc2D, PolyCurve2D
from geometry.surface import *
from exchange.DXF import *
from exchange.IFC import *
from abstract.coordinatesystem import *
from objects.frame import *
from objects.datum import *

GridA = Grid.by_startpoint_endpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A") #check text direction
# project.objects.append(GridA)


project.objects.append(Text(text="A", font_family="calibri", height=200, cs=CoordinateSystem(Point(0,0,0), X_axis, YAxis, ZAxis)))
print(project.objects)

# print(project.objects[2].write())

project.toSpeckle("7603a8603c")

# convert grid to IFC grid.
