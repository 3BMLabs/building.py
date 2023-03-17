import sys, random, math
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


#-1762845660


# Messie = SpeckleMesh(vertices = [0,0,0,1000,0,0,1000,1000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh") #, units = "mm"
# Messie2 = SpeckleMesh(vertices = [1000,1000,0,1000,1000,1000,2000,2000,0], faces = [3,0,1,2], name = "Jonathan zijn mesh", colors = [-1762845660,-1762845660,-1762845660]) #, units = "mm"

#    vert = [0, 0, 0, 1000, 0, 0, 1000, 2000, 0, 0, 1000, 0, 0, 2000, 2000, 3000, 2000, 1000]
# list structure of verts is x y z x y z x y z
#    faces = [3, 0, 1, 2, 3, 2, 3, 5]


# class Arc:
#     def __init__(self, startPoint: SpecklePoint, midPoint: SpecklePoint, endPoint: SpecklePoint):
#         self.startPoint = startPoint
#         self.midPoint = midPoint
#         self.endPoint = endPoint
#         self.plane = SpecklePlane(
#             origin=SpecklePoint.from_coords((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2),
#             normal=SpeckleVector.from_coords(0, 0, 1),
#             xdir=SpeckleVector.from_coords(1, 0, 0),
#             ydir=SpeckleVector.from_coords(0, 1, 0)
#         )
#         self.radius=self.radius()
#         self.startAngle=0
#         self.endAngle=0
#         self.angleRadians=0
#         self.area=0
#         self.length=self.length()
#         self.units="mm"

#     def distance(self, p1, p2):
#         return math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2 + (p2.z-p1.z)**2)
    
#     def radius(self):
#         a = self.distance(self.startPoint, self.midPoint)
#         b = self.distance(self.midPoint, self.endPoint)
#         c = self.distance(self.endPoint, self.startPoint)
#         s = (a + b + c) / 2
#         A = math.sqrt(s * (s-a) * (s-b) * (s-c))
#         R = (a * b * c) / (4 * A)
#         return R

#     def length(self):
#         x1, y1, z1 = self.startPoint.x, self.startPoint.y, self.startPoint.z
#         x2, y2, z2 = self.midPoint.x, self.midPoint.y, self.midPoint.z
#         x3, y3, z3 = self.endPoint.x, self.endPoint.y, self.endPoint.z

#         r1 = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5 / 2
#         a = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
#         b = math.sqrt((x3-x2)**2+(y3-y2)**2+(z3-z2)**2)
#         c = math.sqrt((x3-x1)**2+(y3-y1)**2+(z3-z1)**2)
#         cos_hoek = (a**2 + b**2 - c**2) / (2*a*b)
#         m1 = math.acos(cos_hoek)
#         arc_length = r1 * m1

#         return arc_length


#     @classmethod
#     def ByThreePoints(self, startPoint: SpecklePoint, midPoint: SpecklePoint, endPoint: SpecklePoint, plane=None):
#         radius = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).radius
#         startAngle = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).startAngle
#         endAngle = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).endAngle
#         angleRadians = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).angleRadians
#         area = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).area
#         length = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).length
#         units = self(startPoint=startPoint, midPoint=midPoint, endPoint=endPoint).units

#         if plane is None:
#             plane = SpecklePlane(
#                 origin=SpecklePoint.from_coords((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2, (startPoint.z + endPoint.z) / 2),
#                 normal=SpeckleVector.from_coords(0, 0, 1),
#                 xdir=SpeckleVector.from_coords(1, 0, 0),
#                 ydir=SpeckleVector.from_coords(0, 1, 0)
#             )
        
#         return SpeckleArc(
#             startPoint=startPoint,
#             midPoint=midPoint,
#             endPoint=endPoint,
#             domain=SpeckleInterval(start=0, end=1),
#             plane=plane,
#             radius=radius,
#             startAngle=startAngle,
#             endAngle=endAngle,
#             angleRadians=angleRadians,
#             area=area,
#             length=length,
#             units=units
#         )
    
#     def __id__(self):
#         return f"id:{self.id}"

#     def __str__(self) -> str:
#         return f"{__class__.__name__}({self})"


