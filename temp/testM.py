from objects.frame import *
from exchange.speckle import *
from objects.datum import *
from library.profile import *
from copy import deepcopy

def translatePolyCurve2Da(plycrv2D,justificationx,justificationy):
    xval = []
    yval = []
    for i in plycrv2D:
        xval.append(i.start.x)
        yval.append(i.start.y)

    #Boundingbox2D
    xmin = min(xval)
    xmax = max(xval)
    ymin = min(yval)
    ymax = max(yval)
    b = xmax-xmin
    h = ymax-ymin
    print(h)

    dytop = -ymax
    dybottom = -ymin
    dycenter = dytop - 0.5 * h #CHECK
    dyorigin = 0

    dxleft = -xmax
    dxright = -xmin
    dxcenter = dxleft + 0.5 * b #CHECK
    dxorigin = 0

    if justificationx == "center":
        dx = dxcenter
    elif justificationx == "left":
        dx = dxleft
    elif justificationx == "right":
        dx = dxright
    elif justificationx == "origin":
        dx = 0
    else:
        dx = 0
    print("dx =")
    print(dx)

    if justificationy == "center":
        dy = dycenter
    elif justificationy == "top":
        dy = dytop
    elif justificationy == "bottom":
        dy = dybottom
    elif justificationy == "origin":
        dy = 0
    else:
        dy = 0
    print("dy =")
    print(dy)

    for i in plycrv2D:
        if i.__class__.__name__ == "Arc2D":
            x1 = i.start.x + dx
            i.start.y =+ dy
            i.middle.x =+ dx
            i.middle.y =+ dy
            i.end.x =+ dx
            i.end.y =+ dy
            c = Arc2D(point2D(x1,y1))
        elif i.__class__.__name__ == "Line2D":
            print(i)
            i.start.x =+ dx
            i.start.y =+ dy
            i.end.x =+ dx
            i.end.y =+ dy

        else:
            print("Curvetype not found")
    return plycrv2D

a = profiledataToShape("HEA200").prof.curve

b = deepcopy(a)
b = translatePolyCurve2Da(b, "origin", "origin")

#b = translatePolyCurve2Da(b, "left", "top")
#b = translatePolyCurve2Da(b, "left", "top")

for i in a:
    print(i.start)

print("transformed curve")
for i in b:
    print(i.start)

sys.exit()
obj1 = []
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 0, 0), Point(1000, 0, 0), "L70/70/7","test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 100, 0), Point(1000, 100, 0), "L70/70/7","test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileName(Point(0, 300, 0), Point(1000, 300, 0), "HEA200","test")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 0), Point(1000, 500, 0), "HEA200","test","origin","origin")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 300), Point(1000, 500, 300), "HEA200","test","top","origin")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 600), Point(1000, 500, 600), "HEA200","test","bottom","origin")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 900), Point(1000, 500, 900), "HEA200","test","center","origin")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 1200), Point(1000, 500, 1200), "HEA200","test","top","left")) # dakligger deel 1
obj1.append(Frame.byStartpointEndpointProfileNameOrientation(Point(0, 500, 1500), Point(1000, 500, 1500), "HEA200","test","origin","origin")) # dakligger deel 1



SpeckleObj = translateObjectsToSpeckleObjects(obj1)
Commit = TransportToSpeckle("struct4u.xyz", "1852cf784e", SpeckleObj, "Test objects")