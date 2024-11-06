import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from construction.frame import *
from exchange.IFC import *

# filepath = f"C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/B60_B_TVA_rooms.ifczip"
filepath = f"C:/Users/Jonathan/Documents/GitHub/building.py/sandbox/IFC/models/2_door.ifc"

project = BuildingPy("Tmp", "1")

model = LoadIFC(filepath, project, ["IfcDoor"])
# model = LoadIFC(filepath, project, ["IfcSpace", "IfcBuildingStorey", "IfcWall"])
# model = LoadIFC(filepath, project, ["IfcWall"])

# print(project.objects)

# project.toSpeckle("c6e11e74cb")
