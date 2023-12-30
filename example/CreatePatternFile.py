from exchange.pat import *
import sys

pat1 = TilePattern("500x500", 500, 500, Revitmodelpattern)
pat2 = Strips("hor_200",200,0,Revitmodelpattern)
pat3 = StretcherBondPattern("Brick700x400_100",700,400,200,Revitmodelpattern)
pat4 = BlockPattern("Blokpatroon",300,4,Revitmodelpattern)
pat5 = CombiPattern("Combipatroon",300,Revitmodelpattern)
pat6 = ChevronPattern("Hongaarsepunt",500,100,Revitmodelpattern)
pat7 = HerringbonePattern("Visgraat",500,5,Revitmodelpattern)

patternstrings = pat1 + pat2 + pat3 + pat4 + pat5 + pat6 + pat7
patternstrings.insert(0, Patprefix)



for i in patternstrings:
    print(i)

patn = []
for i in patternstrings:
    patn.append(i+ "\n")
#Create PAT-file
fp = open('C:/TEMP/test.pat', 'w')
for i in patn:
    fp.write(i)

fp.close()
