import sys
import os
from ezdxf import readfile, DXFStructureError, DXFValueError


from project.fileformat import *
from geometry.curve import *
from geometry.point import Point
from geometry.surface import *
from exchange.DXF import *
from exchange.IFC import *
from construction.frame import *
from construction.datum import *
from construction.floor import *


point1 = Point(0, 0, 0)
point2 = Point(10, 0, 0)
point3 = Point(18, 5, 0)
point3 = Point(12, 7, 0)
point4 = Point(0, 5, 0)

floor_points = [point1, point2, point3, point4]

floor_instance = Floor()
floor_instance.points = floor_points
project.objects.append(floor_instance)


ifc_project = CreateIFC()

ifc_project.add_project("My Project")
ifc_project.add_site("My Site")
ifc_project.add_building("Building A")
ifc_project.add_storey("Ground Floor")
ifc_project.add_storey("G2Floor")

translateObjectsToIFC(project.objects, ifc_project)

ifc_project.export("floor.ifc")