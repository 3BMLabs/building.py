import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.IFC import *

filepath = f"C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/B60_B_TVA_rooms.ifczip"

project = BuildingPy("Tmp", "1")

model = LoadIFC(filepath, project, ["IfcSpace"])

print(project.objects)

project.toSpeckle("c6e11e74cb")