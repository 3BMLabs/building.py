from abstract.vector import Point
from construction.datum import GridLine
from geometry.curve import Line, PolyCurve
from project.fileformat import BuildingPy


polycurve = PolyCurve.by_points([Point(0,0,0), Point(100,0,0), Point(100,100,0), Point(0,100,0)])
height = 10.0
dz_loc = 0.0

l1 = Line(Point(0,0,0), Point(0,1000,0))

gr = GridLine.by_startpoint_endpoint(l1, "Grid")

project = BuildingPy()
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