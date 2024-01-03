from exchange.pat import *
from project.fileformat import BuildingPy

project = BuildingPy("Test patterns","0")
project.speckleserver = "speckle.xyz"

pat1 = PAT().TilePattern("500x500", 500, 500, Revitmodelpattern)
pat2 = PAT().BlockPattern("Blokpatroon",300,4,Revitmodelpattern)
pat3 = PAT().Strips("hor_200",200,0,Revitmodelpattern)
pat4 = PAT().StretcherBondPattern("Brick700x300_100",700,300,200,Revitmodelpattern)
pat5 = PAT().TilePatternWithJoint("tiles500x500",500,500,10,20,Revitmodelpattern)
pat6 = PAT().CombiPattern("Combipatroon",300,Revitmodelpattern)
pat7 = PAT().ChevronPattern("Hongaarsepunt",500,100,Revitmodelpattern)
pat8 = PAT().HerringbonePattern("Visgraat",500,5,Revitmodelpattern)
pat9 = PAT().ParallelLines("Bamboe",[0,150,100,100,50,150,50,100,100],Revitmodelpattern)
pat10 = PAT().StretcherBondWithJoint("WF_210x50",210,50,10,12.5,Revitmodelpattern)
pat11 = PAT().Strips("hor_200",200,25,Revitmodelpattern)
pat12 = PAT().ParallelLines("Rollaag", [0,50,12.5],Revitmodelpattern)

lst = [pat1,pat2,pat3,pat4,pat5,pat6,pat7,pat8,pat9,pat10,pat11,pat12]
#lst = [pat5]

CreatePatFile(lst,'C:/TEMP/test4.pat')

dx = 0
spacing = 8000


for i in lst:
    for j in PAT2Geom(i,2500,2500,dx,0):
        project.objects.append(j)
    dx = dx + spacing

#project.toSpeckle("3e34ec62e2")
