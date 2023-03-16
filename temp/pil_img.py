from exchange.speckle import *
from PIL import Image
from objects.shape import *
from objects.frame import *


square = Frame.byStartpointEndpoint(Point(0, 0, 0), Point(1, 0, 0), Rectangle("joas", 0, 1).curve, "L-frame")
square2 = Frame.byStartpointEndpoint(Point(1, 0, 0), Point(2, 0, 0), Rectangle("joas", 0, 1).curve, "L-frame")
square3 = Frame.byStartpointEndpoint(Point(2, 0, 0), Point(3, 0, 0), Rectangle("joas", 0, 1).curve, "L-frame")


img = Image.open("rgb.png")
pixels = img.load()
kleurcode_rijen = []
pixellist = []


for y in range(img.height):
    rij_kleurcodes = []
    for x in range(img.width):
        rij_kleurcodes.append(pixels[x, y])
    kleurcode_rijen.append(rij_kleurcodes)


for kleurcode_rij in kleurcode_rijen:
    for kleurcode in kleurcode_rij:
        pixellist.append(kleurcode)


print(pixellist)


SpeckleObj = translateObjectsToSpeckleObjects([square, square2, square3])
Commit = TransportToSpeckle("speckle.xyz", "8136460d9e", SpeckleObj, "Shiny Commit")
