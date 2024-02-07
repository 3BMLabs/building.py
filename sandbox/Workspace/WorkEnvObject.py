import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.panel import *
from objects.frame import *
from objects.datum import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *
from objects.shape import *

def gridPlane(x_length, y_length, spacing):
    startpoint = Point(100,100,0)
    # translate

    x_step = int(round(x_length/spacing,0))+1
    y_step = int(round(y_length/spacing,0))+1

    lines = []

    for i in range(x_step):
        line = Line(Point(0,i*spacing,0), Point(y_length,i*spacing,0))
        lines.append(line)
        project.objects.append(line)

    for i in range(y_step):
        line = Line(Point(i*spacing,0,0), Point(i*spacing, x_length,0))
        lines.append(line)
        project.objects.append(line)

    return lines