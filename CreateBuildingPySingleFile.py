import glob, sys, fitz
from glob import glob
import re

from os import path

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

folder = "C:/Users/mikev/Documents/GitHub/building.py/abstract"
pythonfiles = find_ext(folder,'py')

BuildingPySingleFileStr = ""

for i in pythonfiles:
    with open(i) as f:
        str = f.read()
        if "# [included in BP singlefile]" in str:
            BuildingPySingleFileStr = BuildingPySingleFileStr + str

start = '# [!not included in BP singlefile - start]'
end = '# [!not included in BP singlefile - end]'
s = BuildingPySingleFileStr
t = s.find(start) + len(start)

#res = s[s.find(start)+len(start):s.rfind(end)]


splt = BuildingPySingleFileStr.split("# [!not included in BP singlefile - start]"
)
print(t)
#print(pythonfiles)