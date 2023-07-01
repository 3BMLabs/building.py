from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from project import fileformat
from objects.datum import *
from geometry.systemsimple import *

project = BuildingPy("Project Aanbouw","0")

#INPUT
lengte = 7000
breedte = 3500
hoogte = 3000
mw = 100
spouw = 30


#1 GRIDS
grids = GridSystem.bySpacingLabels("0 " + str(lengte),seqChar,"0" + str(breedte),seqNumber,1000)

project.objects.append(grids)

#2 LEVELS
BaseConcrete = Material.byNameColor("Concrete", Color().RGB([192, 192, 192]))

#3 HSB-wanden
lengte_hsb_wand_1 = breedte-mw-spouw

div = DivisionSystem().by_fixed_distance_unequal_division(lengte_hsb_wand_1,610,610-19,1)

print(div.distances)

sys.exit()
#project.objects.append(Panel.byBaselineHeight(Line(start= Point(1000,0,0),end=Point(3000,0,0)),2500,150,"wand",BaseConcrete.colorint))

project.toSpeckle("92cf563acc")