# p10=SpecklePoint.from_coords(10, 0, 0)
# p20=SpecklePoint.from_coords(500, 20, 0)
# p30=SpecklePoint.from_coords(1000, 0, 0)
# p = Arc.ByThreePoints(startPoint=p10,midPoint=p20,endPoint=p30)



from svg.path import parse_path
import json
from typing import List, Tuple

class Text:
    def __init__(self, text: str = None, font_family: str = None, bounding_box: bool = None, xyz: list[float, float, float] = None):
        #self.x_axis, self.y_axis, self.x = xyz
        self.bounding_box = bounding_box
        self.font_family = font_family
        self.text = text
        if xyz == None:
            self.x: float = 0
            self.y: float = 0
            self.z: float = 0
        else:
            self.x, self.y, self.z = xyz
        print(self.x)

        self.path = self.load_path()
        self.letter = self.write()
        
    def load_path(self) -> List[str]:
        with open(f'C:/Users/jonat/Desktop/font_json/{self.font_family}.json', 'r') as f:
            glyph_data = json.load(f)
            return [
                glyph_data[letter]["glyph-path"] 
                for letter in self.text if letter in glyph_data
            ]

    def write(self) -> List[List['Polyline']]:
        word_list = []
        if self.x is None:
            self.x = 0
        
        for letter_path in self.path:
            path = parse_path(letter_path)
            points = []
            output_list = []
            subpath_started = False

            for segment in path:
                segment_type = segment.__class__.__name__
                if segment_type == 'Move':
                    if len(points) > 0:
                        output_list.append(self.convert_points_to_polyline(points))
                        points = []
                    subpath_started = True
                elif subpath_started:
                    if segment_type == 'Line':
                        points.extend([(segment.start.real, segment.start.imag), (segment.end.real, segment.end.imag)])
                    elif segment_type == 'CubicBezier':
                        points.extend(segment.sample(10))
                    elif segment_type == 'QuadraticBezier':
                        for i in range(11):
                            t = i / 10.0
                            point = segment.point(t)
                            points.append((point.real, point.imag))
                    elif segment_type == 'Arc':
                        points.extend(segment.sample(10))

            if len(points) > 0:
                output_list.append(self.convert_points_to_polyline(points))
                output_list.append(self.calculate_to_bounding_box(points))
            word_list.append(output_list)
        return word_list


    def bounding_box(self, output_list: List['Polyline'], points: List[Tuple[float, float]]) -> None:
        output_list.append(self.calculate_to_bounding_box(points))


    def calculate_to_bounding_box(self, points: List[Tuple[float, float]]) -> 'Polyline':
        if self.x is None:
            self.x = 0
        if self.y is None:
            self.y = 0

        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]
        z_value = float(self.x)

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        left_top = SpecklePoint.from_coords(min_x + self.x, max_y + self.y, z_value)
        left_bottom = SpecklePoint.from_coords(min_x + self.x, min_y + self.y, z_value)
        right_top = SpecklePoint.from_coords(max_x + self.x, max_y + self.y, z_value)
        right_bottom = SpecklePoint.from_coords(max_x + self.x, min_y + self.y, z_value)

        boundingboxLine2d = Polyline.from_points([left_top, right_top, right_bottom, left_bottom, left_top])

        if self.bounding_box and self.bounding_box == 1:
            return boundingboxLine2d


    def convert_points_to_polyline(self, points: list[tuple[float, float]]) -> Polyline:
        if self.x == None:
            self.x = 0
        if self.y == None:
            self.y = 0

        output_list = [SpecklePoint.from_coords(point[0] + self.x, point[1] + self.y) for point in points]
        output_list.append(output_list[0])

        return Polyline.from_points(output_list)


p = Text(text="1234", font_family="arial", bounding_box=0).write()


print(p)

obj = []
obj.append(p)



# Text.write("Arial", "Jonathan", )
# Text("Arial", "Jonathan", ).write()
# Text("Arial", "Jonathan", ).boundingbox()


#obj.append(letterX.boundingbox())

# obj.append(letterX.boundingbox())

# obj.append(letterX.letter())


# obj.append(dollarX.letter())


SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "fa4e56aed4"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObjects, Message)


#TODO
#place on coordinates/plane
#scale
#vector
#width
