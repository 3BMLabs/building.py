import sys, random, math
from svg.path import parse_path
import json
from typing import List, Tuple
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

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
from specklepy.objects.primitive import Interval as SpeckleInterval


#Speckle Point
SpecklePoint.from_coords(0, 0, 0)

#Speckle Line
Line = SpeckleLine(start = SpecklePoint.from_coords(0, 0, 0), end = SpecklePoint.from_coords(-800, -1000, 1000))

#Speckle Vector
V1 = SpeckleVector.from_coords(0, 0, 1000) # Vector

#Speckle Plane

#Speckle Arc
V1 = SpeckleVector.from_coords(0, 0, 1) # Vector
X = SpeckleVector.from_coords(1, 0, 0)
Y = SpeckleVector.from_coords(0, 1, 0)
Orig = SpecklePoint.from_coords(20, 0, 0)

pln = SpecklePlane(origin=Orig, normal=V1, xdir=X, ydir=Y)
int = SpeckleInterval(start=0, end=5, totalChildrenCount=1)

arcie = SpeckleArc(
   startPoint=SpecklePoint.from_coords(0, 0, 0),
   midPoint=SpecklePoint.from_coords(1000, 0, 0),
   endPoint=SpecklePoint.from_coords(2000, 500, 0),
   plane=pln,
   radius=1, #must be at least > 1
   interval=int,
   units="mm"
)



