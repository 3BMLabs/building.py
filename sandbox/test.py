from library.profile import *
from objects.profile import *
from objects.frame import *
from project import fileformat

project = BuildingPy("Jan zijn ligger project", "0")

test = nameToProfile("UNP300").profile.curve

f1 = Frame.by_startpoint_endpoint(Point(0,0,0),Point(3000,0,0),"HEA300","HEA300+zeeg 30 mm",BaseSteel)
prof = TProfile("T-profiel 2",300,200,100,100)
print(prof)

f2 = Frame.by_startpoint_endpoint(Point(0,1500,0),Point(3000,1500,0),prof,"T profiel test",BaseSteel)

print(f1.profile)
print(f2.profile)

project.objects.append(f1)
project.objects.append(f2)


project.toSpeckle("31d9948b31")