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
lengte = 7000
breedte = 3500
hoogte = 3000
mw = 100
spouw = 30

#GRIDS
#grids = GridSystem.bySpacingLabels("0 " + str(lengte),seqChar,"0" + str(breedte),seqNumber,1000)
grids = GridSystem.bySpacingLabels("0 8x5400",seqChar,"0 3x5400",seqNumber,1000)
project.objects.append(grids)

BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#PANEL
project.objects.append(Panel.byBaselineHeight(Line(start= Point(1000,10800+5400,0),end=Point(5000,10800+5400,0)),2500,150,"Concrete Wall",BaseConcrete.colorint))


#COLUMNS
#project.objects.append(Frame.byStartpointEndpointProfileName(Point(1000,1000,0),Point(500,1000,3000),"HEA200","Kolom",BaseSteel))
f1 = Frame.by_point_height_rotation(Point(10800,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
f2 = Frame.by_point_height_rotation(Point(0,5400,0),3000,Rectangle("A",400,400).curve,"BK 400x400",0,BaseConcrete).write(project)
f3 = Frame.by_point_profile_height_rotation(Point(5400,5400,0),3000,"HEA200",0,BaseSteel).write(project)
ColumnTag.by_frame(f2).write(project)
ColumnTag.by_frame(f1).write(project)
ColumnTag.by_frame(f3).write(project)

f4 = Frame.byStartpointEndpointProfileName(Point(0,3000,0),Point(10800,6000,0),"IPE400","IPE400 zeeg 30 mm",BaseSteel).write(project)
tg = FrameTag.by_frame(f4).write(project)

DL = Dimension(Point(0,-1000,0),Point(5400,-1000,0),DT2_5_mm)
DL.write(project)


CS = CoordinateSystem(Point(10800,10800,0),XAxis,YAxis,ZAxis)
t1 = Text(text="Textnote", font_family="calibri", cs=CS, scale=0.1).write()
for x in t1:
    project.objects.append(x)

CS = CoordinateSystem(Point(0,0,0),XAxis,YAxis,ZAxis)
t2 = Text(text="Textnote", font_family="calibri", cs=CS, scale=0.1).write()
for x in t2:
    project.objects.append(x)

#Columntag1 = Columntag().by_cs_text(CS,"HEA200").write()

project.toSpeckle("261190074a")

