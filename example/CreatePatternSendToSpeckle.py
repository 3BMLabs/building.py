from exchange.pat import *

test = PATRow().create(0,0,0,0,400,0,0)

pat1 = PAT().TilePattern("500x500", 500, 500, Revitmodelpattern)
pat2 = PAT().BlockPattern("Blokpatroon",300,4,Revitmodelpattern)

print(pat1.patstrings)
print(pat2.patstrings)
