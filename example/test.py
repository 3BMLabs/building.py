from geometry.geometry2d import Point2D
from exchange.speckle import *
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Line as SpeckleLine
from specklepy.objects.geometry import Mesh as SpeckleMesh
from specklepy.objects.geometry import Polyline
from specklepy.objects.geometry import Vector as SpeckleVector
from specklepy.objects.geometry import Plane as SpecklePlane
from specklepy.objects.geometry import Arc as SpeckleArc

#Speckle Point
SpecklePoint.from_coords(0, 0, 0)

#Speckle Line
Line = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(800, 1000, 1000))

#Speckle Vector
#V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector

#Speckle Plane
V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector
X = SpeckleVector.from_coords(1000, 0, 0)
Y = SpeckleVector.from_coords(0, 1000, 0)
Orig = SpecklePoint.from_coords(0, 0, 0)
#pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)

#Speckle Polyline
P1 = SpecklePoint.from_coords(0,0,0)
P2 = SpecklePoint.from_coords(1000,0,0)
P3 = SpecklePoint.from_coords(2000,0,0)
P4 = SpecklePoint.from_coords(2000,1000,0)

ply = Polyline.from_points([P1,P2,P3,P4])

#-1762845660


Messie = SpeckleMesh(vertices = [0,0,0,1000,0,0,1000,1000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh") #, units = "mm"
Messie2 = SpeckleMesh(vertices = [1000,1000,0,1000,1000,1000,2000,2000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh", colors = [-1762845660,-1762845660,-1762845660]) #, units = "mm"

#    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
# list structure of verts is x y z x y z x y z
#    faces = [3, 0, 1, 2, 3, 2, 3, 5]

class Arc:
    def __init__(self, startPoint: SpecklePoint, midPoint: SpecklePoint, endPoint: SpecklePoint):
        self.startPoint = startPoint
        self.midPoint = midPoint
        self.endPoint = endPoint
        self.plane = SpecklePlane(
            origin=SpecklePoint.from_coords((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2),
            normal=SpeckleVector.from_coords(0, 0, 1),
            xdir=SpeckleVector.from_coords(1, 0, 0),
            ydir=SpeckleVector.from_coords(0, 1, 0)
        )
        self.radius=self.radius()
        self.startAngle=0
        self.endAngle=0
        self.angleRadians=0
        self.area=0
        self.length=self.length()
        self.units="mm"

    def distance(self, p1, p2):
        return math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2)
    
    def radius(self):
        a = self.distance(self.startPoint, self.midPoint)
        b = self.distance(self.midPoint, self.endPoint)
        c = self.distance(self.endPoint, self.startPoint)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s-a) * (s-b) * (s-c))
        R = (a * b * c) / (4 * A)
        return R

    def length(self):
        x1, y1, z1 = self.startPoint.x, self.startPoint.y, self.startPoint.z
        x2, y2, z2 = self.midPoint.x, self.midPoint.y, self.midPoint.z
        x3, y3, z3 = self.endPoint.x, self.endPoint.y, self.endPoint.z

        r1 = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5 / 2
        a = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
        b = math.sqrt((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)
        c = math.sqrt((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)
        cos_hoek = (a**2 + b**2 - c**2) / (2*a*b)
        m1 = math.acos(cos_hoek)
        arc_length = r1 * m1

        return arc_length


    @classmethod
    def ByThreePoints(self, startPoint: SpecklePoint, midPoint: SpecklePoint, endPoint: SpecklePoint, plane=None):
        radius = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).radius
        startAngle = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).startAngle
        endAngle = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).endAngle
        angleRadians = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).angleRadians
        area = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).area
        length = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).length
        units = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).units

        if plane is None:
            plane = SpecklePlane(
                origin=SpecklePoint.from_coords((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2),
                normal=SpeckleVector.from_coords(0, 0, 1),
                xdir=SpeckleVector.from_coords(1, 0, 0),
                ydir=SpeckleVector.from_coords(0, 1, 0)
            )
        
        return SpeckleArc(
            startPoint=startPoint,
            midPoint=midPoint,
            endPoint=endPoint,
            domain=SpeckleInterval(start=0, end=1),
            plane=plane,
            radius=radius,
            startAngle=startAngle,
            endAngle=endAngle,
            angleRadians=angleRadians,
            area=area,
            length=length,
            units=units
        )
    
    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


p10=SpecklePoint.from_coords(10, 0, 0)
p20=SpecklePoint.from_coords(500, 20, 0)
p30=SpecklePoint.from_coords(1000, 0, 0)
p = Arc.ByThreePoints(startPoint=p10,midPoint=p20,endPoint=p30)


# OPTIONAL
# plane1 = SpecklePlane(
#     origin=SpecklePoint.from_coords(500,12,0),
#     normal=SpeckleVector.from_coords(0, 0, 1),
#     xdir=SpeckleVector.from_coords(1, 0, 0),
#     ydir=SpeckleVector.from_coords(0, 1, 0)
# )
#p = Arc.ByThreePoints(startPoint=p1,midPoint=p2,endPoint=p3, plane=plane1) -> optional plane


print("Start point:", p.startPoint)
print("Mid point:", p.midPoint)
print("End point:", p.endPoint)
print("Plane:", p.plane)
print("Plane Origin:", p.plane.origin)
print("Radius:", p.radius)
print("Length:", p.length)


obj = []

obj.append(ply)
obj.append(Line)
obj.append(Messie)
obj.append(Messie2)
obj.append(p)


#sys.exit()

SpeckleHost = "speckle.xyz"  # struct4u.xyz
StreamID = "ca31cc7a2f"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)

print(Commit)


