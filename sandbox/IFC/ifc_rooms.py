import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.shape

model = ifcopenshell.open('C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/SingleRoom.ifc')

rooms = model.by_type("IfcSpace")
print(rooms)

