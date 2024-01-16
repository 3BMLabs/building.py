import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from objects.panel import *
from objects.frame import *
from objects.steelshape import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import profiledataToShape
from objects.annotation import *
from abstract.intersect2d import *
from geometry.systemsimple import *

project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"


Line1 = Line(start=Point(0, 0, 0), end=Point(0, 500, 0))
Line2 = Line(start=Point(0, 500, 0), end=Point(500, 500, 0))
Line3 = Line(start=Point(500, 500, 0), end=Point(100, 1000, 0))

p1 = Point(0,0,0)
p2 = Point(0,3000,0)
p3 = Point(2000,6500,0)
p4 = Point(4000,3000,0)
p5 = Point(4000,0,0)

PC1 = PolyCurve.byPoints([p1,p2,p3,p4,p5])
project.objects.append(PC1)

window1 = [Point(-500,500,0), Point(500,750,0), Point(750,750,0), Point(750,500,0)]

# PC2 = PolyCurve.byPoints(window1)

window2 = [Point(3700,6000,0), Point(500,750,0), Point(750,750,0), Point(750,500,0)]

# PC3 = PolyCurve.byPoints(window2)

Line4 = Line(start=Point(2500, -900, 0), end=Point(2500, 6000, 0))
# project.objects.append(Line4)

p1 = Point(650,2500,0)
p2 = Point(1000,3000,0)
p3 = Point(6000,6500,0)
p5 = Point(4000,2500,0)

PC4 = PolyCurve.byPoints([p1,p2,p3,p5])
# project.objects.append(PC4)


p1 = Point(0,-500,0)
p2 = Point(0,500,0)
p3 = Point(4000,500,0)
p5 = Point(4000,-500,0)

PC5 = PolyCurve.byPoints([p1,p2,p3,p5])



# project.objects.append(PC5)

# Line5 = Line(start=Point(1500, -750, 0), end=Point(1500, 1500, 0))
# project.objects.append(Line5)

# p1 = Point(1000,-500,0)
# p2 = Point(500,250,0)
# p3 = Point(750,300,0)
# p4 = Point(1000,400,0)
# p5 = Point(2000,500,0)
# p6 = Point(2500,0,0)
# p7 = Point(2000,-500,0)
# PC6 = PolyCurve.byPoints([p1,p2,p3,p4,p5,p6,p7])
# project.objects.append(PC6)



# project.objects.append(PC3)

# for j in window1:
#     project.objects.append(j)

test1 = PatternSystem().StretcherBondWithJoint("halfsteensverband",0,210,50,10,12.5)
# test2 = PatternSystem().TileBondWithJoint("tegels",400,400,0,10,10)
# test3 = PatternSystem().CrossBondWithJoint("kruisverband test",100,210,50,10,12.5)
test_res = PatternGEOM(test1,4200,600)

# for i in test_res:
#     project.objects.append(i)

l3 = Line(Point(-500,500,0), Point(4500,500,0))
l4 = Line(Point(-40,900,0), Point(4700,900,0))
# project.objects.append(l3)
# project.objects.append(l4)

l5 = Line(Point(-500,500,0), Point(4500,500,0))
l6 = Line(Point(300,1200,0), Point(1200,0,0))
# project.objects.append(l5)
# project.objects.append(l6)

intersect_calculator = Intersect2d()


# multiline_intersect = intersect_calculator.getMultiLineIntersect([l3,l4,l5,l6])
# for res_intersect in multiline_intersect:
#     print(res_intersect)
#     project.objects.append(res_intersect)


# polycurve_intersect = intersect_calculator.getIntersectLinePolyCurve(PC2, [l3,l4,l5,l6], True)
# print(polycurve_intersect)

# for pt in polycurve_intersect["IntersectGridPoints"]:
#     project.objects.append(pt)


# lines_and_house = intersect_calculator.getIntersectLinePolyCurve(PC1, [l3,l4,l5,l6], True)
# print(lines_and_house)
# for pt in lines_and_house["IntersectGridPoints"]:
#     project.objects.append(pt)

# for splittedlines in lines_and_house["SplittedLines"]:
#     project.objects.append(splittedlines)

# for outergridlines in lines_and_house["OuterGridLines"]:
#     project.objects.append(outergridlines)

# for innergridlines in lines_and_house["InnerGridLines"]:
#     project.objects.append(innergridlines)


# intersections = find_polycurve_intersections(PC1, PC2)
# split_polycurves = split_polycurve_at_intersections(PC2, intersections)
# for sp_pc in split_polycurves:
#     project.objects.append(sp_pc)

# split_polycurves = split_polycurve_at_intersections(PC3, intersections)
# for sp_pc in split_polycurves:
#     project.objects.append(sp_pc)


# PC10 = PolyCurve.byPoints([Point(410,410,0), Point(410,810,0), Point(8000,810,0), Point(8000,410,0)])
# project.objects.append(PC10)
# for index, line in enumerate(PC1.curves):
#     print(PC10, line)
#     x = splitPolyCurveByLine(PC10, line)
#     for lines in PC10.curves:
#         print(lines)
#     for points in PC10.points:
#         print(points)
#     for i in x:
#         project.objects.append(i)

# c1 = [Line(Point(3690,410,0),Point(3690,810,0)),
# Line(Point(3690,810,0),Point(4090,810,0)),
# Line(Point(4090,810,0),Point(4090,410,0)),
# Line(Point(4090,410,0),Point(3690,410,0))]

# pc = PolyCurve.byJoinedCurves(c1)

# pc = PolyCurve.byPoints([Point(3690,410,0), Point(3690,3000,0), Point(4090,3000,0), Point(4090,410,0)])

pc = PolyCurve.byPoints([Point(3700,410,0), Point(3700,810,0), Point(4200,810,0), Point(4200,410,0)])
# pc = PolyCurve.byPoints([Point(3950,100,0), Point(3950,200,0), Point(4100,200,0), Point(4100,100,0)])
pc = PolyCurve.byPoints([Point(3950,100,0), Point(3950,500,0), Point(4100,500,0), Point(4100,100,0)])

# print(pc.curves)
# project.objects.append(pc)

for index, line in enumerate(PC1.curves):
    x = splitPolyCurveByLine(pc, line)
    # for i in x:
    #     project.objects.append(i)

# for index, line in enumerate(PC1.curves):
#     for p, i in enumerate(test_res):
#         PCPanel = i.extrusion.polycurve_3d_translated
#         project.objects.append(PCPanel)

#         x = splitPolyCurveByLine(PCPanel, line)
#         for i in x:
#             project.objects.append(i)


# sys.exit()

# x = splitPolyCurveByLine(PC4, Line4)
# for i in x:
#     project.objects.append(i)


# b = splitPolyCurveByLine(PC5, Line4)
# for i in b:
#     project.objects.append(i)

# b = splitPolyCurveByLine(PC6, Line5)
# for i in b:
#     project.objects.append(i)

# sys.exit()
# print(split_polycurves)
# project.objects.append(split_polycurves)
# project.objects.append(new_one)

# for p in split_polycurves:
#     print(p.curves)

# for curve in flatten(split_polycurves):
#     # print(curve)
#     project.objects.append(curve)
    # print(curve)  
#     for i in curve.curves:
#         print(i)

# Now `split_polycurves` csontains the segments of PC1 split by PC2

# i = fillin(PC1, test_res)
# print(i)
# for item in i:
#     project.objects.append(item)

project.toSpeckle("bd33f3c533")