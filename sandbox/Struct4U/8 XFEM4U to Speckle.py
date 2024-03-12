from exchange.struct4U import *
from exchange.speckle import *
from objects.frame import *
import xml.etree.ElementTree as ET
from library.material import *

tree = ET.parse("C:/Users/mikev/Documents/GitHub/Struct4U/8 XFEM4U to Speckle/Industrial Steel Structure.xml")

root = tree.getroot()

#TODO: Beams in node
#TODO: Materialcolor
#TODO: Concrete Profiles

obj = []
#LoadGrid and create in Speckle
XYZ = XMLImportNodes(tree)
obj = obj + XMLImportGrids(tree, 1000)

#obj.append(XMLImportPlates(tree))

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")
BeamsLayer = root.findall(".//Beams/Layer")
BeamsRotation = root.findall(".//Beams/Angle")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")

#BEAMS
for i, j, k, l, m in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber, BeamsRotation):
    profile_name = ProfileName[int(k.text)-1].text
    #profile_name = profile_name.split()[0]
    if profile_name == None:
        print("profile_name is None")
    else:
        start = XYZ[1][XYZ[0].index(i.text)]
        end = XYZ[1][XYZ[0].index(j.text)]
        try:
            obj.append(Frame.byStartpointEndpointProfileNameShapevector(start, end, profile_name, profile_name + "-" + l.text, Vector2(0,0,0), float(m.text), BaseSteel))
        except:
            print("could not translate " + profile_name)

SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle("struct4u.xyz", "3fff8f56cc", SpeckleObj, "Industrial Steel Structure 2")
