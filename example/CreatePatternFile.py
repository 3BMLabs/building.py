from exchange.pat import *

pat = TilePattern("500x500", 500, 500, Revitmodelpattern)

pat.insert(0, Patprefix)


patn = []
for i in pat:
    patn.append(i+ "\n")
#Create PAT-file
fp = open('C:/TEMP/test.pat', 'w')
for i in patn:
    fp.write(i)

fp.close()
