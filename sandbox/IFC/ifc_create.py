import ifcopenshell
from ifcopenshell.api import run
import numpy as np


def move_in_3D_matrix(start, end):
    """
    Mark start and end points in a 4x4x4 matrix (3D grid).
    
    Parameters:
    - start: Tuple[int, int, int], the starting coordinates (x, y, z).
    - end: Tuple[int, int, int], the ending coordinates (x, y, z).
    
    Returns:
    - numpy.ndarray: A 4x4x4 matrix with marked start and end points.
    """
    # Create a 4x4x4 matrix filled with zeros
    matrix = np.zeros((4, 4, 4), dtype=int)
    
    # Mark the start point with 1
    matrix[start] = 1
    
    # Mark the end point with 2
    matrix[end] = 2
    
    return matrix

# Create a blank model
model = ifcopenshell.file()

# All projects must have one IFC Project element
project = run("root.create_entity", model, ifc_class="IfcProject", name="My Project")

# Geometry is optional in IFC, but because we want to use geometry in this example, let's define units
# Assigning without arguments defaults to metric units
run("unit.assign_unit", model)

# Let's create a modeling geometry context, so we can store 3D geometry (note: IFC supports 2D too!)
context = run("context.add_context", model, context_type="Model")

# In particular, in this example we want to store the 3D "body" geometry of objects, i.e. the body shape
body = run("context.add_context", model, context_type="Model",
    context_identifier="Body", target_view="MODEL_VIEW", parent=context)

# Create a site, building, and storey. Many hierarchies are possible.
site = run("root.create_entity", model, ifc_class="IfcSite", name="My Site")
building = run("root.create_entity", model, ifc_class="IfcBuilding", name="Building A")
storey = run("root.create_entity", model, ifc_class="IfcBuildingStorey", name="Ground Floor")

# Since the site is our top level location, assign it to the project
# Then place our building on the site, and our storey in the building
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
matrix = ifcopenshell.util.placement.rotation(90, "Y") @ matrix
matrix[:,3][0:3] = (3, 2, 5)

# Example usage
# start_point = (0, 0, 0)  # Starting at one corner of the 3D grid
# end_point = (3, 3, 3)    # Ending at the opposite corner of the 3D grid
# matrix = move_in_3D_matrix(start_point, end_point)
# print(matrix)


material_set = run("material.add_material_set", model, name="B1", set_type="IfcMaterialProfileSet")
steel = run("material.add_material", model, name="ST01", category="steel")
hea100 = model.create_entity("IfcIShapeProfileDef", ProfileName="HEA100", ProfileType="AREA", OverallWidth=100, OverallDepth=96, WebThickness=5, FlangeThickness=8, FilletRadius=12, )
run("material.add_profile", model, profile_set=material_set, material=steel, profile=hea100)
run("material.assign_material", model, product=beam_type, material=material_set)
beam = run("root.create_entity", model, ifc_class="IfcBeam")
run("geometry.edit_object_placement", model, product=beam, matrix=matrix, is_si=True)
run("type.assign_type", model, related_object=beam, relating_type=beam_type)
representation = run("geometry.add_profile_representation", model, context=body, profile=hea100, depth=1)
run("geometry.assign_representation", model, product=beam, representation=representation)
run("spatial.assign_container", model, relating_structure=storey, product=beam)



# Write out to a file
model.write("model.ifc")