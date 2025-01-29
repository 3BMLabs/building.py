from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from project import fileformat
from construction.datum import *
from geometry.systemsimple import *

project = BuildingPy("Project Aanbouw","0")

#INPUT
lengte = 7000
breedte = 3500
hoogte = 3000
mw = 100
spouw = 30

#1 GRIDS
grids = GridSystem.by_spacing_labels("0 " + str(lengte),seqChar,"0" + str(breedte),seqNumber,1000)

project.objects.append(grids)

#2 LEVELS
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#3 HSB-wanden
lengte_hsb_wand_1 = breedte-mw-spouw
spacing = 407
length = 6000

div1 = DivisionSystem().by_fixed_distance_unequal_division(lengte_hsb_wand_1,610,610-19,1)
div2 = DivisionSystem().by_fixed_number_equal_spacing(3000,4)
div3 = DivisionSystem().by_fixed_distance_equal_division(3000,610,0)

div2 = DivisionSystem().by_fixed_distance_unequal_division(length,spacing,spacing-19,0)
wall = RectangleSystem().by_width_height_divisionsystem_studtype(length,2000,38,184,div2,True)

project.objects.append(wall.symbolic_inner_mother_surface)

#for i in wall.outer_frame_objects:
#    project.objects.append(i)
#for i in wall.symbolic_outer_grids:
#    project.objects.append(i)
#for i in wall.symbolic_inner_grids:
#    project.objects.append(i)

for i in wall.outer_frame_objects:
    project.objects.append(i)
for i in wall.inner_frame_objects:
    project.objects.append(i)

for i in wall.panel_objects:
    project.objects.append(i)

#project.objects.append(Panel.by_baseline_height(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand",BaseConcrete.colorint))

project.to_speckle("92cf563acc")

