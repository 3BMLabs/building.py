import glob, sys#, fitz
from glob import glob
import re
from os import path

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))


pythonfiles = \
    [
    "packages/helper.py",
    "packages/svg/path/parser.py",
    "packages/svg/path/path.py",
    "abstract/vector.py",    
    "geometry/point.py",
    "project/fileformat.py",
    "abstract/coordinatesystem.py",
    "abstract/matrix.py",
    "geometry/curve.py",
    "abstract/node.py",
    "abstract/color.py",
    "abstract/image.py",
    "abstract/interval.py",
    "abstract/plane.py",
    "abstract/text.py",
    "geometry/bmesh.py",
    "geometry/geometry2d.py",
    "abstract/intersect.py",
    "abstract/intersect2d.py",
    "geometry/linestyle.py",
    "geometry/pointcloud.py",
    "geometry/solid.py",
    "geometry/surface.py",
    "objects/panel.py",
    "abstract/boundingbox.py",
    "geometry/systemsimple.py",
    "library/material.py",
    "library/profile.py",
    "objects/analytical.py",
    "objects/annotation.py",
    "objects/datum.py",
    "objects/frame.py",
    "objects/shape.py",
    "objects/shape3d.py",
    "objects/steelshape.py",
    "objects/view.py",
    "exchange/pat.py",
    ]

#if export to Revit, add this line:     "exchange/revit.py"
#if export to Scia, add this line:     "exchange/scia.py"

BuildingPySingleFileStr = ""
Includedstr = "# [included in BP singlefile]"

for i in pythonfiles:
    with open(i) as f:
        str = f.read()
        if i == "packages/svg/path/parser.py":
            str = str.replace("path.", "")
        if Includedstr in str:
            BuildingPySingleFileStr = BuildingPySingleFileStr + str

start = '# [!not included in BP singlefile - start]'
end = '# [!not included in BP singlefile - end]'
s = BuildingPySingleFileStr

test2 = ((s.split(start))[1].split(end)[0])

i = 0
max = BuildingPySingleFileStr.count(start)

for j in range(max):
    try:
        substringtoremove = (BuildingPySingleFileStr.split(start))[1].split(end)[0]
        BuildingPySingleFileStr = BuildingPySingleFileStr.replace(substringtoremove, "")
        BuildingPySingleFileStr = BuildingPySingleFileStr.replace(start, "",1)
        BuildingPySingleFileStr = BuildingPySingleFileStr.replace(end, "",1)
    except:
        print("out of range")

BuildingPySingleFileStr = BuildingPySingleFileStr.replace(Includedstr, "")

BuildingPySingleFileStr_NoImports = ""

for line in BuildingPySingleFileStr.split("\n"):
    if "from " in line and "#" not in line and len(line) < 20:
        pass
    elif "import " in line and "#" not in line:
        pass
    else:
        BuildingPySingleFileStr_NoImports = BuildingPySingleFileStr_NoImports + "\n" + line
BuildingPySingleFileStr = BuildingPySingleFileStr_NoImports

startstr = "#[BuildingPy] DO NOT EDIT THIS FILE. IT IS GENERATED FROM THE SOURCE CODE\n" \
    "import math\n" \
    "from math import sqrt, cos, sin, acos, degrees, radians, log, pi\n" \
    "import sys\n" \
    "import os\n" \
    "import re\n" \
    "import json\n" \
    "import bisect\n" \
    "from abc import *\n" \
    "from collections import defaultdict\n" \
    "from collections.abc import MutableSequence\n" \
    "import subprocess\n" \
    "import urllib\n" \
    "import time\n" \
    "import urllib.request\n" \
    "import string\n" \
    "import random\n" \
    "from typing import List, Tuple, Union\n" \
    "import xml.etree.ElementTree as ET\n" \
    "from pathlib import Path\n" \
    "import copy\n" \
    "import pickle\n" \
    "from functools import reduce\n" \
    "import struct\n" \
    "#import ezdxf\n" \

BuildingPySingleFileStr = startstr + BuildingPySingleFileStr

with open('bp_single_file.py', 'w+') as fh:
    fh.write(BuildingPySingleFileStr)