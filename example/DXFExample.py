import sys, os, math
from pathlib import Path
import ifcopenshell
from ifcopenshell.api import run
import ifcopenshell.util.placement
import numpy as np

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
from abstract.intersect2d import is_polycurve_in_polycurve
from packages.helper import flatten

from geometry.point import *
from abstract.vector import *
from abstract.matrix import *


project = BuildingPy("DXF","0001")

# xample = "library/object_database/DXF/PS-isolatievloer 200 Rc=3,5 PURGE.dxf"
xample = "library/object_database/DXF/Appartementenvloer 320 test copy leeg docu.dxf"

readedDXF = ReadDXF(xample)

# print(readedDXF.lines)
# print(readedDXF.arcs)
# print(readedDXF.polylines)


#temp inner function.


# get lines of polycurve 1

extr = Extrusion()

for index, pl2 in enumerate(readedDXF.polylines):
    project.objects.append(pl2)
    if index == 0:
        pl3 = PolyCurve.by_polycurve_2D(pl2)
        extr.by_polycurve_height_vector(polycurve_2d=pl3,
                                                        height=20000, 
                                                        cs_old=CoordinateSystem(Point(0,0,0), X_axis, YAxis, ZAxis), 
                                                        start_point=Point(0,0,0), 
                                                        direction_vector=Vector3(0,0,1)
                                                        )
        extr.outercurve.append(pl2)
    else:
        extr.innercurve.append(pl2)








model = ifcopenshell.file()

project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")

run("unit.assign_unit", model)

context = run("context.add_context", model, context_type="Model")

body = run("context.add_context", model, context_type="Model",
    context_identifier="Body", target_view="MODEL_VIEW", parent=context)

site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

run("aggregate.assign_object", model, relating_object=project, product=site)
run("aggregate.assign_object", model, relating_object=site, product=building)
run("aggregate.assign_object", model, relating_object=building, product=storey)


P1 = [43,1,-45]
P2 = [8,23,12]

column_type = run("root.create_entity", model, ifc_class="IfcColumnType", name="CustomColumnC1")

matrix = np.eye(4)

material_set = run("material.add_material_set", model, name="CustomMaterialSetC1", set_type="IfcMaterialProfileSet")

steel = run("material.add_material", model, name="SteelST01", category="Steel")


externe_punten = []
for polycurve in extr.outercurve:
    for pt in polycurve.points2D:
        externe_punten.append((pt.x, pt.y))


interne_punten = []
for polycurve in extr.innercurve:
    interne = []
    for pt in polycurve.points2D:
        interne.append((pt.x, pt.y))
    interne_punten.append(interne)


externe_punten = []
for polycurve in extr.outercurve:
    for pt in polycurve.points2D:
        externe_punten.append((pt.x, pt.y))

externe_ifc_punten = [model.create_entity('IfcCartesianPoint', Coordinates=p) for p in externe_punten]
externe_polyline = model.create_entity('IfcPolyline', Points=externe_ifc_punten)

interne_polyline_lists = []
for interne in interne_punten:
    interne_ifc_punten = [model.create_entity('IfcCartesianPoint', Coordinates=p) for p in interne]
    interne_polyline = model.create_entity('IfcPolyline', Points=interne_ifc_punten)
    interne_polyline_lists.append(interne_polyline)

custom_profile_with_void = model.create_entity(
    'IfcArbitraryProfileDefWithVoids',
    ProfileType='AREA',
    ProfileName='CustomProfileWithVoid',
    OuterCurve=externe_polyline,
    InnerCurves=interne_polyline_lists
)

# sys.exit()

run("material.add_profile", model, profile_set=material_set, material=steel, profile=custom_profile_with_void)

run("material.assign_material", model, product=column_type, material=material_set)

column = run("root.create_entity", model, ifc_class="IfcColumn")

run("geometry.edit_object_placement", model, product=column, matrix=matrix, is_si=True)

run("type.assign_type", model, related_object=column, relating_type=column_type)

representation = run("geometry.add_profile_representation", model, context=body, profile=custom_profile_with_void, depth=34)

run("geometry.assign_representation", model, product=column, representation=representation)

run("spatial.assign_container", model, relating_structure=storey, product=column)

model.write("model1.ifc")



print(project.objects)

project.toSpeckle("46f2db860e")