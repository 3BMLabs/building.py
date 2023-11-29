#pip install PyQt6
#append output name and desire name, paste that on Desktop page and open in dir.

import sys, os
import json
import specklepy
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton



# from objects.frame import *
# from exchange.scia import *
# from exchange.struct4U import *

# from objects.analytical import *
# from project.fileformat import BuildingPy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scia2Struct4U converter")
        button = QPushButton("Select XML File")
        button.clicked.connect(self.select_xml_file)
        self.setCentralWidget(button)

    def select_xml_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select XML File", filter="XML Files (*.xml)")
        if filename:
            print("Selected XML file:", filename)

            # filepath = f"{os.getcwd()}\\temp\\Scia\\Examples buildingpy\\_2.xml"
            # project = BuildingPy("TempCommit", "0")
            # LoadXML(filepath, project)

            # project.toSpeckle("c6e11e74cb")
            # xmlS4U = xmlXFEM4U() # Create XML object with standard values
            # xmlS4U.addBeamsPlates(project.objects) #Add Beams, Profiles, Plates, Beamgroups, Nodes
            # xmlS4U.addProject("Parametric Industrial Hall")
            # xmlS4U.addPanels() #add Load Panels
            # xmlS4U.addGrids() # Grids
            # xmlS4U.addSurfaceLoad()
            # xmlS4U.addLoadCasesCombinations()
            # xmlS4U.XML()
            # XMLString = xmlS4U.xmlstr

            # filepath = "C:/Users/Jonathan/Desktop/test.xml"
            # file = open(filepath, "w")
            # a = file.write(XMLString)
            # file.close()
        else:
            print("No XML file selected")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()