import sys, os
from pathlib import Path



from construction.beam import *
from exchange.scia import *

from construction.analytical import *

filepath = f"{os.getcwd()}\\sandbox\\Scia\\Projects\\Scia_Construction_1.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

project.to_speckle("c6e11e74cb")