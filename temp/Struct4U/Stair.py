from exchange.speckle import *
from objects.panel import *
from objects.frame import *
from objects.datum import *
from exchange.struct4U import *
from abstract.vector import *
from abstract.coordinatesystem import *

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

Height = 3000
Radius = 1200
NumberOfTreads = 16
DegreesSpiral = 270
Column = "K150/150/10"
Tread = "S120/10"
obj = []

obj.append(Frame.byStartpointEndpointProfileName(Point(0,0,0),Point(0,0,Height),Column,"spiral",BaseSteel)) #Spiral

deg = 0
x = 0
y = Radius
dz = Height / NumberOfTreads
z = dz
p2 = Point(x, y, z)
ddeg = DegreesSpiral / NumberOfTreads

for i in range(NumberOfTreads):
    obj.append(Frame.byStartpointEndpointProfileNameJustifiction(Point(0, 0, z), p2, Tread, "Tread","Center","Center",90,BaseSteel))  # Treads
    p2 = Point.rotateXY(p2, ddeg, dz)
    z = z + dz


SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "4bb051dcbb", SpeckleObj, "Parametric Spiral Staircase.py")

#ExportXML
Frame1 = "<Frame>"
Project = "<ProjectName>" + "Building.py Industrial Hall" + "</ProjectName>"
ProjectNumber = "<ProjectNumber/>"
ExportDate = "<ExportDateTime>2023-02-17 22:02:38Z</ExportDateTime>"
XMLVersion = "<XMLExportVersion>v4.0.30319</XMLExportVersion>"
Nodes = "<Nodes></Nodes>"
Supports = "<Supports></Supports>"
Grids = "<Grids></Grids>"
Profiles = "<Profiles></Profiles>"
Beamgroup = "<Beamgroup></Beamgroup>"
Beams = "<Beams></Beams>"
Plates = "<Plates></Plates>"
RebarLongitudinal = "<RebarLongitudinal></RebarLongitudinal>"
RebarStirrup = "<RebarStirrup></RebarStirrup>"
Layers = "<Layers><Layer_number>1</Layer_number><Layer_description>Layer 1</Layer_description></Layers>"
Frame2 = "</Frame>"


#Number of nodes:
n = 0
Nodes = []
Plates = []
Beams = []
Beamgroup = []
Profiles = []
plateN = 0 # Numbering plates
beamsN = 0 # Numbering beams
beamsGN = 0 #Numbering beamgroup
profN = 0 # Numbering profiles
Nodes.append("<Nodes>")
Plates.append("<Plates>")
Beams.append("<Beams>")
Beamgroup.append("<Beamgroup>")

Profiles.append("<Profiles>")

ProfileNames = [] # all profiles
for i in obj:
    nm = i.__class__.__name__
    if nm == "Frame":
        ProfileNames.append(i.profileName)

ProfileNamesUnique = [] #Unique profiles
for item in ProfileNames:
    if item not in ProfileNamesUnique:
        ProfileNamesUnique.append(item)

for i in ProfileNamesUnique:
    profN = profN + 1
    Profiles.append("<Number>" + str(profN) + "</Number>")
    Profiles.append("<Profile_name>" + i + "</Profile_name>")
    Profiles.append("<Material_type>" + "0" + "</Material_type>")
    Profiles.append("<Material>" + "S235" + "</Material>")
    #if i.material.name == "BaseSteel":
    #    Profiles.append("<Material_type>" + "0" + "</Material_type>")
    #    Profiles.append("<Material>" + "S235" + "</Material>")
    #else:
    #    Profiles.append("<Material_type>" + "0" + "</Material_type>")
    #    Profiles.append("<Material>" + "S235" + "</Material>")
    Profiles.append("<Angle>" + "0" + "</Angle>")

for i in obj:
    nm = i.__class__.__name__
    if nm == 'Panel':
        plateN = plateN + 1
        Plates.append("<Number>" + str(plateN) + "</Number>")
        for j in i.origincurve.points:
            n = n + 1
            Nodes.append("<Number>" + str(n) + "</Number>")
            Nodes.append("<X>" + str(j.x) + "</X>")
            Nodes.append("<Y>" + str(j.y) + "</Y>")
            Nodes.append("<Z>" + str(j.z) + "</Z>")
            Plates.append("<Node>" + str(n) + "</Node>")
        Plates.append("<h>" + str(i.thickness) + "</h>")
        Plates.append("<Material_type>" + "c9a5876f475cefab7cc11281b017914a1" + "</Material_type>") #material nog uitlezen
        Plates.append("<Material>" + "C20/25" + "</Material>") #material nog uitlezen
        Plates.append("<Z>" + "0" + "</Z>")
        Plates.append("<Top_Center_Bottom>" + "Center" + "</Top_Center_Bottom>")

    elif nm == 'Frame':
        ProfN = ProfileNamesUnique.index(i.profileName) + 1
        beamsGN = beamsGN + 1
        Beamgroup.append("<Number>" + str(beamsGN) + "</Number>")

        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(round(i.start.x)) + "</X>")
        Nodes.append("<Y>" + str(round(i.start.y)) + "</Y>")
        Nodes.append("<Z>" + str(round(i.start.z)) + "</Z>")
        Beamgroup.append("<Startnode>" + str(n) + "</Startnode>")

        beamsN = beamsN + 1
        Beams.append("<Number>" + str(beamsN) + "</Number>")
        Beams.append("<Beamgroupnumber>" + str(beamsGN) + "</Beamgroupnumber>")
        Beams.append("<From_node_number>" + str(n) + "</From_node_number>")

        n = n + 1
        Nodes.append("<Number>" + str(n) + "</Number>")
        Nodes.append("<X>" + str(round(i.end.x)) + "</X>")
        Nodes.append("<Y>" + str(round(i.end.y)) + "</Y>")
        Nodes.append("<Z>" + str(round(i.end.z)) + "</Z>")

        Beamgroup.append("<Endnode>" + str(n) + "</Endnode>")

        Beams.append("<To_node_number>" + str(n) + "</To_node_number>")
        Beams.append("<Angle>" + str(i.rotation) + "</Angle>")
        Beams.append("<Angle_profile>" + "0" + "</Angle_profile>")
        ProfNstr = str(ProfN)
        Beams.append("<Profile_number>" + ProfNstr + "</Profile_number>")
        Beams.append("<Z>" + str(i.ZOffset) + "</Z>")
        Beams.append("<Top_Center_Bottom>" + i.YJustification + "</Top_Center_Bottom>")
    elif nm == 'Grid':
        message = 'Hello'

Nodes.append("</Nodes>")
Plates.append("</Plates>")
Beams.append("</Beams>")
Profiles.append("</Profiles>")
Beamgroup.append("</Beamgroup>")

Nodes = ''.join(str(N) for N in Nodes)
Plates = ''.join(str(P) for P in Plates)
Beams = ''.join(str(B) for B in Beams)
Beamgroup = ''.join(str(BP) for BP in Beamgroup)
Profiles = ''.join(str(Pr) for Pr in Profiles)

XMLString = Frame1 + Project + ProjectNumber + ExportDate + XMLVersion + Nodes + Supports + Grids + Profiles + Beamgroup + Beams + Plates + RebarLongitudinal + RebarStirrup + Layers + Frame2

filepath = "C:/TEMP/stair.xml"
file = open(filepath, "w")
a = file.write(XMLString)

file.close()

print(XMLString)