

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

project = BuildingPy("Stalen kolommen","0")
project.round = True
project.closed = False
from itertools import count

#INPUT

#GRIDS
#grids = GridSystem.bySpacingLabels("6x5400",seqChar,"4x5400",seqNumber,2000).write(project)
#Grid.byStartpointEndpoint(Line(Point(100,100,0),Point(-5000,10000,0)),"Q").write(project)
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#PANEL
#project.objects.append(Panel.byBaselineHeight(Line(start= Point(1000,10800+5400,0),end=Point(5000,10800+5400,0)),2500,150,"Concrete Wall",BaseConcrete.colorint))

lst = ["HEA100",
       "DIE14",
       "UNP200",
       "B168.3/8",
       #"T100/100/11",
       "UPE200",
       "S100/5",
       "R50",
       "L50/50/5",
       "K120/80/8",
       #"C150/50/2"
]

spacing = 1000
x = 0

for i in lst:
    x = x+spacing
    f = Frame.by_point_height_rotation(Point(x, 0, 0), 3000, profiledataToShape(i).polycurve2d, i, 0, BaseSteel).write(project)
    ColumnTag.by_frame(f).write(project)


#f4 = Frame.byStartpointEndpointProfileName(Point(0,3000,0),Point(10800,6000,0),"IPE400","IPE400 zeeg 30 mm",BaseSteel).write(project)
#tg = FrameTag.by_frame(f4).write(project)

project.toSpeckle("e973243375")
