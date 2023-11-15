import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from objects.frame import *
from exchange.scia import *

from exchange.struct4U import *

from objects.analytical import *
from project.fileformat import BuildingPy


filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\scia_temp.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

project.toSpeckle("c6e11e74cb")