import sys, json
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[0]
sys.path.append(str(package_root_directory))

from exchange.speckle import *

jsonFile = "temp/rotterdam.json"
data = json.load(open(jsonFile))
vert = data['vertices']
cityobj = data['CityObjects']

lst = []
vert_lst = []
faces_lst = []

for i in cityobj:
    if "geometry" in cityobj[i]:
        if len(cityobj[i]["geometry"][0]["boundaries"]) < 2:
            # print("<2")
            for count, value in enumerate(cityobj[i]["geometry"][0]["boundaries"][0]):
                for c in value:
                    # print("length: ", len(c))
                    faces_lst.append(len(c))
                    for d in c:
                        # print(d)
                        faces_lst.append(d)

        else:
            # print("not <2")
            for count, value in enumerate(cityobj[i]["geometry"][0]["boundaries"]):
                for c in value:
                    # print("length: ", len(c))
                    faces_lst.append(len(c))
                    for d in c:
                        # print(d)
                        faces_lst.append(d)

for a in vert:
    for b in a:
        vert_lst.append(b)

def SpeckleMeshByMesh(verts,faces):
    spcklmesh = SpeckleMesh(vertices = verts, faces = faces, name = "Joas", units = "mm")
    return spcklmesh

obj = []

obj.append(SpeckleMeshByMesh(vert_lst,faces_lst))

SpeckleHost = "3bm.exchange" # struct4u.xyz
StreamID = "55758e05ae" #c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 140"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)