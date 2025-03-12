from construction.datum import GridLine
from exchange.IFC import CreateIFC, translateObjectsToIFC
from abstract.vector import Point
from geometry.curve import Line
from project.fileformat import BuildingPy

project = BuildingPy()

GridA = GridLine.by_startpoint_endpoint(Line(start=Point(-1000, 0, 0), end=Point(10000, 0, 0)), "A")

ifc_project = CreateIFC()

ifc_project.add_project("My Project")
ifc_project.add_site("My Site")
ifc_project.add_building("Building A")
ifc_project.add_storey("Ground Floor")
ifc_project.add_storey("G2Floor")
project += GridA

translateObjectsToIFC(project.objects, ifc_project)

ifc_project.export("grids.ifc")