import sys, os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from objects.frame import *
from exchange.scia import *
from exchange.struct4U import *

from objects.analytical import *
from project.fileformat import BuildingPy

filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\_2.xml"

project = BuildingPy("TempCommit", "0")

LoadXML(filepath, project)

project.toSpeckle("c6e11e74cb")


xmlS4U = xmlXFEM4U() # Create XML object with standard values
xmlS4U.addBeamsPlates(project.objects) #Add Beams, Profiles, Plates, Beamgroups, Nodes
xmlS4U.addProject("Parametric Industrial Hall")
xmlS4U.addPanels() #add Load Panels
xmlS4U.addGrids() # Grids
xmlS4U.addSurfaceLoad()
xmlS4U.addLoadCasesCombinations()
xmlS4U.XML()
XMLString = xmlS4U.xmlstr

filepath = "C:/Users/Jonathan/Desktop/test.xml"
file = open(filepath, "w")
a = file.write(XMLString)
file.close()