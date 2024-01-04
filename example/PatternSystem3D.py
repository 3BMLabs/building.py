from geometry.systemsimple import *
from project.fileformat import BuildingPy

project = BuildingPy("Test patterns 3D","0")
project.speckleserver = "speckle.xyz"

test1 = PatternSystem().StretcherBondWithJoint("halfsteensverband",100,210,50,10,12.5)
test2 = PatternSystem().TileBondWithJoint("tegels",400,400,10,10,10)
test3 = PatternSystem().CrossBondWithJoint("kruisverband test",100,210,50,10,12.5)

test_res = PatternGEOM(test3,4000,3000)

for i in test_res:
    project.objects.append(i)

project.toSpeckle("3e34ec62e2")