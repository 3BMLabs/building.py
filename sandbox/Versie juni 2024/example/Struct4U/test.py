from objects.frame import *
from exchange.struct4U import *
from project.fileformat import *

proj = BuildingPy("WHSD","2321")

filepath = "C:/Users/mikev/3BM/3BM - 3BM Sharepoint/50_projecten/3_3BM_bouwtechniek/2321 Plan WHSD-locatie Oude-Tonge/71_constructie_advies/2321-5.3 Constructie bedrijfshal V3.xml"

tree = ET.parse(filepath)
root = tree.getroot()

#convert .xml to buildingpy objects.
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
    profile_name = profile_name.split()[0]
    if profile_name == None:
        print(f"No profile name '{profile_name}' found.")
    else:
        start = XYZ[1][XYZ[0].index(i.text)]
        end = XYZ[1][XYZ[0].index(j.text)]
        try:
            pf = Frame.by_startpoint_endpoint_profile_shapevector(start, end, profile_name, profile_name + "-" + l.text, Vector2(0,0), float(m.text), BaseSteel, None)
            if pf != None:
                obj.append(pf)
        except Exception as e:
            print(f"Could not translate '{profile_name}'.")
print(f"Generated BuildingPy Objects.")

for i in obj:
    proj.objects.append(i)

proj.toIFC("2321")
#proj.toSpeckle("e017f22fff")
