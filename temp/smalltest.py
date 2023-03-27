from pil_img import *
from objects.frame import *


img = Image.open("photo.jpg")
image = send_img_to_speckle(img)
lshape = Frame.byStartpointEndpoint(Point(-300, 0, 0), Point(-300, 0, 50), Lshape("joas", 300, 200, 50, 50).curve, "L-frame")
l2shape = Frame.byStartpointEndpoint(Point(-600, 0, 0), Point(-600, 0, 50), Lshape("joas", 300, 200, 50, 50).curve, "L-frame")


SpeckleObj = translateObjectsToSpeckleObjects([lshape, l2shape])
lst = [SpeckleObj, image]


Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", lst, "Test")
