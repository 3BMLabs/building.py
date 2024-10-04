import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import *
from geometry.curve import *
from objects.void import *
from objects.datum import *
from exchange.IFC import *


polycurve = PolyCurve.by_points([Point(0,0,0), Point(100,0,0), Point(100,100,0), Point(0,100,0)])
height = 10.0
dz_loc = 0.0

l1 = Line(Point(0,0,0), Point(0,1000,0))

gr = Grid.by_startpoint_endpoint(l1, "Grid")

project.objects.append(gr)

# project.toSpeckle("7603a8603c")
project.toIFC()
# ifc_project = CreateIFC()

# ifc_project.add_project("My Project")
# ifc_project.add_site("My Site")
# ifc_project.add_building("Building A")
# ifc_project.add_storey("Ground Floor")
# ifc_project.add_storey("G2Floor")

# translateObjectsToIFC(project.objects, ifc_project)


# ifc_project.export("grids.ifc")