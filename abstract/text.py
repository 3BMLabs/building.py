# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides tools for text
"""

__title__= "text"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/text.py"


import sys, os, math
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from exchange.speckle import *

#implement these in /packages
from svg.path import parse_path
import json
from typing import List, Tuple

#change these to own geometry
from specklepy.objects.geometry import Point as SpecklePoint
from specklepy.objects.geometry import Polyline


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
        # self.f = []


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
        #THIS FUNCTION SHOULD BE STAND ALONE FUNCTION FOR ALL GEOMETRY IN THE FUTURE

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
        #TO BE REPLACED BY THE GENERIC PolyCurve.byPoints

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
        #TO BE REPLACED BY THE GENERIC GEOMETRY.TRANSLATE
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