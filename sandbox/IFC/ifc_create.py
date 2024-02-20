import ifcopenshell
from ifcopenshell.api import run
import numpy as np
import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from geometry.point import *
from abstract.vector import *


def move_in_3D_matrix(start, end):
    """
    Mark start and end points in a 4x4x4 matrix (3D grid).
    
    Parameters:
    - start: Tuple[int, int, int], the starting coordinates (x, y, z).
    - end: Tuple[int, int, int], the ending coordinates (x, y, z).
    
    Returns:
    - numpy.ndarray: A 4x4x4 matrix with marked start and end points.
    """
    matrix = np.zeros((4, 4, 4), dtype=int)
    
    matrix[start] = 1
    
    matrix[end] = 2
    
    return matrix

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


#create wall
wall = run("root.create_entity", model, ifc_class="IfcWall")
matrix = np.eye(4)
matrix = ifcopenshell.util.placement.rotation(90, "Z") @ matrix
matrix[:,3][0:3] = (0, 0, 5)
run("geometry.edit_object_placement", model, product=wall, matrix=matrix, is_si=True)
representation = run("geometry.add_wall_representation", model, context=body, length=5, height=3, thickness=0.2)
run("geometry.assign_representation", model, product=wall, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=wall)


#create beam
beam_type = run("root.create_entity", model, ifc_class="IfcBeamType", name="B1")
matrix = np.eye(4)
print(matrix)
matrix = ifcopenshell.util.placement.rotation(45, "Y") @ matrix
print(matrix)
matrix[:,3][0:3] = (3, 2, 5)
print(matrix)

#by 2 points

material_set = run("material.add_material_set", model, name="B1", set_type="IfcMaterialProfileSet")
steel = run("material.add_material", model, name="ST01", category="steel")
hea100 = model.create_entity("IfcIShapeProfileDef", ProfileName="HEA100", ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
run("material.add_profile", model, profile_set=material_set, material=steel, profile=hea100)
run("material.assign_material", model, product=beam_type, material=material_set)
beam = run("root.create_entity", model, ifc_class="IfcBeam")
run("geometry.edit_object_placement", model, product=beam, matrix=matrix, is_si=True)
run("type.assign_type", model, related_object=beam, relating_type=beam_type)
representation = run("geometry.add_profile_representation", model, context=body, profile=hea100, depth=1.4)
run("geometry.assign_representation", model, product=beam, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=beam)


#create column
column_type = run("root.create_entity", model, ifc_class="IfcColumnType", name="C1")
matrix = np.eye(4)
# matrix = ifcopenshell.util.placement.rotation(0, "Y") @ matrix
matrix[:,3][0:3] = (3, 2, 5)

# print(matrix)

material_set = run("material.add_material_set", model, name="C1", set_type="IfcMaterialProfileSet")
steel = run("material.add_material", model, name="ST01", category="steel")
hea100 = model.create_entity("IfcIShapeProfileDef", ProfileName="HEA120", ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
run("material.add_profile", model, profile_set=material_set, material=steel, profile=hea100)
run("material.assign_material", model, product=column_type, material=material_set)
column = run("root.create_entity", model, ifc_class="IfcColumn")
run("geometry.edit_object_placement", model, product=column, matrix=matrix, is_si=True)
run("type.assign_type", model, related_object=column, relating_type=column_type)
representation = run("geometry.add_profile_representation", model, context=body, profile=hea100, depth=1)
run("geometry.assign_representation", model, product=column, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=column)


class StructuralElement:
    def __init__(self, name:str, type:str, profile:str, profilename:str, matrix:None, length:float, material:None) -> None:
        # self.id = id
        self.name = name
        self.type = "column" / "beam"
        self.profile = profile
        self.profilename = profilename
        self.matrix = matrix
        self.length = length
        self.material = material


def translate(p1, p2):
    length = Point.distance(p1, p2)

    v1 = Point.toVector(p1)
    v2 = Point.toVector(p2)

    # Vector3.
    # Point.to_matrix()

    print(length)


    #return -> for each axis, the degrees and length

# translate(Point(0,0,0), Point(9,5,0))
p1 = Point(0,0,0)
p2 = Point(9,5,0)

length = Point.distance(p1,p2)
print(length)

# def StructuralElement():


#create a function that create a steel element based on
# (beam/column), 


# Write out to a file
# model.write("model.ifc")