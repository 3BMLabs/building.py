import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *

filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\2.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

# tmp = []

for j in project.objects:
    
    if j.type == "Frame":
        print(j.comments.id, j.profile_data.shape_name)
    #     print(j.profile_data.shape_name)
        # if j.comments.centerbottom != None:
        #     project.objects.append(j.comments.centerbottom)

# project.toSpeckle("c6e11e74cb")