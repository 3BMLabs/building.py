# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module provides tools for text"""

__title__ = "text"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/text.py"

# import requests
from typing import List
import json

from abstract.matrix import Matrix
from abstract.vector import Vector
from geometry.rect import Rect
from abstract.vector import Point


from geometry.curve import PolyCurve
from packages.svg.path import parse_path
from packages.helper import flatten
from packages.svg.path import CubicBezier, QuadraticBezier, Line, Arc

# [!not included in BP singlefile - end]

loaded_fonts = dict()


class Text:
    """The `Text` class is designed to represent and manipulate text within a coordinate system, allowing for the creation of text objects with specific fonts, sizes, and positions. It is capable of generating and translating text into a series of geometric representations."""

    def __init__(
        self, text: str = None, font_family = "Arial", cs=Matrix.identity(3), height=20
    ) -> "Text":
        """Initializes a new Text instance

        - `id` (str): A unique identifier for the text object.
        - `type` (str): The class name, "Text".
        - `text` (str, optional): The text string to be represented.
        - `font_family` (str, optional): The font family of the text, defaulting to "Arial".
        - `xyz` (Vector): The origin point of the text in the coordinate system.
        - `csglobal` (CoordinateSystem): The global coordinate system applied to the text.
        - `x`, `y`, `z` (float): The position offsets for the text within its coordinate system.
        - `scale` (float, optional): The scale factor applied to the text size.
        - `height` (float, optional): The height of the text characters.
        - `bbHeight` (float, optional): The bounding box height of the text.
        - `width` (float, optional): The calculated width of the text string.
        - `character_offset` (int): The offset between characters.
        - `space` (int): The space between words.
        - `curves` (list): A list of curves representing the text geometry.
        - `points` (list): A list of points derived from the text geometry.
        - `path_list` (list): A list containing the path data for each character.
        """

        self.text = text
        self.font_family = font_family
        self.xyz = cs.origin
        self.transform = cs
        self.x, self.y, self.z = 0, 0, 0
        self.scale = None
        self.height = height
        self.bbHeight = None
        self.width = None
        self.character_offset = 150
        self.space = 850
        self.curves = []
        # self.points = []
        self.path_list = self.load_path()

    def load_path(self) -> "str":
        """Loads the glyph paths for the specified text from a JSON file.
        This method fetches the glyph paths for each character in the text attribute, using a predefined font JSON file.

        #### Returns:
                str: A string representation of the glyph paths for the text.

        #### Example usage:
        ```python

        ```
        """
        file_name = "library/text/json/Calibri.json"
        if file_name not in loaded_fonts:
            with open(file_name, "r", encoding="utf-8") as file:
                loaded_fonts[file_name] = json.loads(file.read())
        glyph_data = loaded_fonts[file_name]
        output = []
        for letter in self.text:
            if letter in glyph_data:
                output.append(glyph_data[letter]["glyph-path"])
            elif letter == " ":
                output.append("space")

        letter = "o"
        if letter in glyph_data:
            self.load_o_example = [glyph_data[letter]["glyph-path"]]
        return output

    def write(self) -> "List[List[PolyCurve]]":
        """Generates a list of PolyCurve objects representing the text.
        Transforms the text into geometric representations based on the specified font, scale, and position.

        #### Returns:
                List[List[PolyCurve]]: A list of lists containing PolyCurve objects representing the text geometry.

        #### Example usage:
        ```python

        ```
        """
        # start ref_symbol
        path = self.load_o_example
        ref_points = []
        ref_allPoints = []
        for segment in path:
            pathx = parse_path(segment)
            for segment in pathx:
                segment_type = segment.__class__.__name__
                if isinstance(segment, Line):
                    ref_points.extend(
                        [
                            (segment.start.real, segment.start.imag),
                            (segment.end.real, segment.end.imag),
                        ]
                    )
                    ref_allPoints.extend(
                        [
                            (segment.start.real, segment.start.imag),
                            (segment.end.real, segment.end.imag),
                        ]
                    )
                elif isinstance(segment, CubicBezier):
                    ref_points.extend(segment.sample(10))
                    ref_allPoints.extend(segment.sample(10))
                elif isinstance(segment, QuadraticBezier):
                    for i in range(11):
                        t = i / 10.0
                        point = segment.point(t)
                        ref_points.append((point.real, point.imag))
                        ref_allPoints.append((point.real, point.imag))
                elif isinstance(segment, Arc):
                    ref_points.extend(segment.sample(10))
                    ref_allPoints.extend(segment.sample(10))
        height = self.calculate_bounding_box(ref_allPoints)[2]
        self.scale = self.height / height
        # end ref_symbol

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
                    if segment_type == "Move":
                        if len(points) > 0:
                            points = []
                            allPoints.append("M")
                        subpath_started = True
                    elif subpath_started:
                        if segment_type == "Line":
                            points.extend(
                                [
                                    (segment.start.real, segment.start.imag),
                                    (segment.end.real, segment.end.imag),
                                ]
                            )
                            allPoints.extend(
                                [
                                    (segment.start.real, segment.start.imag),
                                    (segment.end.real, segment.end.imag),
                                ]
                            )
                        elif segment_type == "CubicBezier":
                            points.extend(segment.sample(10))
                            allPoints.extend(segment.sample(10))
                        elif segment_type == "QuadraticBezier":
                            for i in range(11):
                                t = i / 10.0
                                point = segment.point(t)
                                points.append((point.real, point.imag))
                                allPoints.append((point.real, point.imag))
                        elif segment_type == "Arc":
                            points.extend(segment.sample(10))
                            allPoints.extend(segment.sample(10))
                if points:
                    output_list.append(self.convert_points_to_polyline(allPoints))
                    width = self.calculate_bounding_box(allPoints)[1]
                    self.x += width + self.character_offset

                height = self.calculate_bounding_box(allPoints)[2]
                self.bbHeight = height
        pList = []
        for ply in flatten(output_list):
            translated = self.translate(ply)
            pList.append(translated)

        # for pl in pList:
        # 	for pt in pl.points:
        # 		self.points.append(pt)

        # print(f'Object text naar objects gestuurd.')
        return pList

    def translate(self, polyCurve: "PolyCurve") -> "PolyCurve":
        """Translates a PolyCurve according to the text object's global coordinate system and scale.

        #### Parameters:
                polyCurve (PolyCurve): The PolyCurve to be translated.

        #### Returns:
                PolyCurve: The translated PolyCurve.

        #### Example usage:
        ```python

        ```
        """
        combined_matrix = self.transform * Matrix.scale(
            Vector(self.scale, self.scale, self.scale)
        )
        return combined_matrix * polyCurve

    def calculate_bounding_box(self, points: "list[Point]") -> tuple:
        """Calculates the bounding box for a given set of points.

        #### Parameters:
                points (list): A list of points to calculate the bounding box for.

        #### Returns:
                tuple: A tuple containing the bounding box, its width, and its height.

        #### Example usage:
        ```python

        ```
        """

        points = [elem for elem in points if elem != "M"]
        ptList = [Point(pt[0], pt[1]) for pt in points]
        bounding_box_polyline = Rect.by_points(ptList)
        return (
            bounding_box_polyline,
            bounding_box_polyline.width,
            bounding_box_polyline.length,
        )

    def convert_points_to_polyline(self, points: "list[Point]") -> "PolyCurve":
        """Converts a list of points into a PolyCurve.
        This method is used to generate a PolyCurve from a series of points, typically derived from text path data.

        #### Parameters:
                points (list): A list of points to be converted into a PolyCurve.

        #### Returns:
                PolyCurve: A PolyCurve object representing the points.

        #### Example usage:
        ```python

        ```
        """
        output_list = []
        sub_lists = [[]]
        tempPoints = [elem for elem in points if elem != "M"]
        x_values = [point[0] for point in tempPoints]
        y_values = [point[1] for point in tempPoints]

        xmin = min(x_values)
        ymin = min(y_values)

        for item in points:
            if item == "M":
                sub_lists.append([])
            else:
                x = item[0] + self.x - xmin
                y = item[1] + self.y - ymin
                z = self.xyz.z
                eput = x, y, z
                sub_lists[-1].append(eput)
        output_list = [
            [Point(point[0], point[1], self.xyz.z) for point in element]
            for element in sub_lists
        ]

        polyline_list = [
            PolyCurve.by_points([Point(coord.x, coord.y, self.xyz.z) for coord in pts])
            for pts in output_list
        ]
        return polyline_list
