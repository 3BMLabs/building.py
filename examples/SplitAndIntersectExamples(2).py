import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from geometry.curve import Line, PolyCurve
from library.profile import data as jsondata

from project.fileformat import BuildingPy
from abstract.intersect2d import split_polycurve_by_line
from geometry.point import Point


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

# PC1 = PolyCurve.by_points([p1,p2,p3,p4,p5])
# project.objects.append(PC1)

window1 = [Point(-500,500,0), Point(500,750,0), Point(750,750,0), Point(750,500,0)]

# PC2 = PolyCurve.by_points(window1)

window2 = [Point(3700,6000,0), Point(500,750,0), Point(750,750,0), Point(750,500,0)]

# PC3 = PolyCurve.by_points(window2)

Line4 = Line(start=Point(2500, -900, 0), end=Point(2500, 6000, 0))
project.objects.append(Line4)

p1 = Point(650,2500,0)
p2 = Point(1000,3000,0)
p3 = Point(6000,6500,0)
p5 = Point(4000,2500,0)

PC4 = PolyCurve.by_points([p1,p2,p3,p5])
project.objects.append(PC4)


p1 = Point(0,-500,0)
p2 = Point(0,500,0)
p3 = Point(4000,500,0)
p5 = Point(4000,-500,0)

PC5 = PolyCurve.by_points([p1,p2,p3,p5])
project.objects.append(PC5)

PC6 = PolyCurve.by_points([p5,p3,p2,p1])


# Line5 = Line(start=Point(1500, -750, 0), end=Point(1500, 1500, 0))
# project.objects.append(Line5)

# p1 = Point(1000,-500,0)
# p2 = Point(500,250,0)
# p3 = Point(750,300,0)
# p4 = Point(1000,400,0)
# p5 = Point(2000,500,0)
# p6 = Point(2500,0,0)
# p7 = Point(2000,-500,0)
# PC6 = PolyCurve.by_points([p1,p2,p3,p4,p5,p6,p7])
# project.objects.append(PC6)



# project.objects.append(PC3)

# for j in window1:
#     project.objects.append(j)

# test1 = PatternSystem().stretcher_bond_with_joint("halfsteensverband",100,210,50,10,12.5)
# test2 = PatternSystem().tile_bond_with_joint("tegels",400,400,10,10,10)
# test3 = PatternSystem().cross_bond_with_joint("kruisverband test",100,210,50,10,12.5)
# test_res = pattern_geom(test3,2000,2000)

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

# intersect_calculator = Intersect2d()


# multiline_intersect = intersect_calculator.getMultiLineIntersect([l3,l4,l5,l6])
# for res_intersect in multiline_intersect:
#     print(res_intersect)
#     project.objects.append(res_intersect)


# polycurve_intersect = intersect_calculator.get_intersect_line_polycurve(PC2, [l3,l4,l5,l6], True)
# print(polycurve_intersect)

# for pt in polycurve_intersect["IntersectGridPoints"]:
#     project.objects.append(pt)


# lines_and_house = intersect_calculator.get_intersect_line_polycurve(PC1, [l3,l4,l5,l6], True)
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



x = split_polycurve_by_line(PC4, Line4)
for i in x:
    project.objects.append(i)

# b = split_polycurve_by_line(PC5, Line4)
# for i in b:
#     project.objects.append(i)

b = split_polycurve_by_line(PC6, Line4)
for i in b:
    project.objects.append(i)

# b = split_polycurve_by_line(PC6, Line5)
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

project.to_speckle("bd33f3c533")