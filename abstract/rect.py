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


"""This module provides tools for boundingbox
"""

__title__ = "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/boundingbox.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.coords import Coords
from packages.helper import *
from geometry.solid import Extrusion
from abstract.vector import Vector
from abstract.coordinatesystem import CoordinateSystem, CSGlobal
from geometry.curve import PolyCurve, Line
from geometry.point import Point
from geometry.geometry2d import Point2D, PolyCurve2D
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]

class Rect(Serializable):
    """Represents a two-dimensional bounding box."""
    def __init__(self, p0: Coords, size: Coords):
        self.id = generateID()
        self.type = __class__.__name__
        self.points = []
        self.corners = []
        self.isClosed = True
        self.z = 0
        self.p0 = p0
        self.size = size
        
    @property
    def length(self):
        return self.size.y
    @length.setter
    def length(self, value):
        self.size.y = value
    
    @property
    def width(self):
        return self.size.x
    @width.setter
    def width(self, value):
        self.size.x = value
        
    def area(self):
        return self.size.volume()
    
    def __str__(self):
        return __class__.__name__ + '(p0=' + str(self.p0)+',size=' + str(self.size) + ')'
    def __repr__(self):
        return str(self)

    def by_points(self, points: list[Point]) -> 'Rect':
        """Constructs a 2D bounding box based on a list of points.

        Calculates the minimum and maximum x and y values from the points to define the corners of the bounding box.

        #### Parameters:
        - `points` (list[Point]): A list of Point objects to calculate the bounding box from.

        #### Returns:
        `Rect`: The bounding box instance with updated corners based on the provided points.

        #### Example usage:
        ```python
        points = [Point(0, 0, 0), Point(2, 2, 0), Point(2, 0, 0), Point(0, 2, 0)]
        bbox = Rect().by_points(points)
        # Rect with corners at (0, 0, 0), (2, 2, 0), (2, 0, 0), and (0, 2, 0)
        ```
        """

        self.points = points
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        left_top = Point(x=min_x, y=max_y, z=self.z)
        left_bottom = Point(x=min_x, y=min_y, z=self.z)
        right_top = Point(x=max_x, y=max_y, z=self.z)
        right_bottom = Point(x=max_x, y=min_y, z=self.z)
        self.length = abs(Point.distance(left_top, left_bottom))
        self.width = abs(Point.distance(left_top, right_top))
        self.corners.append(left_top)
        self.corners.append(left_bottom)
        self.corners.append(right_bottom)
        self.corners.append(right_top)
        return self

    def by_dimensions(self, length: float, width: float) -> 'Rect':
        """Constructs a 2D bounding box with specified dimensions, centered at the origin.

        #### Parameters:
        - `length` (float): The length of the bounding box.
        - `width` (float): The width of the bounding box.

        #### Returns:
        `Rect`: The bounding box instance with dimensions centered at the origin.

        #### Example usage:
        ```python
        bbox = Rect().by_dimensions(length=100, width=50)
        # Rect centered at origin with specified length and width
        ```
        """

        # startpoint = Point2D(0,0)
        # widthpoint = Point2D(0,width)
        # widthlengthpoint = Point2D(length,width)
        # lengthpoint = Point2D(length,0)

        half_length = length / 2
        half_width = width / 2

        startpoint = Point2D(-half_length, -half_width)
        widthpoint = Point2D(-half_length, half_width)
        widthlengthpoint = Point2D(half_length, half_width)
        lengthpoint = Point2D(half_length, -half_width)

        self.points.append(startpoint)
        self.corners.append(startpoint)
        self.points.append(widthpoint)
        self.corners.append(widthpoint)
        self.points.append(widthlengthpoint)
        self.corners.append(widthlengthpoint)
        self.points.append(lengthpoint)
        self.corners.append(lengthpoint)

        self.length = length
        self.width = width
        return self


