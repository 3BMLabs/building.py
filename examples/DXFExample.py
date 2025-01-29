import sys, os, math
from pathlib import Path
import ifcopenshell
from ifcopenshell.api import run
import ifcopenshell.util.placement
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
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

project = BuildingPy("DXF","0001") 

readedDXF = ReadDXF("library/object_database/DXF/VBI Isolatieplaatvloer K260 Randoplegging.dxf")

obj = Surface.by_patch_inner_and_outer(readedDXF.polylines)


for index, pl2 in enumerate(readedDXF.polylines):
    project.objects.append(pl2)

project.objects.append(obj)

project.to_speckle("7603a8603c")


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


column_type = run("root.create_entity", model, ifc_class="IfcColumnType", name="CustomColumnC1")

matrix = np.eye(4)

material_set = run("material.add_material_set", model, name="CustomMaterialSetC1", set_type="IfcMaterialProfileSet")

steel = run("material.add_material", model, name="SteelST01", category="Steel")


interne_punten = []
for polycurve in obj.inner_Polygon:
    interne = []
    for pt in polycurve.points:
        interne.append((pt.x, pt.y))
    interne_punten.append(interne)


externe_punten = []
for pt in obj.outer_Polygon.points:
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


run("material.add_profile", model, profile_set=material_set, material=steel, profile=custom_profile_with_void)

run("material.assign_material", model, product=column_type, material=material_set)

column = run("root.create_entity", model, ifc_class="IfcColumn")

run("geometry.edit_object_placement", model, product=column, matrix=matrix, is_si=True)

run("type.assign_type", model, related_object=column, relating_type=column_type)

representation = run("geometry.add_profile_representation", model, context=body, profile=custom_profile_with_void, depth=34)

run("geometry.assign_representation", model, product=column, representation=representation)

run("spatial.assign_container", model, relating_structure=storey, product=column)

model.write("model1.ifc")