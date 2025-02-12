
from construction.panel import *
from construction.beam import *
from construction.profile import *
from exchange.speckle import *
from library.profile import data as jsondata
from library.material import *
from construction.annotation import *
from geometry.solid import *
from exchange.IFC_2 import *

ifc = IfcBp().create("testproject","testlibrary")
ifc.organisation_application("3BM", "Jonathan")
ifc.ownerhistory()
ifc.site_building("Site","Building")

ifc.write("test.ifc")