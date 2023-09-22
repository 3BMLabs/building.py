

import sys, os, math
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from project import fileformat
from objects.datum import *
from geometry.systemsimple import *
from abstract.text import Text
from objects.annotation import *
project = BuildingPy("Aanbouw","0")
from itertools import count

#INPUT

#GRIDS
grids = GridSystem.bySpacingLabels("6x5400",seqChar,"4x5400",seqNumber,2000).write(project)
Grid.byStartpointEndpoint(Line(Point(100,100,0),Point(-5000,10000,0)),"Q").write(project)
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#PANEL
project.objects.append(Panel.byBaselineHeight(Line(start= Point(1000,10800+5400,0),end=Point(5000,10800+5400,0)),2500,150,"Concrete Wall",BaseConcrete.colorint))

#COLUMNS
f1 = Frame.by_point_height_rotation(Point(10800,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
f2 = Frame.by_point_height_rotation(Point(0,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
#f3 = Frame.by_point_profile_height_rotation(Point(5400,5400,0),3000,"HEA200",0,BaseSteel).write(project)
ColumnTag.by_frame(f2).write(project)
ColumnTag.by_frame(f1).write(project)
#ColumnTag.by_frame(f3).write(project)

f4 = Frame.byStartpointEndpointProfileName(Point(0,3000,0),Point(10800,6000,0),"IPE400","IPE400 zeeg 30 mm",BaseSteel).write(project)
tg = FrameTag.by_frame(f4).write(project)

project.toSpeckle("261190074a")
