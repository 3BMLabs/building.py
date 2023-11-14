import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.append(str(Path(__file__).resolve().parents[2]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2d import *
from abstract.plane import Plane
from abstract.text import Text
from abstract.intersect2d import Intersect2d
from objects.datum import *
from geometry.solid import Extrusion
from objects.panel import Panel
from abstract.color import Color
from geometry.surface import Surface
from packages.helper import *
from objects.frame import *
from objects.analytical import *

path = "C:\\Users\\Jonathan\\Desktop\\TEMP\\_3.xml"
scale = 1000
objExporter = []

tree = ET.parse(path)
root = tree.getroot()

def getAllKnoop(root):
    tableName = "EP_DSG_Elements.EP_StructNode.1"
    for container in root:
        for table in container:
            if table.attrib["t"] == tableName:
                for obj in table:
                    if obj.tag == "{http://www.scia.cz}h":
                        for header in obj:
                            print(header.attrib["t"])
                    else:
                        print(obj.attrib["nm"])


# getAllKnoop(root)

def findKnoop(name):
    tableName = "EP_DSG_Elements.EP_StructNode.1"
    for container in root:
        for table in container:
            if table.attrib["t"] == tableName:
                for obj in table.iter("{http://www.scia.cz}obj"):
                    if obj.attrib["nm"] == name:
                        x, y, z = float(obj[1].attrib["v"])*scale, float(obj[2].attrib["v"])*scale, float(obj[3].attrib["v"])*scale
                        return Point(x,y,z)
                        # return x, y, z

# findKnoop("K2")

# searchKnoop("K3054")

# import xml.etree.ElementTree as ET

# def get_coordinates(xml_data, name):
#     # Maak een ElementTree-object van de XML-data
#     tree = ET.fromstring(xml_data)

#     # Vind het object met de gegeven naam
#     object = tree.find(".//obj[@nm='{}']".format(name))

#     # Haal de waarden uit de p-knooppunten
#     values = [float(x.text) for x in object.findall("p")]

#     return values


# # Lees de XML-data in
# xml_data = open("path.xml", "r").read()

# # Haal de coordinaten van K2 op
# coordinates = get_coordinates(xml_data, "K2")

# # Print de coordinaten
# print(coordinates)

unrecognizedElements = []

def getStaaf(root):
    tableName = "EP_DSG_Elements.EP_Beam.1"
    h0 = "Naam"
    h1 = "Laag"
    h2 = "Loodrecht uitlijning"
    h3 = "LCS-rotatie"
    h4 = "Beginknoop"
    h4Index = None

    h5 = "Eindknoop"
    h5Index = None

    h6 = "Doorsnede"
    h6Index = None

    h7 = "EEM-type"
    h8 = "Staafsysteemlijn op"
    h9 = "ey"
    h10= "ez"
    h11 = "Tabel van geometrie"

    #filters
    #remove the Laag contains
    removeLayers = ["dummy"]

    for container in root:
        for table in container:
            if table.attrib["t"] == tableName:
                for obj in table:
                    if obj.tag == "{http://www.scia.cz}h":
                        for index, header in enumerate(obj):
                            if header.attrib["t"] == h4:
                                h4Index = index
                            elif header.attrib["t"] == h5:
                                h5Index = index
                            elif header.attrib["t"] == h6:
                                h6Index = index
                    else:
                        p1 = findKnoop(obj[h4Index].attrib["n"])
                        p2 = findKnoop(obj[h5Index].attrib["n"])
                        lineSeg = Line(start=p1, end=p2)
                        
                        elementType = (obj[h6Index].attrib["n"])#.split("-")[1].strip() #try to get those elements from the lib maarten did write earlier.
                        for removeLayer in removeLayers:
                            # print(elementType.lower(), removeLayer.lower())
                            if removeLayer.lower() in elementType.lower():
                                print(f"[removeLayers]: {elementType}")
                            else:

                                elementType = elementType.split("-")[1].strip()

                                objExporter.append(lineSeg)
                                # objExporter.append(Support.pinned(p1))
                                # objExporter.append(Support.pinned(p2))
                                # objExporter.append(Frame.byStartpointEndpointProfileNameShapevector(p1, p2, elementType, elementType, Vector2(x=0,y=12), 0, BaseSteel))
                                # objExporter.append(Frame.byStartpointEndpointProfileNameShapevector(p1, p2, "HE100A", "Frame 4", Vector2(0,0), 20, BaseSteel))

                                try:
                                    # elementType = elementType.replace("SHS", "K") #temp
                                    # Frame.byStartpointEndpointProfileNameShapevector(cls, start: Point, end: Point, profile_name: str, name: str, vector2d: Vector2, rotation: float, material = None):
                                    # objExporter.append(Frame.byStartpointEndpointProfileNameShapevector(p1, p2, elementType, elementType, Vector2(x=0,y=0), 0, BaseSteel))
                                    objExporter.append(Frame.byStartpointEndpointProfileNameShapevector(p1, p2, elementType, elementType, Vector2(0,0), 0, BaseSteel))

                                    # objExporter.append(Frame.byStartpointEndpointProfileName(p1,p2,elementType,elementType,BaseSteel))
                                    # objExporter.append(Frame.byStartpointEndpointProfileName(p1,p2,"HEA400","HEA400",BaseSteel))
                                except Exception as e:
                                    if elementType not in unrecognizedElements:
                                        unrecognizedElements.append(elementType)
                                    # print(e)

getStaaf(root)
print(unrecognizedElements)
# print()
# sys.exit()
# for container in root:
#     for table in container:
#         print(table.attrib["t"])

#knopen: "EP_DSG_Elements.EP_StructNode.1";
#staaf: "EP_DSG_Elements.EP_Beam.1";
#materialen: "CrossSection.EP_CssGeometry.1";
#

# Print de naam van het project
# for project in root.findall("project"):
#   print(project.attrib["name"])
  
# Print de namen van alle lagen
# for layer in root.findall("container"):
#     print(layer.attrib["nm"])

# Print de ID en naam van alle objecten in de laag "Lagen"
# for obj in root.find("container")[1].findall("obj"):
#     print(obj.attrib["id"], obj.attrib["nm"])

# sys.exit()

SpeckleHost = "speckle.xyz"
StreamID = "c6e11e74cb"
SpeckleObjects = objExporter
Message = "Elements"
SpeckleObj = translateObjectsToSpeckleObjects(objExporter)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)