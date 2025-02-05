#Preview: https://speckle.xyz/streams/d2e38baf76/commits/505b8630c6?c=%5B0.0581,-0.28286,0.32333,0.23898,0.12909,-0.03397,0,1%5D

from typing import List, Tuple
from svg.path import parse_path
import sys, math, requests, json
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.objects import Base
from specklepy.objects.geometry import Point, Line, Arc, Circle, Ellipse, SpiralType, Spiral, Polycurve, Polyline, Mesh, Vector, Plane, Interval
from abstract.text import Text


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
arcPlane = Plane(origin = Point.from_coords(200, 30, 13), normal = Vector.from_coords(0, 0, 1), xdir = Vector.from_coords(1, 0, 0), ydir = Vector.from_coords(0, 1, 0), units="mm")
arcInterval = Interval(start=0, end=1, totalChildrenCount=1)
arcObj = Arc(startPoint=Point(x=0, y=20, z=13), midPoint=Point(x=500, y=0, z=13), endPoint=Point(x=1000, y=20, z=13), plane=arcPlane, radius=20, interval=arcInterval, units="mm")
objList.append(arcObj)
#Arc - end

#Circle - start
circlePlane = Plane(origin = Point(x=350, y=35, z=13, units="mm"), normal = Vector(x=0, y=0, z=1), xdir = Vector(x=1, y=0, z=0), ydir = Vector(x=0, y=1, z=0), units="mm")
circleObj = Circle(radius=20.0, plane=circlePlane, units="mm")
objList.append(circleObj)
#Circle - end

#Ellipse - start
ellipsePlane = Plane(origin = Point(x=1, y=0, z=13, units="mm"), normal = Vector(x=0, y=1, z=0), xdir = Vector(x=1, y=0, z=0), ydir = Vector(x=0, y=1, z=0), units="mm")
ellipseObj = Ellipse(firstRadius=40.0, secondRadius=20.0, plane=ellipsePlane, units="mm")
objList.append(ellipseObj)
#Ellipse - end

#Spiral - start
spiralPlane = Plane(origin = Point(x=1, y=0, z=13, units="mm"), normal = Vector(x=0, y=1, z=0), xdir = Vector(x=1, y=0, z=0), ydir = Vector(x=0, y=1, z=0), units="mm")
p1 = Point(x=50, y=190, z=13, units="mm")
p2 = Point(x=0, y=280, z=13, units="mm")
spiralObj = Spiral(startPoint=p1, endPoint=p2, plane=spiralPlane, turns=4, pitchAxis=Vector(x=0, y=1, z=0), spiralType=SpiralType.BiquadraticParabola)
objList.append(spiralObj)
#Spiral - end

#Polycurve - start
p = 340
xp = 185
p1 = Point(x=50+p, y=0+xp, z=13, units="mm")
p2 = Point(x=0+p, y=0+xp, z=13, units="mm")
arcPlane = Plane(origin = Point.from_coords(0+p, 0+xp, 13), normal = Vector.from_coords(1, 0, 0), xdir = Vector.from_coords(0, 1, 0), ydir = Vector.from_coords(0, 1, 0), units="mm")
arcInterval = Interval(start=0, end=1, totalChildrenCount=1)
arcObj = Arc(startPoint=p1, midPoint=Point(x=250+p, y=40+xp, z=13), endPoint=p2, plane=arcPlane, radius=20, interval=arcInterval, units="mm")
segmentObjs = [p1, arcObj, p2]
polycurveObj = Polycurve(segments=segmentObjs)
objList.append(polycurveObj)
#Polycurve - end

#Polyline - start
coordZ = 13
polylineObj = Polyline.from_points([Point(x=175, y=175, z=coordZ, units="mm"), Point(x=225, y=175, z=coordZ, units="mm"), Point(x=225, y=200, z=coordZ, units="mm"), Point(x=175, y=200, z=coordZ, units="mm"), Point(x=175, y=175, z=coordZ, units="mm")])
objList.append(polylineObj)
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
def Platform(height, xyz, btmShape=None, text=None, txyz=None):
    x, y, z = xyz
    
    if btmShape == "btmShape":
        btmShape = [20+x,0+y,0+z,80+x,0+y,0+z,100+x,20+y,0+z,100+x,80+y,0+z,80+x,100+y,0+z,20+x,100+y,0+z,0+x,80+y,0+z,0+x,20+y,0+z,20+x,0+y,0+z]
    elif btmShape == "OveralShape":
        btmShape = [-50,-50,0, 600, -50, 0, 600, 300, 0, -50, 300, 0, -50, -50, 0]
    elif btmShape == "Example0":
        btmShape = [0+x,0+y,0+z, 0+x,35+y,0+z, 35+x,35+y,0+z, 35+x,0+y,0+z, 0+x,0+y,0+z]
    elif btmShape == "Example1":
        btmShape = [0+x,0+y,0+z, 50+x,0+y,0+z, 50+x,5+y,0+z, 27+x,5+y,0+z, 27+x,35+y,0+z, 50+x,35+y,0+z, 50+x,40+y,0+z, 0+x,40+y,0+z, 0+x,35+y,0+z, 23+x,35+y,0+z, 23+x,5+y,0+z, 0+x,5+y,0+z, 0+x,0+y,0+z]

    if text != None and txyz != None:
        tx, ty, tz = txyz
        t = Text(text=text, font_family="arial", bounding_box=False, xyz=[-tx, -ty, 15], rotation=0, scale=0.007).write()

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
    if text != None:
        return meshPlatform, t
    else:
        return meshPlatform


MeshExample0 = Platform(5, [481,160,13], btmShape="Example0")
objList.append(MeshExample0)

MeshExample1 = Platform(5, [475,10,13], btmShape="Example1")
objList.append(MeshExample1)

MeshBase0 = Platform(10, [0,0,0], btmShape="OveralShape")
objList.append(MeshBase0)

MeshBase1 = Platform(2, [0,0,10], btmShape="btmShape", text="LINE", txyz=[0+20,0+50,10])
objList.append(MeshBase1)

MeshBase2 = Platform(2, [150,0,10], btmShape="btmShape", text="ARC", txyz=[150+18,0+50,10])
objList.append(MeshBase2)

MeshBase3 = Platform(2, [150,150,10], btmShape="btmShape", text="POLYLINE", txyz=[150+0,150+50,10])
objList.append(MeshBase3)

MeshBase4 = Platform(2, [0,150,10], btmShape="btmShape", text="POINT", txyz=[0+15,150+50,10])
objList.append(MeshBase4)

MeshBase5 = Platform(2, [300,0,10], btmShape="btmShape", text="CIRCLE", txyz=[300+10,0+50,10])
objList.append(MeshBase5)

MeshBase6 = Platform(2, [300,150,10], btmShape="btmShape", text="POLYCURVE", txyz=[290,150+50,10])
objList.append(MeshBase6)

MeshBase7 = Platform(2, [450,0,10], btmShape="btmShape", text="MESH2", txyz=[450+10,0+50,10])
objList.append(MeshBase7)

MeshBase8 = Platform(2, [450,150,10], btmShape="btmShape", text="MESH1", txyz=[450+10,150+50,10])
objList.append(MeshBase8)
#Platform - end


send_to_speckle(host="https://3bm.exchange", stream_id="fa4e56aed4", objects=objList, msg="Objects")