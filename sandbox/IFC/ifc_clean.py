import ifcopenshell
from ifcopenshell import template

source_model = ifcopenshell.open('C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/Revit_Export_Natuursteen_IFC4 - scrape.ifc')

new_ifc_file = ifcopenshell.file(schema='IFC4')

project = new_ifc_file.createIfcProject(global_id=new_ifc_file.create_guid(), owner_history=None, name='Nieuw Project')

building = new_ifc_file.createIfcBuilding(global_id=new_ifc_file.create_guid(), owner_history=None, name='Nieuw Gebouw', composition_type='ELEMENT', container=project)

context = new_ifc_file.createIfcGeometricRepresentationContext(context_identifier='Context3D', context_type='Model', coordinate_space_dimension=3)