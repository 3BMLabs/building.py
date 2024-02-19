import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *

filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\2.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

# for j in project.objects:
#     if j.type == "Frame":
#         print(j.profile_data.profile_data.synonyms)

project.toSpeckle("c6e11e74cb")