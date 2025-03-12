
from abstract.color import Color
from abstract.vector import Point
from construction.annotation import ColumnTag, BeamTag
from construction.beam import Beam
from construction.datum import GridLine, Grid, seqChar, seqNumber
from construction.panel import Panel
from geometry.curve import Line
from library.material import BaseSteel, Material
from library.profile import profile_by_name
from project.fileformat import BuildingPy


project = BuildingPy("Stalen kolommen","0")
project.round = True
project.closed = False

#INPUT

#GRIDS
grids = Grid.by_spacing_labels("6x5400",seqChar,"4x5400",seqNumber,2000).write(project)
GridLine.by_startpoint_endpoint(Line(Point(100,100,0),Point(-5000,10000,0)),"Q").write(project)
BaseConcrete = Material.byNameColor("Concrete", Color.RGB([192, 192, 192]))

#PANEL
project.objects.append(Panel.by_baseline_height(Line(start= Point(1000,10800+5400,0),end=Point(5000,10800+5400,0)),2500,150,"Concrete Wall",BaseConcrete.colorint))

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
    f = Beam.by_point_height_rotation(Point(x, 0, 0), 3000, profile_by_name(i).curve, i, 0, BaseSteel).write(project)
    ColumnTag.by_beam(f).write(project)


f4 = Beam.by_startpoint_endpoint_profile(Point(0,3000,0),Point(10800,6000,0),"IPE400","IPE400 zeeg 30 mm",BaseSteel).write(project)
tg = BeamTag.by_frame(f4).write(project)

project.to_speckle("e973243375")
