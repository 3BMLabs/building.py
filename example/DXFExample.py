import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from objects.annotation import *
from geometry.solid import *
from exchange.DXF import *

project = BuildingPy("DXF","0001")

# xample = "library/object_database/DXF/PS-isolatievloer 200 Rc=3,5 PURGE.dxf"
xample = "library/object_database/DXF/Appartementenvloer 320 test copy leeg docu.dxf"

readedDXF = ReadDXF(xample)

print(readedDXF.lines)
print(readedDXF.arcs)
print(readedDXF.polylines)

for pl2 in readedDXF.polylines:
    pl3 = PolyCurve.by_polycurve_2D(pl2)
    ext = Extrusion.by_polycurve_height_vector(pl3, 20000, CoordinateSystem(Point(0,0,0), X_axis, YAxis, ZAxis), Point(0,0,0), Vector3(0,0,1))

    project.objects.append(ext)
    project.objects.append(pl2)


project.toSpeckle("46f2db860e")