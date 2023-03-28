import sys, os, math, random
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from abstract.color import *
from library.material import *
from objects.frame import *
# from exchange.speckle import *
# from objects.steelshape import *
# from library.profile import *

# test = profiledataToShape("HEA200")

# print(test)

obj1 = []

sys.exit()

SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "1852cf784e", SpeckleObj, "Test objects")

