from exchange.speckle import *
import json
import sys

# jsonFile = "C:/Users/JoasHollander/Downloads/rotterdam.city.json"
# jsonFile = "C:/Users/JoasHollander/Downloads/twobuildings.city.json"
# jsonFile = "C:/Users/mikev/3BM Dropbox/Maarten Vroegindeweij/Maarten en Jonathan 3BM/CityJSON/Roffa.json"
jsonFile = "C:/TEMP/mont.json"


data = json.load(open(jsonFile))
vert = data['vertices']
cityobj = data['CityObjects']

lst = []
vert_lst = []
vert_lst_new = []
faceslistnew = []


def diff(li1, li2):
    temp3 = []
    for element in li1:
        if element not in li2:
            temp3.append(element)
    return temp3


def renumber(lst):
    temp = sorted(set(lst))
    return [temp.index(i) for i in lst]


def renumberMesh(verts, faces):
    lst1 = renumber(verts)  # new verts nunmbers
    lst0 = diff(faces, verts)  # list with number of verts in face
    lst2 = []
    for i in range(0, len(lst0), 2):
        n = lst0[i]
        lst2.append(n)
        lst2.extend(lst1[:n])
        lst1 = lst1[n:]
        if i + 1 < len(lst0):
            n = lst0[i + 1]
            lst2.append(n)
            lst2.extend(lst1[:n])
            lst1 = lst1[n:]
    return lst2


for a in vert:
    for b in a:
        vert_lst.append(b)

# print(vert)

index = 0
maximum = 40000
for i in cityobj:
    faces_lst = []  # sublijst met faces per gebouw
    vertsindices = [] # lijst met alle hoekpunten van de meshed in de juiste volgorde zonder het aantal ervoor genoemd.
    verts_lst = []  # sublijst hoekpunten weggeschreven per gebouw
    verts_lst_uniq = []  # sublijst met alle unieke hoekpunten per gebouw

    if "geometry" in cityobj[i]:
        if len(cityobj[i]["geometry"][0]["boundaries"]) < 2:
            # print("<2")
            for count, value in enumerate(cityobj[i]["geometry"][0]["boundaries"][0]):
                for c in value:
                    for d in c:
                        verts_lst.append(d)  # alle indices van hoekpunten achter elkaar zonder het aantal er tussen.
                        print(d)
            for count, value in enumerate(cityobj[i]["geometry"][0]["boundaries"][0]):
                for c in value:
                    # print("length: ", len(c))
                    faces_lst.append(len(c))  # aantal hoekpunten wegschrijven per face
                    for d in c:
                        faces_lst.append(d)  # indices van hoekpunten achter elkaar wegschrijven hernummerd vanaf 0.
                        verts_lst.append(d)  # alle indices van hoekpunten achter elkaar, ...
                        # ... zonder het aantal er tussen hernummerd vanaf 0.
        else:
            # print("not <2")
            for count, value in enumerate(cityobj[i]["geometry"][0]["boundaries"]):
                # dit is 1 mesh
                renumberedList = []
                for c in value:
                    for d in c:
                        verts_lst.append(d)
                        # print(d)
            for count, coords in enumerate(cityobj[i]["geometry"][0]["boundaries"]):
                for coord in coords:
                    # print("length: ", len(coord))
                    faces_lst.append(len(coord))
                    for coordindex in coord:
                        faces_lst.append(coordindex)
                        verts_lst.append(coordindex)
                        vertsindices.append(coordindex)
                        # print(coordindex)

    # verts_lst zijn de indices van de hoekpunten uit de desbetreffende mesh
    # print(verts_lst)
    verts_lst_uniq = set(verts_lst)
    vert_lst_uniq_new = []
    for vert_lst_uniq in verts_lst_uniq:
        vert_lst_uniq_new.append(vert_lst_uniq)
    vert_lst_uniq_new.sort()

    # print(vert_lst_uniq_new)
    vertscoord = []
    for i in vert_lst_uniq_new:
        vertscoord.append(vert[i][0])
        vertscoord.append(vert[i][1])
        vertscoord.append(vert[i][2])
    # nu heb ik hier de XYZ-coordinaten

    # faces_lst_new = []
    faces_lst_new = renumberMesh(verts_lst,faces_lst)

    faceslistnew.append(faces_lst_new)  # list met faces per gebouw wordt in een overall list weggeschreven.
    vert_lst_new.append(vertscoord)  # list met hoekpunten per gebouw wordt in een overall list weggeschreven.

    index = index + 1
    if index == maximum:
        break


def SpeckleMeshByMesh(verts, faces):
    spcklmesh = SpeckleMesh(vertices=verts, faces=faces, name="Joas", units="mm")
    return spcklmesh


obj = []

for i, j in zip(faceslistnew, vert_lst_new):
    obj.append(SpeckleMeshByMesh(j, i))

print(vert_lst_new[3])
print(faceslistnew[3])

# sys.exit()

SpeckleHost = "speckle.xyz"  # struct4u.xyz
StreamID = "bd36f755cd"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)
