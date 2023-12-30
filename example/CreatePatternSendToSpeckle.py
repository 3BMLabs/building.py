from exchange.pat import *

pat1 = PAT().TilePattern("500x500", 500, 500, Revitmodelpattern)
pat2 = PAT().BlockPattern("Blokpatroon",300,4,Revitmodelpattern)
pat3 = PAT().ParallelLines("Bamboe",[0,150,100,100,50,150,50,100,100],Revitmodelpattern)

CreatePatFile([pat1,pat2,pat3],'C:/TEMP/test3.pat')