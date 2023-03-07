from exchange.Struct4U import *
from exchange.speckle import *
from abstract.plane import *
from objects.panel import *
import xml.etree.ElementTree as ET

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

tree = ET.parse("C:/Users/mikev/Documents/GitHub/building.py/temp/testplates.xml")
root = tree.getroot()

def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b


#TODO: Lines and Grids units
#TODO: Beams in node
#TODO: Materialcolor
#TODO: Concrete Profiles

#LoadGrid and create in Speckle
Grids = XMLImportGrids(tree,1000)
XYZ = XMLImportNodes(tree)
Plates = XMLImportPlates(tree)

jsonFile = "C:/Users/mikev/Documents/GitHub/building.py/library/material.json"

jsonFileStr = open(jsonFile, "r").read()

with open(jsonFile) as f:
    data = json.load(f)

print(data)

class searchMaterial:
    def __init__(self, name):
        self.name = name
        self.color = []
        self.synonyms = None
        for item in data:
            for i in item.values():
                synonymList = i[0]["synonyms"]
                if self.name in synonymList:
                    self.color = i[0]["color"]

test = searchMaterial("Beton").color   #kleur van beton

color_int = rgb_to_int(test)

print(test)

sys.exit()

color = -1762845660
colrs = []
for j in range(int(len(Plates[0].extrusion.verts)/3)):
    colrs.append(color)

#sys.exit()
obj = translateObjectsToSpeckleObjects(Plates)

Commit = TransportToSpeckle("struct4u.xyz", "498714a19b", obj, "Test with Plates from XFEM4U")

sys.exit()

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")

# for i, j, k, l in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber):
#     profile_name = ProfileName[int(k.text)-1].text
#     if profile_name == None:
#         pass
#     else:
#         frame = Frame()
#         start = XYZ[int(i.text)-1]
#         end = XYZ[int(j.text)-1]
#         profile = matchprofile(profile_name)
#         try:
#             frame.byStartpointEndpointProfileName(start, end, profile, profile_name + "-" + l.text)
#         except:
#             pass
#         test = SpeckleMeshByMesh(frame)
#         obj.append(test)

