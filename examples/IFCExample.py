import sys, os, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from construction.panel import *
from construction.frame import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from library.profile import nameToProfile
from construction.annotation import *
from geometry.solid import *
from exchange.IFC_2 import *

ifc = IfcBp().create("testproject","testlibrary")
ifc.organisation_application("3BM", "Jonathan")
ifc.ownerhistory()
ifc.site_building("Site","Building")

ifc.write("test.ifc")