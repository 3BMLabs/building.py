from objects.frame import *
from exchange.speckle import *

#Proof of Concept of Wood Frame Wall
def POCWoodFrameWall(l,h,startPoint,studheight,studwidth,spacing):
    distribution = 0 #Fixed Distance, Fixed Number, Maximum Spacing, Minimum Spacing
    count = round(l/spacing)
    obj1 = []
    x = 0 + studheight*0.5
    for i in range(count):
        obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint, Vector3(x, 0, studheight)),
                                               Point.translate(startPoint, Vector3(x, 0, h-studheight)),
                                               Rectangle("stud", studwidth, studheight).curve, "stud", 0, BaseTimber))
        x = x + spacing

    obj1.append(Frame.by_startpoint_endpoint(startPoint, Point.translate(startPoint,Vector3(l,0,0)),Rectangle("stud", studwidth, studheight).curve.translate(Vector2(studheight/2,0)),"bottomplate", 90, BaseTimber))
    obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint,Vector3(0,0,h)), Point.translate(startPoint,Vector3(l,0,h)),Rectangle("stud", studwidth, studheight).curve.translate(Vector2(-studheight/2,0)),"topplate", 90, BaseTimber))
    obj1.append(Frame.by_startpoint_endpoint(Point.translate(startPoint, Vector3(l-studheight*0.5, 0, studheight)),
                                           Point.translate(startPoint, Vector3(l-studheight*0.5, 0, h - studheight)),
                                           Rectangle("stud", studwidth, studheight).curve, "last stud", 0, BaseTimber))
    return obj1

a = POCWoodFrameWall(2000,2600,Point(0, 0, 0),38,184,407)
b = POCWoodFrameWall(1500,1000,Point(2000, 0, 0),38,184,407)
c = POCWoodFrameWall(1500,600,Point(2000, 0, 2000),38,184,407)
d = POCWoodFrameWall(2000,2600,Point(3500, 0, 0),38,184,407)

obj = a + b + c + d

SpeckleObj = translateObjectsToSpeckleObjects(obj)
Commit = TransportToSpeckle("struct4u.xyz", "58b53799c6", SpeckleObj, "Test objects")

