import sys, os
from pathlib import Path




from geometry.point import *
from geometry.curve import Line, PolyCurve
from construction.frame import *
from exchange.scia import *

from construction.analytical import *
# from exchange.speckle import *
from project.fileformat import BuildingPy

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element

import ifcopenshell.util.shape

model = ifcopenshell.open('C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/SingleRoom.ifc')

rooms = model.by_type("IfcSpace")
print(rooms)

project = BuildingPy("TempCommit", "0")

if rooms:
    room = rooms[0]
    print(room)
    shape_representation = room.Representation

    all_points = []
    for representation in shape_representation.Representations:
        for item in representation.Items:
            print(item)
            if item.is_a("IfcExtrudedAreaSolid"):
                profile = item.SweptArea
                if profile.is_a("IfcArbitraryClosedProfileDef"):
                    outer_curve = profile.OuterCurve
                    if outer_curve.is_a("IfcPolyline"):
                        for point in outer_curve.Points:
                            all_points.append(Point(point.Coordinates[0], point.Coordinates[1], 0))

                direction = item.ExtrudedDirection
                depth = item.Depth
                dx, dy, dz = direction.DirectionRatios if len(direction.DirectionRatios) == 3 else (*direction.DirectionRatios, 0)
                extrusion_point = (dx * depth, dy * depth, dz * depth)
                all_points.append(extrusion_point)

            elif item.is_a("IfcFacetedBrep"):
                for shell in item.Outer.CfsFaces:
                    for loop in shell.Bounds:
                        for vertex in loop.Bound.Polygon:
                            coord = vertex.Coordinates
                            pt = Point(coord[0], coord[1], coord[2])
                            project.objects.append(pt)
                            all_points.append(pt)

    print("Alle punten:", all_points)
else:
    print("Er zijn geen ruimtes in het model.")


project.objects = [2,3,3,1]
project.to_speckle("6d9555e57f")
