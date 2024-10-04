import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.shape
from ifcopenshell.api import run

model = ifcopenshell.open('C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/Huis.ifc')

print(model)

wall = model.by_type("ifcwall")
g = ifcopenshell.file(schema=model.schema)

projmod = model.by_type("IfcProject")[0]
wallfromModel = wall[0]

g.add(projmod)

wall_copy_class = run("root.copy_class", model, product = wall[0])

g.add(wall_copy_class)

for x in model.get_inverse(wall_copy_class):
    g.add(x)


g.write(r"C:\Users\Jonathan\Documents\utils\new.ifc")
gopen = ifcopenshell.open(r"C:\Users\Jonathan\Documents\utils\new.ifc")
gopenwall = gopen.by_type("ifcwall")[0]
gopenpsets = ifcopenshell.util.element.get_psets(gopenwall)
wallfromModelpsets = ifcopenshell.util.element.get_psets(wallfromModel)

print(model.to_string())
print(g.to_string())
print(gopen.to_string())