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


"""
Represents a 3D vector with x, y, and z coordinates.
"""

__title__ = "vector"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/vector.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import *
from packages.helper import *
from geometry.coords import Coords

# [!not included in BP singlefile - end]


class Vector(Coords):
    """Represents a 3D vector with x, y, and z coordinates."""
    def __init__(self, *args, **kwargs) -> 'Vector':
        """Initializes a new Vector instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the vector.
        - `y` (float): Y-coordinate of the vector.
        - `z` (float): Z-coordinate of the vector.
        """
        super().__init__(*args, **kwargs)
        self.type = __class__.__name__

    @staticmethod
    def square(vector_1: 'Vector') -> 'Vector':
        """
        Computes the square of each component of the input vector.

        #### Parameters:
        - `vector_1` (`Vector`): The input vector.

        #### Returns:
        `Vector`: A new Vector object representing the square of each component of the input vector.

        #### Example usage:
        ```python
        vector = Vector(2, 3, 4)
        squared_vector = Vector.square(vector)
        # Vector(X = 4, Y = 9, Z = 16)
        ```
        """
        return Vector(
            vector_1.x ** 2,
            vector_1.y ** 2,
            vector_1.z ** 2
        )

    @staticmethod
    def to_line(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
        """Creates a Line object from two vectors.

        #### Parameters:
        - `vector_1` (`Vector`): The start vector of the line.
        - `vector_2` (`Vector`): The end vector of the line.

        #### Returns:
        `Line`: A Line object connecting the two vectors.

        #### Example usage:
        ```python
        vector1 = Vector(10, 20, 30)
        vector2 = Vector(2, 4, 5)
        line = Vector.to_line(vector1, vector2)
        # Line(start=Point(X = 10.000, Y = 20.000, Z = 30.000), end=Point(X = 2.000, Y = 4.000, Z = 5.000))
        ```
        """
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start=Point(x=vector_1.x, y=vector_1.y, z=vector_1.z), end=Point(x=vector_2.x, y=vector_2.y, z=vector_2.z))

    @staticmethod
    def by_line(line_1) -> 'Vector':
        """Computes a vector representing the direction of a given line.
        This method takes a Line object and returns a Vector representing the direction of the line.

        #### Parameters:
        - `line_1` (`Line`): The Line object from which to extract the direction.

        #### Returns:
        `Vector`: A Vector representing the direction of the line.

        #### Example usage:
        ```python
        line = Line(start=Point(0, 0, 0), end=Point(1, 1, 1))
        direction_vector = Vector.by_line(line)
        # Vector(X = 1, Y = 1, Z = 1)
        ```
        """
        return Vector(line_1.dx, line_1.dy, line_1.dz)

    @staticmethod
    def cross_product(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
        """Computes the cross product of two vectors.
        The cross product of two vectors in three-dimensional space is a vector that is perpendicular to both original vectors. It is used to find a vector that is normal to a plane defined by the input vectors.

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `Vector`: A new Vector object representing the cross product of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        vector2 = Vector(4, 5, 6)
        cross_product = Vector.cross_product(vector1, vector2)
        # Vector(X = -3, Y = 6, Z = -3)
        ```
        """
        return Vector(
            vector_1.y*vector_2.z - vector_1.z*vector_2.y,
            vector_1.z*vector_2.x - vector_1.x*vector_2.z,
            vector_1.x*vector_2.y - vector_1.y*vector_2.x
        )

    @staticmethod
    def dot_product(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
        """Computes the dot product of two vectors.
        The dot product of two vectors is a scalar quantity equal to the sum of the products of their corresponding components. It gives insight into the angle between the vectors.

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The dot product of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        vector2 = Vector(4, 5, 6)
        dot_product = Vector.dot_product(vector1, vector2)
        # 32
        ```
        """
        return vector_1.x*vector_2.x+vector_1.y*vector_2.y+vector_1.z*vector_2.z

    @staticmethod
    def product(number: float, vector_1: 'Vector') -> 'Vector':
        """Scales a vector by a scalar value.
        This method multiplies each component of the vector by the given scalar value.

        #### Parameters:
        - `number` (float): The scalar value to scale the vector by.
        - `vector_1` (`Vector`): The vector to be scaled.

        #### Returns:
        `Vector`: A new Vector object representing the scaled vector.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        scaled_vector = Vector.product(2, vector1)
        # Vector(X = 2, Y = 4, Z = 6)
        ```
        """
        return Vector(
            vector_1.x*number,
            vector_1.y*number,
            vector_1.z*number
        )

    @staticmethod
    def length(vector_1: 'Vector') -> float:
        """Computes the length (magnitude) of a vector.
        The length of a vector is the Euclidean norm or magnitude of the vector, which is calculated as the square root of the sum of the squares of its components.

        #### Parameters:
        - `vector_1` (`Vector`): The vector whose length is to be computed.

        #### Returns:
        `float`: The length of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        length = Vector.length(vector1)
        # 3.7416573867739413
        ```
        """
        return math.sqrt(vector_1.x*vector_1.x+vector_1.y*vector_1.y+vector_1.z*vector_1.z)

    @staticmethod
    def pitch(vector_1: 'Vector', angle: float) -> 'Vector':
        """Rotates a vector around the X-axis (pitch).
        This method rotates the vector around the X-axis (pitch) by the specified angle.

        #### Parameters:
        - `vector_1` (`Vector`): The vector to be rotated.
        - `angle` (float): The angle of rotation in radians.

        #### Returns:
        `Vector`: A new Vector object representing the rotated vector.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        rotated_vector = Vector.pitch(vector1, math.pi/2)
        # Vector(X = 1.000, Y = -3.000, Z = 2.000)
        ```
        """
        return Vector(
            vector_1.x,
            vector_1.y*math.cos(angle) - vector_1.z*math.sin(angle),
            vector_1.y*math.sin(angle) + vector_1.z*math.cos(angle)
        )

    @staticmethod
    def angle_between(vector_1: 'Vector', vector_2: 'Vector') -> float:
        """Computes the angle in degrees between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in degrees.

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        angle = Vector.angle_between(vector1, vector2)
        # 90
        ```
        """
        proj_vector_1 = Vector.to_matrix(vector_1)
        proj_vector_2 = Vector.to_matrix(vector_2)
        dot_product = Vector.dot_product(vector_1, vector_2)
        length_vector_1 = Vector.length(vector_1)
        length_vector_2 = Vector.length(vector_2)

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_radian_between(vector_1: 'Vector', vector_2: 'Vector') -> float:
        """Computes the angle in radians between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in radians.

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in radians between the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector(1, 0, 0)
        vector2 = Vector(0, 1, 0)
        angle = Vector.angle_radian_between(vector1, vector2)
        # 1.5707963267948966
        ```
        """
        return math.acos((Vector.dot_product(vector_1, vector_2)/(Vector.length(vector_1)*Vector.length(vector_2))))

    @staticmethod
    def angle_between_YZ(vector_1: 'Vector', vector_2: 'Vector') -> float:
        """Computes the angle in degrees between two vectors projected onto the YZ plane (X-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the YZ plane (X-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector(1, 1, 0)
        vector2 = Vector(1, 0, 1)
        angle = Vector.angle_between_YZ(vector1, vector2)
        # 90
        ```
        """
        dot_product = Vector.dot_product(vector_1, vector_2)
        length_vector_1 = Vector.length(Vector(0, vector_1.y, vector_1.z))
        length_vector_2 = Vector.length(Vector(0, vector_2.y, vector_2.z))
        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_between_XZ(vector_1: 'Vector', vector_2: 'Vector') -> float:
        """Computes the angle in degrees between two vectors projected onto the XZ plane (Y-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the XZ plane (Y-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector(1, 0, 1)
        vector2 = Vector(0, 1, 1)
        angle = Vector.angle_between_XZ(vector1, vector2)
        # 90
        ```
        """
        dot_product = Vector.dot_product(vector_1, vector_2)
        length_vector_1 = Vector.length(Vector(vector_1.x, 0, vector_1.z))
        length_vector_2 = Vector.length(Vector(vector_2.x, 0, vector_2.z))

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_between_XY(vector_1: 'Vector', vector_2: 'Vector') -> float:
        """Computes the angle in degrees between two vectors projected onto the XY plane (Z-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector`): The first vector.
        - `vector_2` (`Vector`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the XY plane (Z-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector(1, 0, 1)
        vector2 = Vector(0, 1, 1)
        angle = Vector.angle_between_XY(vector1, vector2)
        # 45
        ```
        """
        dot_product = Vector.dot_product(vector_1, vector_2)
        length_vector_1 = Vector.length(Vector(vector_1.x, vector_1.y, 0))
        length_vector_2 = Vector.length(Vector(vector_2.x, vector_2.y, 0))

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def value(vector_1: 'Vector') -> tuple:
        """Returns the rounded values of the vector's components.

        #### Parameters:
        - `vector_1` (`Vector`): The vector.

        #### Returns:
        `tuple`: A tuple containing the rounded values of the vector's components.

        #### Example usage:
        ```python
        vector1 = Vector(1.123456, 2.345678, 3.987654)
        rounded_values = Vector.value(vector1)
        # (1.1235, 2.3457, 3.9877)
        ```
        """
        roundValue = 4
        return (round(vector_1.x, roundValue), round(vector_1.y, roundValue), round(vector_1.z, roundValue))

    @staticmethod
    def reverse(vector_1: 'Vector') -> 'Vector':
        """Returns the reverse (negation) of the vector.

        #### Parameters:
        - `vector_1` (`Vector`): The vector.

        #### Returns:
        `Vector`: The reverse (negation) of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        reversed_vector = Vector.reverse(vector1)
        # Vector(X = -1, Y = -2, Z = -3)
        ```
        """
        return Vector(
            vector_1.x*-1,
            vector_1.y*-1,
            vector_1.z*-1
        )

    @staticmethod
    def perpendicular(vector_1: 'Vector') -> tuple:
        """Computes two vectors perpendicular to the input vector.

        #### Parameters:
        - `vector_1` (`Vector`): The input vector.

        #### Returns:
        `tuple`: A tuple containing two vectors perpendicular to the input vector.

        #### Example usage:
        ```python
        vector1 = Vector(1, 2, 3)
        perpendicular_vectors = Vector.perpendicular(vector1)
        # (Vector(X = 2, Y = -1, Z = 0), Vector(X = -3, Y = 0, Z = 1))
        ```
        """
        lokX = Vector(vector_1.y, -vector_1.x, 0)
        lokZ = Vector.cross_product(vector_1, lokX)
        if lokZ.z < 0:
            lokZ = Vector.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def by_two_points(point_1: 'Point', point_2: 'Point') -> 'Vector':
        """Computes the vector between two points.

        #### Parameters:
        - `point_1` (`Point`): The starting point.
        - `point_2` (`Point`): The ending point.

        #### Returns:
        `Vector`: A new Vector object representing the vector between the two points.

        #### Example usage:
        ```python
        point1 = Point(1, 2, 3)
        point2 = Point(4, 6, 8)
        vector = Vector.by_two_points(point1, point2)
        # Vector(X = 3, Y = 4, Z = 5)
        ```
        """
        return Vector(
            point_2.x-point_1.x,
            point_2.y-point_1.y,
            point_2.z-point_1.z
        )

    @staticmethod
    def rotate_XY(vector: 'Vector', Beta: float) -> 'Vector':
        """Rotates the vector in the XY plane by the specified angle.

        #### Parameters:
        - `vector` (`Vector`): The vector to be rotated.
        - `Beta` (float): The angle of rotation in radians.

        #### Returns:
        `Vector`: A new Vector object representing the rotated vector.

        #### Example usage:
        ```python
        vector = Vector(1, 0, 0)
        rotated_vector = Vector.rotate_XY(vector, math.pi/2)
        # Vector(X = 0, Y = 1, Z = 0)
        ```
        """
        return Vector(
            math.cos(Beta)*vector.x - math.sin(Beta)*vector.y,
            math.sin(Beta)*vector.x + math.cos(Beta)*vector.y,
            vector.z
        )

    @staticmethod
    def to_matrix(vector: 'Vector') -> list:
        """Converts the vector to a list representation.

        #### Parameters:
        - `vector` (`Vector`): The vector to be converted.

        #### Returns:
        `list`: A list representation of the vector.

        #### Example usage:
        ```python
        vector = Vector(1, 2, 3)
        vector_list = Vector.to_matrix(vector)
        # [1, 2, 3]
        ```
        """
        return [vector.x, vector.y, vector.z]

    @staticmethod
    def from_matrix(vector_list: list) -> 'Vector':
        """Creates a Vector object from a list representation.

        #### Parameters:
        - `vector_list` (list): The list representing the vector.

        #### Returns:
        `Vector`: A Vector object created from the list representation.

        #### Example usage:
        ```python
        vector_list = [1, 2, 3]
        vector = Vector.from_matrix(vector_list)
        # Vector(X = 1, Y = 2, Z = 3)
        ```
        """
        return Vector(
            vector_list[0],
            vector_list[1],
            vector_list[2]
        )