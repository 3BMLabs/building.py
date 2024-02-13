import ifcopenshell
from ifcopenshell.api import run

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

wall = run("root.create_entity", model, ifc_class="IfcWall")

run("geometry.edit_object_placement", model, product=wall)

representation = run("geometry.add_wall_representation", model, context=body, length=50, height=3, thickness=1)

run("geometry.assign_representation", model, product=wall, representation=representation)

run("spatial.assign_container", model, relating_structure=storey, product=wall)

model.write("model.ifc")
print(f"Model: {model} created")