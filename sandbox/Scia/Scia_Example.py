import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from objects.analytical import *

filepath = f"{os.getcwd()}\\sandbox\\Scia\\Projects\\Scia_Construction_1.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

project.toSpeckle("c6e11e74cb")