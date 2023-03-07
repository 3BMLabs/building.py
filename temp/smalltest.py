from library.profile import *
from exchange.speckle import *
test = profiledataToShape("HEA300")[0].curve

test2 = PolyCurve.byPolyCurve2D(test)

print(test2)

sys.exit()
SpeckleObj = translateObjectsToSpeckleObjects(test)

Commit = TransportToSpeckle("struct4u.xyz", "16c0309866", SpeckleObj, "Test with Plates from XFEM4U")