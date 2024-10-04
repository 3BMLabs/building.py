import ifcopenshell
from ifcopenshell.api import run
import ifcopenshell.util.placement
import numpy as np
import sys, os
from pathlib import Path
# custom_profile = model.create_entity("IfcIShapeProfileDef", ProfileName="CustomHProfile", ProfileType="AREA", OverallWidth=120, OverallDepth=200, WebThickness=10, FlangeThickness=15, FilletRadius=0)

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import *
from abstract.vector import *
from abstract.matrix import *


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
matrix[:,3][0:3] = (P2[0], P2[1], P2[2])

material_set = run("material.add_material_set", model, name="CustomMaterialSetC1", set_type="IfcMaterialProfileSet")

steel = run("material.add_material", model, name="SteelST01", category="Steel")


pad_punten = [
    (0.0, 0.0, 0.0),  # Beginpunt van het pad
    (0.0, 0.0, 100.0)  # Eindpunt van het pad (voor een verticale extrusie, bijvoorbeeld)
]

# Maak IfcCartesianPoint entiteiten voor de padpunten
pad_ifc_punten = [model.create_entity('IfcCartesianPoint', Coordinates=p) for p in pad_punten]

# Creëer een IfcPolyline voor het pad
pad_polyline = model.create_entity('IfcPolyline', Points=pad_ifc_punten)


externe_punten = [
    (0.0, 0.0),
    (100.0, 0.0), 
    (100.0, 50.0),
    (0.0, 50.0),
    (0.0, 0.0)
]

interne_punten = [
    (25.0, 15.0),
    (75.0, 15.0),
    (75.0, 35.0), 
    (25.0, 35.0), 
    (25.0, 15.0) 
]

externe_ifc_punten = [model.create_entity('IfcCartesianPoint', Coordinates=p) for p in externe_punten]
interne_ifc_punten = [model.create_entity('IfcCartesianPoint', Coordinates=p) for p in interne_punten]

externe_polyline = model.create_entity('IfcPolyline', Points=externe_ifc_punten)
interne_polyline = model.create_entity('IfcPolyline', Points=interne_ifc_punten)

custom_profile_with_void = model.create_entity(
    'IfcArbitraryProfileDefWithVoids',
    ProfileType='AREA',
    ProfileName='CustomProfileWithVoid',
    OuterCurve=externe_polyline,
    InnerCurves=[interne_polyline]
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