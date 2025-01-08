import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from exchange.IFC import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from construction.annotation import *
from geometry.solid import *
from exchange.DXF import *
from abstract.intersect2d import is_polycurve_in_polycurve
from packages.helper import flatten

from geometry.point import *
from geometry.vector import *
from geometry.matrix import *
from geometry.surface import *

objects = []

ifc_project = CreateIFC()

ifc_project.add_project("My Project")
ifc_project.add_site("My Site")
ifc_project.add_building("Building A")
ifc_project.add_storey("Ground Floor")
ifc_project.add_storey("G2Floor")


project = BuildingPy("DXF","0001")

readedDXF = ReadDXF("library/object_database/DXF/VBI Isolatieplaatvloer HVU 400 Standaard.dxf")
print(readedDXF.polylines)

obj = Surface.by_patch_inner_and_outer(readedDXF.polylines)


for i in readedDXF.polylines:
    project.objects.append(i)
# project.objects.append(obj)

project.toSpeckle("7603a8603c")

# lst = [PG1, innerPolygon1, innerPolygon2]


# translateObjectsToIFC(project.objects, ifc_project)


# ifc_project.export("my_model.ifc")

# VBI PS-isolatievloer 200 V4
