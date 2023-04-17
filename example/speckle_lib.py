#Point
#SpeckleLine
#SpeckleArc
#Polyline
#SpeckleMesh
#Vector (cannot be visualised)
#Plane
#SpeckleInterval

#Section 1:
# -> Create plane / platform
# -> import text, check if text has converter ose
# -> text by each specklepy object.
# -> send to speckleserver (default method)
# -> consequent variable names / clean space after comma
# -> show everything in the right scale

import sys
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.objects import Base
from specklepy.objects.geometry import Point, Line, Arc, Polyline, Mesh, Vector, Plane, Interval


def flatten(nested_list):
    flattened_list = []
    for sublist in nested_list:
        flattened_list.extend(sublist)
    return flattened_list


def send_to_speckle(host, stream_id, objects, msg=None):
    account = get_default_account()
    client = SpeckleClient(host=host)
    client.authenticate_with_account(account)
    transport = ServerTransport(client=client, stream_id=stream_id)
    class SpeckleExport(Base):
        objects = None
    obj = SpeckleExport(objects=objects)
    hash = operations.send(base=obj, transports=[transport])
    commit_id = client.commit.create(stream_id = stream_id, object_id = hash, message = msg)
    print(f"Export ID: {commit_id}")


objList = []

#Vector - start, note: cannot be visualised
vectorObj = Vector.from_coords(1, 0, 0)
#Vector - end

#Point - start
pointObj = Point(x=50, y=190, z=13, units="mm")
objList.append(pointObj)
#Point - end

#Line - start
lineObj = Line(start=Point(x=75, y=30, z=13), end=Point(x=25, y=30, z=13), units="mm")
objList.append(lineObj)
#Line - end

#Arc - start
arcPlane = Plane(origin = Point.from_coords(10, 0, 0), normal = Vector.from_coords(0, 0, 1), xdir = Vector.from_coords(1, 0, 0), ydir = Vector.from_coords(0, 1, 0), units="mm")
arcInterval = Interval(start=0, end=1, totalChildrenCount=1, units="mm")
arcObj = Arc(startPoint=Point.from_coords(0, 0, 0), midPoint=Point.from_coords(10, 0, 0), endPoint=Point.from_coords(20, 5, 0), plane=arcPlane, radius=1, interval=arcInterval, units="mm")
objList.append(arcObj)
#Arc - end

#Polyline - start
coordZ = 20
polylineObj = Polyline.from_points([Point.from_coords(0,0,coordZ), Point.from_coords(10,0,coordZ), Point.from_coords(10,10,coordZ), Point.from_coords(0,10,coordZ), Point.from_coords(0,0,coordZ)])
# objList.append(polylineObj)

#Polyline - end

#Mesh - start, note: cuboid
height = 100
bottomVertices = [0, 0, 0, 100, 0, 0, 100, 100, 0, 0, 100, 0, 0, 0, 0] #automatic close

topVertices = [v + height if i % 3 == 2 else v for i, v in enumerate(bottomVertices)]
allVertices = bottomVertices + topVertices

bottom_faces = []
i = 0
for x in range(len(bottomVertices)-1):
    if x % 3 == 2:
        bottom_faces.append(i)
        i += 1
p = bottom_faces.insert(0, len(bottom_faces))

top_faces = []
for index, i in enumerate(bottom_faces[1:]):
    if index == 0:
        top_faces.append(bottom_faces[0])
    top_faces.append(bottom_faces[0]+1 + bottom_faces[i+1])

tempList = []
faces = []

for i in range(len(bottom_faces)-1):
    between1 = bottom_faces[i+1]+1
    list1 = [4, bottom_faces[i+1], between1]
    mXtop_faces = top_faces[-1:][0]
    between2 = top_faces[i+1]+1
    if between2 > mXtop_faces:
        between2 = top_faces[1]
    list2 = [between2, top_faces[i+1]]
    tempList = list1 + list2
    faces.append(tempList)

allFaces = bottom_faces + top_faces + flatten(faces)

meshObj = Mesh(
    vertices=allVertices,
    faces=allFaces,
    units="mm"
)
#Mesh - end


#Platform - start
# length = 1000
# width = 1000
# startZ = 0
# radius = 50
# radius_segments = 30