class BoundingBox3d:
    def __init__(self, points=Point):
        self.id = generateID()
        self.type = __class__.__name__
        self.points = points
        self.Rect = None
        self.coordinatesystem = None
        self.height = None

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'points': [point.serialize() for point in self.points]
        }

    @staticmethod
    def deserialize(data):
        points = [Point.deserialize(point_data)
                  for point_data in data.get('points', [])]
        return BoundingBox3d(points)

    def corners(self) -> 'list[Point]':
        """Calculates the eight corners of the 3D bounding box based on the contained points.

        #### Returns:
        `list[Point]`: A list of eight Point objects representing the corners of the bounding box.

        #### Example usage:
        ```python
        bbox3d = BoundingBox3d(points=[Point(1, 1, 1), Point(2, 2, 2)])
        corners = bbox3d.corners()
        # Returns a list of eight points representing the corners of the bounding box
        ```
        """

        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        min_z = min(z_values)
        max_z = max(z_values)

        left_top_bottom = Point(x=min_x, y=max_y, z=min_z)
        left_bottom_bottom = Point(x=min_x, y=min_y, z=min_z)
        right_top_bottom = Point(x=max_x, y=max_y, z=min_z)
        right_bottom_bottom = Point(x=max_x, y=min_y, z=min_z)

        left_top_top = Point(x=min_x, y=max_y, z=max_z)
        left_bottom_top = Point(x=min_x, y=min_y, z=max_z)
        right_top_top = Point(x=max_x, y=max_y, z=max_z)
        right_bottom_top = Point(x=max_x, y=min_y, z=max_z)

        return [left_top_bottom, left_top_top, right_top_top, right_top_bottom, left_top_bottom, left_bottom_bottom, left_bottom_top, left_top_top, left_bottom_top, right_bottom_top, right_bottom_bottom, left_bottom_bottom, right_bottom_bottom, right_top_bottom, right_top_top, right_bottom_top]

    def perimeter(self):
        return PolyCurve.by_points(self.corners(self.points))

    def convert_boundingbox_2d(self, Rect: 'Rect', coordinatesystem: 'CoordinateSystem', height: 'float') -> 'BoundingBox3d':
        """Converts a 2D bounding box into a 3D bounding box using a specified coordinate system and height.

        #### Parameters:
        - `Rect` (Rect): The 2D bounding box to be converted.
        - `coordinatesystem` (CoordinateSystem): The coordinate system for the 3D bounding box.
        - `height` (float): The height of the 3D bounding box.

        #### Returns:
        `BoundingBox3d`: The instance itself, now representing a 3D bounding box.

        #### Example usage:
        ```python
        bbox2d = Rect().by_dimensions(length=100, width=50)
        cs = CoordinateSystem()
        bbox3d = BoundingBox3d().convert_boundingbox_2d(bbox2d, cs, height=30)
        # Converts bbox2d into a 3D bounding box with a specified height and coordinate system
        ```
        """
        self.Rect = Rect
        self.coordinatesystem = coordinatesystem
        self.height = height
        return self

    def to_cuboid(self) -> 'Extrusion':
        """Generates an extrusion representing a cuboid from the 3D bounding box dimensions.

        #### Returns:
        `Extrusion`: An Extrusion object that represents a cuboid, matching the dimensions and orientation of the bounding box.

        #### Example usage:
        ```python
        bbox2d = Rect().by_dimensions(length=100, width=50)
        cs = CoordinateSystem()
        bbox3d = BoundingBox3d().convert_boundingbox_2d(bbox2d, cs, height=30)
        cuboid = bbox3d.to_cuboid()
        # Generates a cuboid extrusion based on the 3D bounding box
        ```
        """
        pts = self.Rect.corners
        pc = PolyCurve2D.by_points(pts)
        height = self.height
        cs = self.coordinatesystem
        dirXvector = Vector.angle_between(CSGlobal.Y_axis, cs.Y_axis)
        pcrot = pc.rotate(dirXvector)  # bug multi direction
        cuboid = Extrusion.by_polycurve_height_vector(
            pcrot, height, CSGlobal, cs.Origin, cs.Z_axis)
        return cuboid

    def to_axis(self, length: 'float' = 1000) -> 'list':
        """Generates lines representing the coordinate axes of the bounding box's coordinate system.

        This method creates three Line objects corresponding to the X, Y, and Z axes of the bounding box's coordinate system. Each line extends from the origin of the coordinate system in the direction of the respective axis.

        #### Parameters:
        - `length` (float, optional): The length of each axis line. Defaults to 1000 units.

        #### Returns:
        `list`: A list containing three Line objects representing the X, Y, and Z axes.

        #### Example usage:
        ```python
        # Assuming `bbox3d` is an instance of BoundingBox3d with a defined coordinate system
        axes_lines = bbox3d.to_axis(length=500)
        # This returns a list of three Line objects representing the X, Y, and Z axes of the bounding box's coordinate system, each 500 units long.
        ```
        """
        if length == None:
            length = 1000
        cs = self.coordinatesystem
        lnX = Line.by_startpoint_direction_length(cs.Origin, cs.X_axis, length)
        lnY = Line.by_startpoint_direction_length(cs.Origin, cs.Y_axis, length)
        lnZ = Line.by_startpoint_direction_length(cs.Origin, cs.Z_axis, length)
        return [lnX, lnY, lnZ]
