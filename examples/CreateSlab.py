
from abstract.vector import Point
from construction.floor import Floor
from exchange.IFC import CreateIFC, translateObjectsToIFC
from project.fileformat import BuildingPy

project = BuildingPy()

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