# top_left = (radius, width - radius, startZ)
# top_right = (length - radius, width - radius, startZ)
# bottom_left = (radius, radius, startZ)
# bottom_right = (length - radius, radius, startZ)

# arc_angles = [math.pi / 2 * i / radius_segments for i in range(radius_segments + 1)]
# arc_offsets = [(radius * math.cos(angle), radius * math.sin(angle), 0) for angle in arc_angles]

# point_list = [top_left]
# point_list.extend([(top_left[0], top_left[1] - radius, 0)] + [(top_left[0] + offset[0], top_left[1] - offset[1], startZ) for offset in arc_offsets])
# point_list.append(top_right)
# point_list.extend([(top_right[0] + radius, top_right[1])] + [(top_right[0] + offset[0], top_right[1] - offset[1], startZ) for offset in arc_offsets[::-1]])
# point_list.append(bottom_right)
# point_list.extend([(bottom_right[0], bottom_right[1] + radius)] + [(bottom_right[0] - offset[0], bottom_right[1] + offset[1], startZ) for offset in arc_offsets])
# point_list.append(bottom_left)
# point_list.extend([(bottom_left[0] - radius, bottom_left[1])] + [(bottom_left[0] - offset[0], bottom_left[1] + offset[1], startZ) for offset in arc_offsets[::-1]])
# point_list.extend([(top_left[0], top_left[1] - radius, 0)] + [(top_left[0] + offset[0], top_left[1] - offset[1], startZ) for offset in arc_offsets]) #automatic enclose

# bottomVertices = [val for point in point_list for val in point]

def Platform(height, xyz, btmShape=None):
    x, y, z = xyz
    if btmShape == "btmShape":
        btmShape = [20+x,0+y,0+z,80+x,0+y,0+z,100+x,20+y,0+z,100+x,80+y,0+z,80+x,100+y,0+z,20+x,100+y,0+z,0+x,80+y,0+z,0+x,20+y,0+z,20+x,0+y,0+z]
    elif btmShape == "OveralShape":

        btmShape = [-50,-50,0, 450, -50, 0, 450, 300, 0, -50, 300, 0, -50, -50, 0]
    topVertices = [v + height if i % 3 == 2 else v for i, v in enumerate(btmShape)]
    allVertices = btmShape + topVertices

    bottom_faces = []
    i = 0
    for x in range(len(btmShape)-1):
        if x % 3 == 2:
            bottom_faces.append(i)
            i += 1
    p = bottom_faces.insert(0, len(bottom_faces))

    top_faces = []
    for index, i in enumerate(bottom_faces[1:]):
        if index == 0:
            top_faces.append(bottom_faces[0])
        top_faces.append(bottom_faces[0]+1 + bottom_faces[i+1])


    tempList = []
    side_faces = []

    for i in range(len(bottom_faces)-1):
        between1 = bottom_faces[i+1]+1
        list1 = [4, bottom_faces[i+1], between1]

        mXtop_faces = top_faces[-1:][0]
        between2 = top_faces[i+1]+1
        if between2 > mXtop_faces:
            between2 = top_faces[1]
        list2 = [between2, top_faces[i+1]]

        tempList = list1 + list2
        side_faces.append(tempList)

    allFaces = bottom_faces + top_faces + flatten(side_faces)

    meshPlatform = Mesh(
        vertices=allVertices,
        faces=allFaces,
        units="mm"
    )

    return meshPlatform

MeshBase0 = Platform(10, [0,0,0], btmShape="OveralShape")
objList.append(MeshBase0)

MeshBase1 = Platform(2, [0,0,10], btmShape="btmShape")
objList.append(MeshBase1)

MeshBase2 = Platform(2, [150,0,10], btmShape="btmShape")
objList.append(MeshBase2)

MeshBase3 = Platform(2, [150,150,10], btmShape="btmShape")
objList.append(MeshBase3)

MeshBase4 = Platform(2, [0,150,10], btmShape="btmShape")
objList.append(MeshBase4)

MeshBase5 = Platform(2, [300,0,10], btmShape="btmShape")
objList.append(MeshBase5)

MeshBase6 = Platform(2, [300,150,10], btmShape="btmShape")
objList.append(MeshBase6)

#Platform - end


send_to_speckle(host="https://3bm.exchange", stream_id="fa4e56aed4", objects=objList, msg="Objects")
