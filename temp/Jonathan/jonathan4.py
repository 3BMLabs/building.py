import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path
# https://help.xtools.pro/pro/22.0/en/XTools_Pro_Components/Geometry_Tools/Split_Polygons.htm

sys.path.append(str(Path(__file__).resolve().parents[2]))


from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import *
from abstract.vector import Vector3
from abstract.intersect2d import *
from abstract.plane import Plane
from abstract.text import Text
from abstract.intersect2d import Intersect2d
from objects.datum import *
from geometry.solid import Extrusion


#finish
# l1 = Line(start=Point(230,-1000,0), end=Point(45,1000,0))
# l2 = Line(start=Point(-1000,0,0), end=Point(1230,0,0))
# f1 = Intersect2d().getLineIntersect(l1, l2)
# obj = [l1, l2, f1]


Point1 = Point(1500,-4030,0)
Point2 = Point(6900,5000,0)
Point3 = Point(0,10000,0)
Point4 = Point(0,0,0)
Point5 = Point(-2900,1600,0)
ply1 = PolyCurve.byPoints([Point1, Point2, Point3, Point4, Point5, Point1])
z = Extrusion.byPolyCurveHeight(ply1, 1000, 200)






l3 = Line(start=Point(300, -1500, 0), end=Point(1730, 1520, 0))


startLinexAxis = Line(start=Point(10000,-10000,0), end=Point(-10000,-10000,0))
startLineyAxis = Line(start=Point(-10000,-10000,0), end=Point(-10000,10000,0))


part2 = PolyCurve.byPoints([Point(400.0,9710.144927536232,0), Point(0,10000,0), Point(0,0,0), Point(-2900,1600,0), Point(400.0,-2622.5,0), Point(400.0,9710.144927536232,0)])


obj = []

# obj = [ply1]
# obj = [part2]

gridLines = []
# sys.exit()
for xRange in range(50):
    vector1 = Vector3(0, 600*(xRange+1), 0)
    vector2 = Vector3(600*(xRange+1), 0, 0)
    gridLines.append(Line.offset(startLinexAxis, vector1))
    gridLines.append(Line.offset(startLineyAxis, vector2))

Intersctline  = Line(start=Point(5000,200,0), end=Point(-10000,200,0))
# Intersctline1 = Line(start=Point(200,10000,0), end=Point(200,-1000,0))
Intersctline2 = Line(start=Point(400,-4000,0), end=Point(400,12000,0))
lns = [Intersctline, Intersctline2]


insect = Intersect2d().getIntersectLinePolyCurve(ply1, Intersctline2, split=True, stretch=False) #stretch
# print(insect)
# print(ply1.curves)
# for z in ply1.curves:
    # print(z)

part1 = []
part2 = []

st = insect["InnerGridLines"][0].start #Point(400.0,9710.144927536232,0)
en = insect["InnerGridLines"][0].end #Point(400.0,-2622.5,0)

lenList = len(ply1.curves)-1
i1 = None
i2 = None

for index, i in enumerate(ply1.curves):
    print(is_point_on_line_segment(en, i))
    if is_point_on_line_segment(st, i) == True:
        i1 = index
    if is_point_on_line_segment(en, i) == True:
        i2 = index

list1 = list(range(1, i2+1))

# Generate list2 and update values
list2 = list(range(i1+i2, lenList+i1+i2))
min_val = min(list1)
list2 = [x-min_val for x in list2]


print(list1)
print(list2)


part1.append(st)
for n1 in range(i1, i2):
    seg = ply1.curves[n1].start
    part1.append(seg)
part1.append(en)
part1.append(st)

part2.append(st)
for n1 in range(i1, i2):
    seg = ply1.curves[n1].start
    part1.append(seg)
part1.append(en)
part1.append(st)



for i in part2:
    print(i)

obj.append(PolyCurve.byPoints(part1))


# print(i1, i2)
    # if is_point_on_line_segment(st, i) == True: #start
    #     draw = Line.split(i, [st])
    #     for ix, lne in enumerate(draw):
    #         if ix == 0:
    #             part2.append(lne)
        # draw = Line.split(i, [st])
        # for lne in draw:
        #     if lne.start == st:
        #         checkthisC == lne.end
        #     elif lne.end == st:
        #         checkthisC = lne.start
            
                # print(lne)
            # print(lne.start)
            # print(lne.end)
            # obj.append(lne)

    # if is_point_on_line_segment(en, i) == True: #end
    #     draw = Line.split(i, [en])
    #     for lne in draw:
    #         obj.append(lne)

for x in part2:
    # print(x)
    obj.append(x)


for pt in insect["IntersectGridPoints"]:
    obj.append(pt)



# for pt in insect["InnerGridLines"]:
#     obj.append(pt)

# sys.exit()


# for grid in gridLines: #shows grid lines
#     obj.append(grid)
# obj.append(startLinexAxis)
# obj.append(startLineyAxis)


# sys.exit()


SpeckleHost = "3bm.exchange"
StreamID = "fa4e56aed4"
SpeckleObjects = obj
Message = "x"
SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)