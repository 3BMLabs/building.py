import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from objects.analytical import *


a = 1000
b = 500
c = a + b
d = a * b

e = "Job"
f = "Jesper"
g = e + " " + f

h = math.sqrt(1000 * 1000 + 2000 * 2000 + 500 * 500)

print(h)