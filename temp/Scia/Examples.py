import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *
from project.fileformat import BuildingPy

point = Point(1.0, 2.0, 3.0)

p2 = Point(20, 3, 50)

line1 = Line(point, p2)

print(line1)
# print(point.id)
serialized_point = json.dumps(line1.serialize())

print(serialized_point)

file_name = 'project/data.json'
with open(file_name, 'w') as file:
    file.write(serialized_point)
# filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\_1.xml"

# project = BuildingPy("TempCommit", "0")

# LoadXML(filepath, project)

# project.toSpeckle("c6e11e74cb")
# project.save()