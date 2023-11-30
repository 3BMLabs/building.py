import sys, os, math
from pathlib import Path
import json
import urllib.request

package_root_directory = "C:/Users/mikev/Documents/GitHub/building.py/"
sys.path.append(str(package_root_directory))

from temp.Revit.LIb import *

test = searchProfile("HEA200")

OUT = test