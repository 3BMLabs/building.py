from geometry.systemsimple import *
from project.fileformat import BuildingPy

from abstract.intersect2d import *
from geometry.systemsimple import *

import sys

project = BuildingPy("Test patterns 3D","0")
project.speckleserver = "speckle.xyz"

test1 = PatternSystem().StretcherBondWithJoint("halfsteensverband",100,210,50,10,12.5)
test2 = PatternSystem().TileBondWithJoint("tegels",400,400,10,10,10)
test3 = PatternSystem().CrossBondWithJoint("kruisverband test",100,210,50,10,12.5)


def PatternGEOM2(PatternSystem,width,height):
    test = PatternSystem
    panels = []
    for i,j in zip(test.basepanels,test.vectors):
        ny = int(height / (j[0].y)) #number of panels in y-direction
        nx = int(width / (j[1].x)) #number of panels in x-direction
        PC = i.origincurve
        thickness = i.thickness
        color = i.colorint

        #YX ARRAY
        yvectdisplacement = j[0]
        yvector = Vector3(0,0,0)
        xvectdisplacement = j[1]
        xvector = Vector3(0, 0, 0)

        ylst = []
        for k in range(ny):
            yvector = Vector3.sum(yvectdisplacement, yvector)
            for l in range(nx):
                #Copy in x-direction
                xvector = Vector3.sum(xvectdisplacement, xvector)
                print(xvector)
                xyvector = Vector3.sum(yvector,xvector)
                PCNew = PolyCurve.copyTranslate(PC,xyvector) #translate curve in x and y-direction
                pan = Panel.byPolyCurveThickness(PCNew,thickness,0,"name",color)
                panels.append(PCNew)
            xvector = Vector3.sum(xvectdisplacement, Vector3(0, 0, 0))
    return panels

paneelcontouren = PatternGEOM2(test2,4000,4000) # polycurves van panelen

contour = PolyCurve.byPoints([Point(1000,1000,0),Point(3000,1000,0),Point(3500,3500,0),Point(2000,3500,0),Point(1000,1000,0)])
contour2d = contour.to_polycurve_2D()

contour_panel = Panel.byPolyCurveThickness(contour,5,0,"name",BaseBrickYellow.colorint)

project.objects.append(contour_panel)

for i in paneelcontouren:
    i2d = i.to_polycurve_2D()
    test = is_polycurve_in_polycurve(contour2d,i2d)
    print(test)

sys.exit()
#for i in test_res:
 #   print(i)
#sys.exit()

#intersections = find_polycurve_intersections(PC1, PC2)
#split_polycurves = split_polycurve_at_intersections(PC2, intersections)

#for sp_pc in split_polycurves:
#    project.objects.append(sp_pc)

for i in test_res:
    j = Panel.byPolyCurveThickness(i,20,0,"name",BaseBrick.colorint)
    project.objects.append(j)

project.toSpeckle("3e34ec62e2")