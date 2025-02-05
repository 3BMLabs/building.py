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


"""This module provides tools to create points."""

__title__ = "point"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/point.py"


import sys
from pathlib import Path
import math



from geometry.coords import Coords
from packages.helper import *

# [!not included in BP singlefile - end]

# from project.fileformat import project


class Point(Coords):
    """Represents a point in 3D space with x, y, and z coordinates."""
    def __init__(self, *args, **kwargs) -> 'Point':
        """Initializes a new Point instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the point.
        - `y` (float): Y-coordinate of the point.
        - `z` (float): Z-coordinate of the point.
        """
        super().__init__(*args, **kwargs)
        self.units = "mm"

    @staticmethod
    def distance_list(points: list['Point']) -> float:
        """Calculates distances between points in a list.
        
        #### Parameters:
        - `points` (list): List of points.

        #### Returns:
        `float`: Total distance calculated between all the points in the list.

        #### Example usage:
    	```python
        point_1 = Point(231, 13, 76)
        point_2 = Point(71, 12.3, -232)
        point_3 = Point(2, 71, -102)
        output = Point.distance_list([point_1, point_2, point_3])
        # [(<geometry.point.Point object at 0x00000226BD9CAB90>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 158.45090722365714), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 295.78539517697624), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BD9CAB90>, 347.07994756251765)]
        ```
        """
        distances = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                distances.append(
                    (points[i], points[j], Point.distance(points[i], points[j])))
        distances.sort(key=lambda x: x[2])
        return distances

    @staticmethod
    def origin(point_1: 'Point', point_2: 'Point') -> 'Point':
        """Computes the midpoint between two points.        
        
        #### Parameters:
        - `point_1` (Point): First point.
        - `point_2` (Point): Second point.
        
        #### Returns:
        `Point`: Midpoint between the two input points.

        #### Example usage:
    	```python
        point_1 = Point(100.23, 182, 19)
        point_2 = Point(81, 0.1, -901)
        output = Point.origin(point_1, point_2)
        # Point(X = 90.615, Y = 91.050, Z = -441.000)
        ```
        """
        return Point(
            (point_1.x + point_2.x) / 2,
            (point_1.y + point_2.y) / 2,
            (point_1.z + point_2.z) / 2
        )

    @staticmethod
    def rotate_XY(point: 'Point', beta: float, dz: float) -> 'Point':
        """Rotates the point about the Z-axis by a given angle.        
        
        #### Parameters:
        - `point` (Point): Point to be rotated.
        - `beta` (float): Angle of rotation in degrees.
        - `dz` (float): Offset in the z-coordinate.

        #### Returns:
        `Point`: Rotated point.

        #### Example usage:
    	```python
        point_1 = Point(19, 30, 12.3)
        output = Point.rotate_XY(point_1, 90, 12)
        # Point(X = -30.000, Y = 19.000, Z = 24.300)
        ```
        """
        return Point(
            math.cos(math.radians(beta))*point.x -
            math.sin(math.radians(beta))*point.y,
            math.sin(math.radians(beta))*point.x +
            math.cos(math.radians(beta))*point.y,
            point.z + dz
        )

    @staticmethod
    def intersect(point_1: 'Point', point_2: 'Point') -> 'bool':
        """Checks if two points intersect.        
        
        #### Parameters:
        - `point_1` (Point): First point.
        - `point_2` (Point): Second point.

        #### Returns:
        `boolean`: True if points intersect, False otherwise.

        #### Example usage:
    	```python
        point_1 = Point(23, 1, 23)
        point_2 = Point(93, 0, -19)
        output = Point.intersect(point_1, point_2)
        # False
        ```
        """
        return point_1.x == point_2.x and point_1.y == point_2.y and point_1.z == point_2.z

    @staticmethod
    def from_matrix(list: list) -> 'Point':
        """Converts a list to a Point object.        
        
        #### Parameters:
        Converts a list to a Point object.

        #### Returns:
        `Point`: Point object created from the list.

        #### Example usage:
    	```python
        point_1 = [19, 30, 12.3]
        output = Point.from_matrix(point_1)
        # Point(X = 19.000, Y = 30.000, Z = 12.300)
        ```
        """
        return Point(list)