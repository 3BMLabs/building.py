from exchange.struct4U import *
from exchange.speckle import *
from abstract.plane import *
from objects.panel import *
from objects.frame import *
import xml.etree.ElementTree as ET
from library.material import *
import sys

#file = Path(__file__).resolve()
#package_root_directory = file.parents[0]
#sys.path.append(str(package_root_directory))

#tree = ET.parse("C:/TEMP/export.xml")
#tree = ET.parse("C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Struct4U/Example Projects/Industrial steel structure 2/export.xml")
#tree = ET.parse("C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Struct4U/Example Projects/Industrial steel structure 1/export.xml")
tree = ET.parse("C:/Users/mikev/Documents/GitHub/Struct4U/Industrial Steel Structure/Industrial Steel Structure.xml")

root = tree.getroot()

#TODO: Beams in node
#TODO: Materialcolor
#TODO: Concrete Profiles

obj = []
#LoadGrid and create in Speckle
XYZ = XMLImportNodes(tree)

#obj = obj + XMLImportGrids(tree, 1000)

#obj.append(XMLImportPlates(tree))

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")
BeamsLayer = root.findall(".//Beams/Layer")

#print(BeamsFrom)
#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")

ExcludeLayer = "25"
#BEAMS

beams = []
for i, j, k, l, m in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber, BeamsLayer):
    profile_name = ProfileName[int(k.text)-1].text
    profile_name = profile_name.split()[0]
    if profile_name == None:
        pass
    else:
        if m == ExcludeLayer:
            pass
        else:
            start = XYZ[1][XYZ[0].index(i.text)]
            end = XYZ[1][XYZ[0].index(j.text)]
            try:
                obj.append(Frame.byStartpointEndpointProfileName(start, end, profile_name, profile_name + "-" + l.text, BaseSteel))
            except:
                pass
                print("could not translate " + profile_name)

SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle("struct4u.xyz", "a63404e44e", SpeckleObj, "Export from XFEM4U")
