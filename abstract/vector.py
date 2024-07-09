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


class Vector3(Coords):
    """Represents a 3D vector with x, y, and z coordinates."""
    def __init__(self, x: float, y: float, z: float) -> 'Vector3':
        """Initializes a new Vector3 instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the vector.
        - `y` (float): Y-coordinate of the vector.
        - `z` (float): Z-coordinate of the vector.
        """
        super().__init__(x, y, z)
        self.type = __class__.__name__

    @staticmethod
    def deserialize(data):
        """Converts a dictionary representation of a vector into a Vector3 object.
        This method takes a dictionary containing 'x', 'y', and 'z' keys with numeric values and creates a new Vector3 instance representing the vector described by these values. It's particularly useful for converting serialized vector data back into Vector3 objects, for instance, when loading vectors from a file or a database.

        #### Parameters:
        - `data` (dict): A dictionary with keys 'x', 'y', and 'z', corresponding to the components of the vector. Each key's value should be a number (int or float).

        #### Returns:
        Vector3: A new Vector3 object initialized with the x, y, and z values from the input dictionary.

        #### Example usage:
        ```python
        data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
        vector = Vector3.deserialize(data)
        # Vector3 object with x=1.0, y=2.0, z=3.0
        ```
        """
        return Vector3(data['x'], data['y'], data['z'])

    @staticmethod
    def sum(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Adds two vectors element-wise.        
        
        #### Parameters:
        - `vector_1` (Vector3): First vector.
        - `vector_2` (Vector3): Second vector.

        Returns:
        `Vector3`: Sum of the two input vectors.

        #### Example usage:

        ```python
        vector_1 = Vector3(19, 18, 17)
        vector_2 = Vector3(8, 17, 1)
        output = Vector3.sum(vector_1, vector_2)
        # Vector3(X = 27.000, Y = 35.000, Z = 18.000)
        ```
        """
        return Vector3(
            vector_1.x + vector_2.x,
            vector_1.y + vector_2.y,
            vector_1.z + vector_2.z
        )

    @staticmethod
    def sum3(vector_1: 'Vector3', vector_2: 'Vector3', vector_3: 'Vector3') -> 'Vector3':
        """Calculates the sum of three Vector3 objects.
        This method returns a new Vector3 object whose components are the sum of the corresponding components of the three input vectors.

        #### Parameters:
        - `vector_1`, `vector_2`, `vector_3` (`Vector3`): The vectors to be summed.

        #### Returns:
        `Vector3`: A new Vector3 object resulting from the component-wise sum of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        vector2 = Vector3(4, 5, 6)
        vector3 = Vector3(-1, -2, -3)
        result = Vector3.sum3(vector1, vector2, vector3)
        # Vector3(X = 4.000, Y = 5.000, Z = 6.000)
        ```
        """
        return Vector3(
            vector_1.x + vector_2.x + vector_3.x,
            vector_1.y + vector_2.y + vector_3.y,
            vector_1.z + vector_2.z + vector_3.z
        )

    @staticmethod
    def diff(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Calculates the difference between two Vector3 objects.
        This method returns a new Vector3 object that is the result of subtracting the components of `vector_2` from `vector_1`.

        #### Parameters:
        - `vector_1` (`Vector3`): The minuend vector.
        - `vector_2` (`Vector3`): The subtrahend vector.

        #### Returns:
        `Vector3`: A new Vector3 object resulting from the component-wise subtraction of `vector_2` from `vector_1`.

        #### Example usage:
        ```python
        vector1 = Vector3(5, 7, 9)
        vector2 = Vector3(1, 2, 3)
        result = Vector3.diff(vector1, vector2)
        # Vector3(X = 4.000, Y = 5.000, Z = 6.000)
        ```
        """
        return Vector3(
            vector_1.x - vector_2.x,
            vector_1.y - vector_2.y,
            vector_1.z - vector_2.z
        )

    @staticmethod
    def subtract(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Subtracts the components of the second vector from the first.
        This method is synonymous with `diff` and serves the same purpose, providing an alternative naming convention.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector from which to subtract.
        - `vector_2` (`Vector3`): The vector to be subtracted.

        #### Returns:
        `Vector3`: The result of the component-wise subtraction.

        #### Example usage:
        ```python
        vector1 = Vector3(10, 20, 30)
        vector2 = Vector3(1, 2, 3)
        result = Vector3.subtract(vector1, vector2)
        # Vector3(X = 9.000, Y = 18.000, Z = 27.000)
        ```
        """
        return Vector3(
            vector_1.x - vector_2.x,
            vector_1.y - vector_2.y,
            vector_1.z - vector_2.z
        )

    @staticmethod
    def divide(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Divides the components of the first vector by the corresponding components of the second vector.
        This method performs component-wise division. If any component of `vector_2` is 0, the result for that component will be undefined.

        #### Parameters:
        - `vector_1` (`Vector3`): The numerator vector.
        - `vector_2` (`Vector3`): The denominator vector.

        #### Returns:
        `Vector3`: A new Vector3 object resulting from the component-wise division.

        #### Example usage:
        ```python
        vector1 = Vector3(10, 20, 30)
        vector2 = Vector3(2, 4, 5)
        result = Vector3.divide(vector1, vector2)
        # Vector3(X = 5.000, Y = 5.000, Z = 6.000)
        ```
        """
        return Vector3(
            vector_1.x / vector_2.x,
            vector_1.y / vector_2.y,
            vector_1.z / vector_2.z
        )

    @staticmethod
    def square(vector_1: 'Vector3') -> 'Vector3':
        """
        Computes the square of each component of the input vector.

        #### Parameters:
        - `vector_1` (`Vector3`): The input vector.

        #### Returns:
        `Vector3`: A new Vector3 object representing the square of each component of the input vector.

        #### Example usage:
        ```python
        vector = Vector3(2, 3, 4)
        squared_vector = Vector3.square(vector)
        # Vector3(X = 4, Y = 9, Z = 16)
        ```
        """
        return Vector3(
            vector_1.x ** 2,
            vector_1.y ** 2,
            vector_1.z ** 2
        )

    @staticmethod
    def to_point(vector_1: 'Vector3') -> 'Vector3':
        """Converts the vector to a Point object.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector to be converted to a Point object.

        #### Returns:
        `Point`: A Point object with coordinates same as the vector.

        #### Example usage:
        ```python
        vector1 = Vector3(10, 20, 30)
        point = Vector3.to_point(vector1)
        # Point(X = 10.000, Y = 20.000, Z = 30.000)
        ```
        """
        from geometry.point import Point
        return Point(x=vector_1.x, y=vector_1.y, z=vector_1.z)

    @staticmethod
    def to_line(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Creates a Line object from two vectors.

        #### Parameters:
        - `vector_1` (`Vector3`): The start vector of the line.
        - `vector_2` (`Vector3`): The end vector of the line.

        #### Returns:
        `Line`: A Line object connecting the two vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(10, 20, 30)
        vector2 = Vector3(2, 4, 5)
        line = Vector3.to_line(vector1, vector2)
        # Line(start=Point(X = 10.000, Y = 20.000, Z = 30.000), end=Point(X = 2.000, Y = 4.000, Z = 5.000))
        ```
        """
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start=Point(x=vector_1.x, y=vector_1.y, z=vector_1.z), end=Point(x=vector_2.x, y=vector_2.y, z=vector_2.z))

    @staticmethod
    def by_line(line_1) -> 'Vector3':
        """Computes a vector representing the direction of a given line.
        This method takes a Line object and returns a Vector3 representing the direction of the line.

        #### Parameters:
        - `line_1` (`Line`): The Line object from which to extract the direction.

        #### Returns:
        `Vector3`: A Vector3 representing the direction of the line.

        #### Example usage:
        ```python
        line = Line(start=Point(0, 0, 0), end=Point(1, 1, 1))
        direction_vector = Vector3.by_line(line)
        # Vector3(X = 1, Y = 1, Z = 1)
        ```
        """
        return Vector3(line_1.dx, line_1.dy, line_1.dz)

    @staticmethod
    def cross_product(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Computes the cross product of two vectors.
        The cross product of two vectors in three-dimensional space is a vector that is perpendicular to both original vectors. It is used to find a vector that is normal to a plane defined by the input vectors.

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `Vector3`: A new Vector3 object representing the cross product of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        vector2 = Vector3(4, 5, 6)
        cross_product = Vector3.cross_product(vector1, vector2)
        # Vector3(X = -3, Y = 6, Z = -3)
        ```
        """
        return Vector3(
            vector_1.y*vector_2.z - vector_1.z*vector_2.y,
            vector_1.z*vector_2.x - vector_1.x*vector_2.z,
            vector_1.x*vector_2.y - vector_1.y*vector_2.x
        )

    @staticmethod
    def dot_product(vector_1: 'Vector3', vector_2: 'Vector3') -> 'Vector3':
        """Computes the dot product of two vectors.
        The dot product of two vectors is a scalar quantity equal to the sum of the products of their corresponding components. It gives insight into the angle between the vectors.

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The dot product of the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        vector2 = Vector3(4, 5, 6)
        dot_product = Vector3.dot_product(vector1, vector2)
        # 32
        ```
        """
        return vector_1.x*vector_2.x+vector_1.y*vector_2.y+vector_1.z*vector_2.z

    @staticmethod
    def product(number: float, vector_1: 'Vector3') -> 'Vector3':
        """Scales a vector by a scalar value.
        This method multiplies each component of the vector by the given scalar value.

        #### Parameters:
        - `number` (float): The scalar value to scale the vector by.
        - `vector_1` (`Vector3`): The vector to be scaled.

        #### Returns:
        `Vector3`: A new Vector3 object representing the scaled vector.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        scaled_vector = Vector3.product(2, vector1)
        # Vector3(X = 2, Y = 4, Z = 6)
        ```
        """
        return Vector3(
            vector_1.x*number,
            vector_1.y*number,
            vector_1.z*number
        )

    @staticmethod
    def length(vector_1: 'Vector3') -> float:
        """Computes the length (magnitude) of a vector.
        The length of a vector is the Euclidean norm or magnitude of the vector, which is calculated as the square root of the sum of the squares of its components.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector whose length is to be computed.

        #### Returns:
        `float`: The length of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        length = Vector3.length(vector1)
        # 3.7416573867739413
        ```
        """
        return math.sqrt(vector_1.x*vector_1.x+vector_1.y*vector_1.y+vector_1.z*vector_1.z)

    @staticmethod
    def pitch(vector_1: 'Vector3', angle: float) -> 'Vector3':
        """Rotates a vector around the X-axis (pitch).
        This method rotates the vector around the X-axis (pitch) by the specified angle.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector to be rotated.
        - `angle` (float): The angle of rotation in radians.

        #### Returns:
        `Vector3`: A new Vector3 object representing the rotated vector.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        rotated_vector = Vector3.pitch(vector1, math.pi/2)
        # Vector3(X = 1.000, Y = -3.000, Z = 2.000)
        ```
        """
        return Vector3(
            vector_1.x,
            vector_1.y*math.cos(angle) - vector_1.z*math.sin(angle),
            vector_1.y*math.sin(angle) + vector_1.z*math.cos(angle)
        )

    @staticmethod
    def angle_between(vector_1: 'Vector3', vector_2: 'Vector3') -> float:
        """Computes the angle in degrees between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in degrees.

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 0, 0)
        vector2 = Vector3(0, 1, 0)
        angle = Vector3.angle_between(vector1, vector2)
        # 90
        ```
        """
        proj_vector_1 = Vector3.to_matrix(vector_1)
        proj_vector_2 = Vector3.to_matrix(vector_2)
        dot_product = Vector3.dot_product(vector_1, vector_2)
        length_vector_1 = Vector3.length(vector_1)
        length_vector_2 = Vector3.length(vector_2)

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_radian_between(vector_1: 'Vector3', vector_2: 'Vector3') -> float:
        """Computes the angle in radians between two vectors.
        The angle between two vectors is the angle required to rotate one vector onto the other, measured in radians.

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The angle in radians between the input vectors.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 0, 0)
        vector2 = Vector3(0, 1, 0)
        angle = Vector3.angle_radian_between(vector1, vector2)
        # 1.5707963267948966
        ```
        """
        return math.acos((Vector3.dot_product(vector_1, vector_2)/(Vector3.length(vector_1)*Vector3.length(vector_2))))

    @staticmethod
    def angle_between_YZ(vector_1: 'Vector3', vector_2: 'Vector3') -> float:
        """Computes the angle in degrees between two vectors projected onto the YZ plane (X-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the YZ plane (X-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector3(1, 1, 0)
        vector2 = Vector3(1, 0, 1)
        angle = Vector3.angle_between_YZ(vector1, vector2)
        # 90
        ```
        """
        dot_product = Vector3.dot_product(vector_1, vector_2)
        length_vector_1 = Vector3.length(Vector3(0, vector_1.y, vector_1.z))
        length_vector_2 = Vector3.length(Vector3(0, vector_2.y, vector_2.z))
        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_between_XZ(vector_1: 'Vector3', vector_2: 'Vector3') -> float:
        """Computes the angle in degrees between two vectors projected onto the XZ plane (Y-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the XZ plane (Y-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector3(1, 0, 1)
        vector2 = Vector3(0, 1, 1)
        angle = Vector3.angle_between_XZ(vector1, vector2)
        # 90
        ```
        """
        dot_product = Vector3.dot_product(vector_1, vector_2)
        length_vector_1 = Vector3.length(Vector3(vector_1.x, 0, vector_1.z))
        length_vector_2 = Vector3.length(Vector3(vector_2.x, 0, vector_2.z))

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def angle_between_XY(vector_1: 'Vector3', vector_2: 'Vector3') -> float:
        """Computes the angle in degrees between two vectors projected onto the XY plane (Z-axis rotation).

        #### Parameters:
        - `vector_1` (`Vector3`): The first vector.
        - `vector_2` (`Vector3`): The second vector.

        #### Returns:
        `float`: The angle in degrees between the input vectors projected onto the XY plane (Z-axis rotation).

        #### Example usage:
        ```python
        vector1 = Vector3(1, 0, 1)
        vector2 = Vector3(0, 1, 1)
        angle = Vector3.angle_between_XY(vector1, vector2)
        # 45
        ```
        """
        dot_product = Vector3.dot_product(vector_1, vector_2)
        length_vector_1 = Vector3.length(Vector3(vector_1.x, vector_1.y, 0))
        length_vector_2 = Vector3.length(Vector3(vector_2.x, vector_2.y, 0))

        if length_vector_1 == 0 or length_vector_2 == 0:
            return 0

        cos_angle = dot_product / (length_vector_1 * length_vector_2)
        cos_angle = max(-1.0, min(cos_angle, 1.0))
        angle = math.acos(cos_angle)
        return math.degrees(angle)

    @staticmethod
    def value(vector_1: 'Vector3') -> tuple:
        """Returns the rounded values of the vector's components.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector.

        #### Returns:
        `tuple`: A tuple containing the rounded values of the vector's components.

        #### Example usage:
        ```python
        vector1 = Vector3(1.123456, 2.345678, 3.987654)
        rounded_values = Vector3.value(vector1)
        # (1.1235, 2.3457, 3.9877)
        ```
        """
        roundValue = 4
        return (round(vector_1.x, roundValue), round(vector_1.y, roundValue), round(vector_1.z, roundValue))

    @staticmethod
    def reverse(vector_1: 'Vector3') -> 'Vector3':
        """Returns the reverse (negation) of the vector.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector.

        #### Returns:
        `Vector3`: The reverse (negation) of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        reversed_vector = Vector3.reverse(vector1)
        # Vector3(X = -1, Y = -2, Z = -3)
        ```
        """
        return Vector3(
            vector_1.x*-1,
            vector_1.y*-1,
            vector_1.z*-1
        )

    @staticmethod
    def perpendicular(vector_1: 'Vector3') -> tuple:
        """Computes two vectors perpendicular to the input vector.

        #### Parameters:
        - `vector_1` (`Vector3`): The input vector.

        #### Returns:
        `tuple`: A tuple containing two vectors perpendicular to the input vector.

        #### Example usage:
        ```python
        vector1 = Vector3(1, 2, 3)
        perpendicular_vectors = Vector3.perpendicular(vector1)
        # (Vector3(X = 2, Y = -1, Z = 0), Vector3(X = -3, Y = 0, Z = 1))
        ```
        """
        lokX = Vector3(vector_1.y, -vector_1.x, 0)
        lokZ = Vector3.cross_product(vector_1, lokX)
        if lokZ.z < 0:
            lokZ = Vector3.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def normalize(vector_1: 'Vector3') -> 'Vector3':
        """Returns the normalized form of the input vector.
        The normalized form of a vector is a vector with the same direction but with a length (magnitude) of 1.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector to be normalized.

        #### Returns:
        `Vector3`: A new Vector3 object representing the normalized form of the input vector.

        #### Example usage:
        ```python
        vector1 = Vector3(3, 0, 4)
        normalized_vector = Vector3.normalize(vector1)
        # Vector3(X = 0.600, Y = 0.000, Z = 0.800)
        ```
        """
        length = Vector3.length(vector_1)
        if length == 0:
            return Vector3(0, 0, 0)

        normalized_vector = Vector3(
            vector_1.x / length,
            vector_1.y / length,
            vector_1.z / length
        )

        return normalized_vector

    @staticmethod
    def by_two_points(point_1: 'Point', point_2: 'Point') -> 'Vector3':
        """Computes the vector between two points.

        #### Parameters:
        - `point_1` (`Point`): The starting point.
        - `point_2` (`Point`): The ending point.

        #### Returns:
        `Vector3`: A new Vector3 object representing the vector between the two points.

        #### Example usage:
        ```python
        point1 = Point(1, 2, 3)
        point2 = Point(4, 6, 8)
        vector = Vector3.by_two_points(point1, point2)
        # Vector3(X = 3, Y = 4, Z = 5)
        ```
        """
        return Vector3(
            point_2.x-point_1.x,
            point_2.y-point_1.y,
            point_2.z-point_1.z
        )

    @staticmethod
    def rotate_XY(vector: 'Vector3', Beta: float) -> 'Vector3':
        """Rotates the vector in the XY plane by the specified angle.

        #### Parameters:
        - `vector` (`Vector3`): The vector to be rotated.
        - `Beta` (float): The angle of rotation in radians.

        #### Returns:
        `Vector3`: A new Vector3 object representing the rotated vector.

        #### Example usage:
        ```python
        vector = Vector3(1, 0, 0)
        rotated_vector = Vector3.rotate_XY(vector, math.pi/2)
        # Vector3(X = 0, Y = 1, Z = 0)
        ```
        """
        return Vector3(
            math.cos(Beta)*vector.x - math.sin(Beta)*vector.y,
            math.sin(Beta)*vector.x + math.cos(Beta)*vector.y,
            vector.z
        )

    @staticmethod
    def scale(vector: 'Vector3', scalefactor: float) -> 'Vector3':
        """Scales the vector by the specified scale factor.

        #### Parameters:
        - `vector` (`Vector3`): The vector to be scaled.
        - `scalefactor` (float): The scale factor.

        #### Returns:
        `Vector3`: A new Vector3 object representing the scaled vector.

        #### Example usage:
        ```python
        vector = Vector3(1, 2, 3)
        scaled_vector = Vector3.scale(vector, 2)
        # Vector3(X = 2, Y = 4, Z = 6)
        ```
        """
        return Vector3(
            vector.x * scalefactor,
            vector.y * scalefactor,
            vector.z * scalefactor
        )

    @staticmethod
    def new_length(vector_1: 'Vector3', newlength: float) -> 'Vector3':
        """Rescales the vector to have the specified length.

        #### Parameters:
        - `vector_1` (`Vector3`): The vector to be rescaled.
        - `newlength` (float): The desired length of the vector.

        #### Returns:
        `Vector3`: A new Vector3 object representing the rescaled vector.

        #### Example usage:
        ```python
        vector = Vector3(3, 4, 0)
        new_vector = Vector3.new_length(vector, 5)
        # Vector3(X = 3.000, Y = 4.000, Z = 0.000)
        ```
        """
        scale = newlength / Vector3.length(vector_1)

        return Vector3.scale(vector_1, scale)

    @staticmethod
    def to_matrix(vector: 'Vector3') -> list:
        """Converts the vector to a list representation.

        #### Parameters:
        - `vector` (`Vector3`): The vector to be converted.

        #### Returns:
        `list`: A list representation of the vector.

        #### Example usage:
        ```python
        vector = Vector3(1, 2, 3)
        vector_list = Vector3.to_matrix(vector)
        # [1, 2, 3]
        ```
        """
        return [vector.x, vector.y, vector.z]

    @staticmethod
    def from_matrix(vector_list: list) -> 'Vector3':
        """Creates a Vector3 object from a list representation.

        #### Parameters:
        - `vector_list` (list): The list representing the vector.

        #### Returns:
        `Vector3`: A Vector3 object created from the list representation.

        #### Example usage:
        ```python
        vector_list = [1, 2, 3]
        vector = Vector3.from_matrix(vector_list)
        # Vector3(X = 1, Y = 2, Z = 3)
        ```
        """
        return Vector3(
            vector_list[0],
            vector_list[1],
            vector_list[2]
        )

    def __str__(self):
        """Returns a string representation of the vector.

        #### Returns:
        `str`: A string representation of the vector.

        #### Example usage:
        ```python
        vector = Vector3(1.234, 2.345, 3.456)
        print(vector)
        # Vector3(X = 1.234, Y = 2.345, Z = 3.456)
        ```
        """
        return f"{__class__.__name__}(" + f"X = {self.x:.3f}, Y = {self.y:.3f}, Z = {self.z:.3f})"


X_axis = Vector3(1, 0, 0)

Y_Axis = Vector3(0, 1, 0)

Z_Axis = Vector3(0, 0, 1)
