import sys, math, requests, json
from svg.path import parse_path
from typing import List, Tuple
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from exchange.speckle import TransportToSpeckle, translateObjectsToSpeckleObjects
from geometry.point import Point
from geometry.curve import PolyCurve


class Text:
    def __init__(self, text: str = None, font_family: str = None, bounding_box: bool = None, xyz: Point = None, rotation: float = None):
        self.text = text
        self.font_family = font_family or "arial"
        self.bounding_box = bounding_box
        self.originX, self.originY, self.originZ = xyz.x, xyz.y, xyz.z or (0, 0, 0)
        self.x, self.y, self.z = xyz.x, xyz.y, xyz.z or (0, 0, 0)
        self.rotation = rotation
        self.character_offset = 150
        self.space = 850
        self.path_list = self.load_path()
        self.f = []


    def load_path(self) -> List[str]:
        with open(f'library/text/json/{self.font_family}.json', 'r') as f:
            glyph_data = json.load(f)
            output = []
            for letter in self.text:
                if letter in glyph_data:
                    output.append(glyph_data[letter]["glyph-path"])
                elif letter == " ":
                    output.append("space")
            return output



    def write(self) -> List[List[PolyCurve]]:
        output_list = []
        for letter_path in self.path_list:
            points = []
            allPoints = []
            if letter_path == "space":
                self.x += self.space + self.character_offset
                pass
            else:
                path = parse_path(letter_path)
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
        return output_list

    def get_output(self) -> List[List[PolyCurve]]:
        return self.write()


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
        
        left_top = Point(ltX, ltY, self.z)
        left_bottom = Point(lbX, lbY, self.z)
        right_top = Point(rtX, rtY, self.z)
        right_bottom = Point(rbX, rbY, self.z)


        bounding_box_polyline = self.rotate_polyline([left_top, right_top, right_bottom, left_bottom, left_top])

        char_width = rtX - ltX
        char_height = ltY - lbY
        return bounding_box_polyline, char_width, char_height


    def convert_points_to_polyline(self, points: list[Point]) -> PolyCurve: #move
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
                x = point[0]
                y = point[1]
                z = self.z
                tmp.append(Point(x,y,z))
            output_list.append(tmp)

        polyline_list = []
        for pts in output_list:
            polyline_list.append(self.rotate_polyline(pts))
        return polyline_list


    def rotate_polyline(self, polylinePoints):
        translated_points = [(coord.x - self.originX, coord.y - self.originY) for coord in polylinePoints]
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
            pts_list.append(Point(x,y,self.z))

        return PolyCurve.byPoints(pts_list)
    

Text1 = Text(text="Hello world!", xyz=Point(20,10,20), rotation=0)

obj = [Text1]


SpeckleHost = "3bm.exchange"  # struct4u.xyz
StreamID = "a5de7fe769"  # c4cc12fa6f
SpeckleObjects = obj
Message = "Shiny commit 170"


SpeckleObj = translateObjectsToSpeckleObjects(obj)

Commit = TransportToSpeckle(SpeckleHost, StreamID, SpeckleObj, Message)