Messie = SpeckleMesh(vertices = [0,0,0,1000,0,0,1000,1000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh") #, units = "mm"
Messie2 = SpeckleMesh(vertices = [1000,1000,0,1000,1000,1000,2000,2000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh", colors = [-1762845660,-1762845660,-1762845660]) #, units = "mm"

vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
# list structure of verts is x y z x y z x y z
faces = [3, 0, 1, 2, 3, 2, 3, 5]


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

# p10=SpecklePoint.from_coords(10, 0, 0)
# p20=SpecklePoint.from_coords(500, 20, 0)
# p30=SpecklePoint.from_coords(1000, 0, 0)
# p = Arc.ByThreePoints(startPoint=p10,midPoint=p20,endPoint=p30)


class Text:
    def __init__(self, text: str = None, font_family: str = None, bounding_box: bool = None, xyz: Tuple[float, float, float] = None, rotation: float = None):
        self.text = text
        self.font_family = font_family
        self.bounding_box = bounding_box
        self.originX, self.originY, self.originZ = xyz or (0, 0, 0)
        self.x, self.y, self.z = xyz or (0, 0, 0)
        self.rotation = rotation
        self.character_offset = 150
        self.spacie = 200
        self.path_list = self.load_path()


    def load_path(self) -> List[str]:
        with open(f'C:/Users/jonat/Desktop/font_json/{self.font_family}.json', 'r') as f:
            glyph_data = json.load(f)
            return [
                glyph_data[letter]["glyph-path"] 
                for letter in self.text if letter in glyph_data
            ]


    def write(self) -> List[List[Polyline]]:
        word_list = []
        for index, letter_path in enumerate(self.path_list):
            path = parse_path(letter_path)
            output_list = []
            points = []
            allPoints = []

            for segment in path:
                segment_type = segment.__class__.__name__
                if segment_type == 'Move':
                    if len(points) > 0:
                        points = []
                        allPoints.append("M")
                    subpath_started = True
                elif subpath_started:
                    if segment_type == 'Line':
                        points.extend([(segment.start.real, segment.start.imag), (segment.end.real, segment.end.imag)])
                        allPoints.extend([(segment.start.real, segment.start.imag), (segment.end.real, segment.end.imag)])
                    elif segment_type == 'CubicBezier':
                        points.extend(segment.sample(10))
                        allPoints.extend(segment.sample(10))
                    elif segment_type == 'QuadraticBezier':
                        for i in range(11):
                            t = i / 10.0
                            point = segment.point(t)
                            points.append((point.real, point.imag))
                            allPoints.append((point.real, point.imag))
                    elif segment_type == 'Arc':
                        points.extend(segment.sample(10))
                        allPoints.extend(segment.sample(10))
            if points:
                output_list.append(self.convert_points_to_polyline(allPoints))
                if self.bounding_box == True and self.bounding_box != None:
                    output_list.append(self.calculate_bounding_box(allPoints)[0])
                width = self.calculate_bounding_box(allPoints)[1]

                self.x += width + self.character_offset
            word_list.append(output_list)
        return word_list


    def calculate_bounding_box(self, points):
        
        points = [elem for elem in points if elem != 'M']
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        ltX = self.x
        ltY = self.y + max_y - min_y

        lbX = self.x
        lbY = self.y + min_y - min_y

        rtX = self.x + max_x - min_x
        rtY = self.y + max_y - min_y

        rbX = self.x + max_x - min_x
        rbY = self.y + min_y - min_y
        
        left_top = SpecklePoint.from_coords(ltX, ltY, self.z)
        left_bottom = SpecklePoint.from_coords(lbX, lbY, self.z)
        right_top = SpecklePoint.from_coords(rtX, rtY, self.z)
        right_bottom = SpecklePoint.from_coords(rbX, rbY, self.z)

        bounding_box_polyline = self.rotate_polyline([left_top, right_top, right_bottom, left_bottom, left_top])

        char_width = rtX - ltX
        char_height = ltY - lbY
        return bounding_box_polyline, char_width, char_height


    def convert_points_to_polyline(self, points: list[tuple[float, float]]) -> Polyline: #move
        if self.rotation == None:
            self.rotation = 0

        output_list = []
        sub_lists = [[]]

        tempPoints = [elem for elem in points if elem != 'M']
        x_values = [point[0] for point in tempPoints]
        y_values = [point[1] for point in tempPoints]

        xmin = min(x_values)
        ymin = min(y_values)

        for item in points:

            if item == 'M':
                sub_lists.append([])
            else:
                x = item[0] + self.x - xmin
                y = item[1] + self.y - ymin
                z = self.z
                eput = x, y, z
                sub_lists[-1].append(eput)

        output_list = []

        for element in sub_lists:
            tmp = []
            for point in element:
                x = point[0]# + self.x
                y = point[1]# + self.y
                z = self.z
                tmp.append(SpecklePoint.from_coords(x,y,z))
            output_list.append(tmp)

        polyline_list = []
        for pts in output_list:
            print(pts)
            #self.rotate_polyline(Polyline.from_points(x)) 
            polyline_list.append(self.rotate_polyline(pts))
        return polyline_list


    def rotate_polyline(self, polylinePoints):

        translated_points = [(coord.x - self.originX, coord.y - self.originY) for coord in polylinePoints]

        # Rotate around the origin
        radians = math.radians(self.rotation)
        cos = math.cos(radians)
        sin = math.sin(radians)
        rotated_points = [
            (
                (x - self.originX) * cos - (y - self.originY) * sin + self.originZ,
                (x - self.originX) * sin + (y - self.originY) * cos + self.originZ
            ) for x, y in translated_points
        ]

        pts_list = []
        for x, y in rotated_points:
            pts_list.append(SpecklePoint.from_coords(x,y,self.z))

        return Polyline.from_points(pts_list)


p = Text(text="PyBuildingSystem1", font_family="arial", bounding_box=False, xyz=[0,0,0], rotation=90).write()
# p1 = Text(text="Maarten", font_family="arial", bounding_box=True, xyz=[0,0,0], rotation=0).write()
# p2 = Text(text="Piet", font_family="arial", bounding_box=False, xyz=[0,0,0], rotation=-90).write()
# p3 = Text(text="Joas", font_family="arial", bounding_box=True, xyz=[0,0,0], rotation=180).write()

# p4 = Text(text="Speckle", font_family="arial", bounding_box=False, xyz=[-1800,-1800,0], rotation=0).write()
# p5 = Text(text="12345678910", font_family="arial", bounding_box=False, xyz=[-7200,-7200,0], rotation=0).write()
# p6 = Text(text="abcdefghijklmnopqrstuvwxyz", font_family="arial", bounding_box=False, xyz=[-8900,-8900,0], rotation=0).write()

# p1 = Text(text="112", font_family="arial", bounding_box=True, xyz=[0,0,0], rotation=45).write()
# p2 = Text(text="112", font_family="arial", bounding_box=True, xyz=[0,0,0], rotation=-90).write()


obj = []
obj.append(p)
obj.append(Line)

SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "fa4e56aed4"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)