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

tree = ET.parse("C:/TEMP/export.xml")
#tree = ET.parse("C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Struct4U/Example Projects/Industrial steel structure 2/export.xml")
#tree = ET.parse("C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Struct4U/Example Projects/Industrial steel structure 1/export.xml")
root = tree.getroot()

#TODO: Lines and Grids units
#TODO: Beams in node
#TODO: Materialcolor
#TODO: Concrete Profiles

#LoadGrid and create in Speckle
Grids = XMLImportGrids(tree,1000)
XYZ = XMLImportNodes(tree)
obj = XMLImportPlates(tree)

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#print(BeamsFrom)
#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileNumber = root.findall(".//Profiles/Material_type")
ProfileName = root.findall(".//Profiles/Profile_name")

#sys.exit()

beams = []
for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
    profile_name = ProfileName[int(k.text)-1].text
    if profile_name == None:
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

Commit = TransportToSpeckle("struct4u.xyz", "6166d4a8b6", SpeckleObj, "Export from XFEM4U")
