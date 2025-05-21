











from abstract.vector import Point
from exchange.pat import PAT
from geometry.curve import PolyCurve
from geometry.systemsimple import pattern_geom
from project.fileformat import BuildingPy


project = BuildingPy("Split and Intersect examples","0")
project.speckleserver = "speckle.xyz"

p1 = Point(0,0,0)
p2 = Point(0,3000,0)
p3 = Point(2000,6500,0)
p4 = Point(4000,3000,0)
p5 = Point(4000,0,0)

PC1 = PolyCurve.by_points([p1,p2,p3,p4,p5])
project.objects.append(PC1)

#MULTI PATROON

test2 = PAT().stretcher_bond_with_joint("halfsteensverband",0,210,50,10,12.5)
# test2 = PatternSystem().tile_bond_with_joint("tegels",400,400,0,10,10)
test_res = pattern_geom(test2, 5400, 7500, Point(-1000, -1000, 0))


for index, line in enumerate(PC1.curves):
    for p, i in enumerate(test_res):

        PCPanel = PolyCurve.from_polycurve_3D(i.extrusion.polycurve_3d_translated)

        x = split_polycurve_by_line(PCPanel, line)

        if len(x["splittedPolycurve"]) == 0:
            if is_polycurve_in_polycurve(x["inputPolycurve"][0], PC1):
                project.objects.append(x["inputPolycurve"][0])
                
        else:
            for i in x["splittedPolycurve"]:
                try:
                    if is_point_in_polycurve(i.centroid(), PC1):
                        project.objects.append(i)
                except:
                    pass

project.to_speckle("bd33f3c533")