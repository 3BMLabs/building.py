from pil_img import *
from objects.frame import *
from temp.Joasdiv import cone_to_speckle
from objects.shape import *
from objects.shape3d import *


img = Image.open("photo.jpg")
image = send_img_to_speckle(img)
lshape = Frame.byStartpointEndpoint(Point(-300, 0, 0), Point(-300, 0, 50), Lshape("joas", 300, 200, 50, 50).curve, "L-frame", 0, BaseSteel)
l2shape = Frame.byStartpointEndpoint(Point(-600, 0, 0), Point(-600, 0, 50), Lshape("joas", 300, 200, 50, 50).curve, "L-frame", 0, BaseSteel)
SpeckleObj = translateObjectsToSpeckleObjects([lshape, l2shape])
lst = [SpeckleObj, image]
list1 = Origin()




# cone = cone_to_speckle()
# lst2 = [cone]


Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", list1, "Test")
# Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst2, "Test")
