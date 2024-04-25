

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


#INPUT
DL = Dimension(Point(0,-1000,0),Point(5400,-1000,0),DT2_5_mm)
print(DL.start)
DL.write(project)

#GRIDS
grids = GridSystem.by_spacing_labels("9x5500",seqChar,"3x5500",seqNumber,1600).write(project)
Grid.by_startpoint_endpoint(Line(Point(100,100,0),Point(-5000,10000,0)),"Q").write(project)
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#PANEL
project.objects.append(Panel.by_baseline_height(Line(start= Point(1000,10800+5400,0),end=Point(5000,10800+5400,0)),2500,150,"Concrete Wall",BaseConcrete.colorint))


#COLUMNS
#project.objects.append(Frame.by_startpoint_endpoint_profile(Point(1000,1000,0),Point(500,1000,3000),"HEA200","Kolom",BaseSteel))
f1 = Frame.by_point_height_rotation(Point(10800,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
f2 = Frame.by_point_height_rotation(Point(0,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
f3 = Frame.by_point_profile_height_rotation(Point(5400,5400,0),3000,"HEA200",0,BaseSteel).write(project)
ColumnTag.by_frame(f2).write(project)
ColumnTag.by_frame(f1).write(project)
ColumnTag.by_frame(f3).write(project)

f4 = Frame.by_startpoint_endpoint_profile(Point(0,3000,0),Point(10800,6000,0),"IPE400","IPE400 zeeg 30 mm",BaseSteel).write(project)
tg = FrameTag.by_frame(f4).write(project)

CS = CoordinateSystem(Point(10800,10800,0),X_axis,YAxis,ZAxis)
t1 = Text(text="Textnote", font_family="calibri", cs=CS, height=200).write()
for x in t1:
    project.objects.append(x)

CS = CoordinateSystem(Point(0,0,0),X_axis,YAxis,ZAxis)
t2 = Text(text="Textnote", font_family="calibri", cs=CS, height=200).write()
for x in t2:
    project.objects.append(x)

#Columntag1 = Columntag().by_cs_text(CS,"HEA200").write()

project.toSpeckle("261190074a")