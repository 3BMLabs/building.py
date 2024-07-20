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


"""This module provides tools for coordinatesystems
"""

__title__ = "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/coordinatesystem.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from abstract.vector import *

# from project.fileformat import project

# [!not included in BP singlefile - end]


class CoordinateSystem:
    # UNITY VECTORS REQUIRED #TOdo organize resic
    """The `CoordinateSystem` class represents a coordinate system in 3D space, defined by an origin point and three orthogonal unit vectors along the X, Y, and Z axes."""
    def __init__(self, origin: Point, x_axis, y_axis, z_axis):
        """Initializes a new CoordinateSystem instance.

        #### Parameters:
        - `origin` (Point): The origin point of the coordinate system.
        - `x_axis` (Vector3): The X-axis direction vector.
        - `y_axis` (Vector3): The Y-axis direction vector.
        - `z_axis` (Vector3): The Z-axis direction vector.

        #### Example usage:
        ```python
        origin = Point(0, 0, 0)
        x_axis = Vector3(1, 0, 0)
        y_axis = Vector3(0, 1, 0)
        z_axis = Vector3(0, 0, 1)
        coordinate_system = CoordinateSystem(origin, x_axis, y_axis, z_axis)
        ```
        """

        self.id = generateID()
        self.type = __class__.__name__
        self.Origin = origin
        self.Xaxis = Vector3.normalize(x_axis)
        self.Y_axis = Vector3.normalize(y_axis)
        self.Z_axis = Vector3.normalize(z_axis)

    def serialize(self) -> dict:
        """Serializes the coordinate system's attributes into a dictionary.

        #### Returns:
        `dict`: A dictionary containing the serialized attributes of the coordinate system.

        #### Example usage:
        ```python
        coordinate_system = CoordinateSystem(...)
        serialized_cs = coordinate_system.serialize()
        ```
        """
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'Origin': self.Origin.serialize(),
            'Xaxis': self.Xaxis.serialize(),
            'Y_axis': self.Y_axis.serialize(),
            'Z_axis': self.Z_axis.serialize()
        }

    @staticmethod
    def deserialize(data: dict):
        """Recreates a CoordinateSystem object from serialized data.

        #### Parameters:
        - `data` (dict): The dictionary containing the serialized data of a CoordinateSystem object.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem object initialized with the data from the dictionary.

        #### Example usage:
        ```python
        data = {...}
        coordinate_system = CoordinateSystem.deserialize(data)
        ```
        """
        origin = Point.deserialize(data['Origin'])
        x_axis = Vector3.deserialize(data['Xaxis'])
        y_axis = Vector3.deserialize(data['Y_axis'])
        z_axis = Vector3.deserialize(data['Z_axis'])
        return CoordinateSystem(origin, x_axis, y_axis, z_axis)

    # @classmethod
    # def by_origin(self, origin: Point):
    #     self.Origin = origin
    #     self.Xaxis = X_axis
    #     self.Y_axis = Y_Axis
    #     self.Z_axis = Z_Axis
    #     return self

    @classmethod
    def by_origin(self, origin: Point) -> 'CoordinateSystem':
        """Creates a CoordinateSystem with a new origin while keeping the standard orientation.

        #### Parameters:
        - `origin` (Point): The new origin point of the coordinate system.

        #### Returns:
        `CoordinateSystem`: A CoordinateSystem instance with the specified origin and standard axes orientation.

        #### Example usage:
        ```python
        new_origin = Point(10, 10, 10)
        coordinate_system = CoordinateSystem.by_origin(new_origin)
        ```
        """
        from abstract.coordinatesystem import X_axis, Y_Axis, Z_Axis
        return self(origin, x_axis=X_axis, y_axis=Y_Axis, z_axis=Z_Axis)

    # @staticmethod
    # def translate(cs_old, direction):
    #     CSNew = CoordinateSystem(cs_old.Origin, cs_old.Xaxis, cs_old.Y_axis, cs_old.Z_axis)
    #     new_origin = Point.translate(CSNew.Origin, direction)
    #     CSNew.Origin = new_origin
    #     return CSNew

    @staticmethod
    def translate(cs_old, direction: Vector3):
        """Translates an existing CoordinateSystem by a given direction vector.

        #### Parameters:
        - `cs_old` (CoordinateSystem): The original CoordinateSystem to be translated.
        - `direction` (Vector3): The direction vector by which to translate the coordinate system.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem instance translated according to the direction vector.

        #### Example usage:
        ```python
        original_cs = CoordinateSystem(...)
        direction_vector = Vector3(5, 5, 0)
        translated_cs = CoordinateSystem.translate(original_cs, direction_vector)
        ```
        """
        from abstract.vector import Vector3
        pt = cs_old.Origin
        new_origin = Point.translate(pt, direction)

        X_axis = Vector3(1, 0, 0)

        Y_Axis = Vector3(0, 1, 0)

        Z_Axis = Vector3(0, 0, 1)

        CSNew = CoordinateSystem(
            new_origin, x_axis=X_axis, y_axis=Y_Axis, z_axis=Z_Axis)

        CSNew.Origin = new_origin
        return CSNew

    @staticmethod
    def transform(CS1, CS2):
        """Transforms one coordinate system (CS1) to align with another (CS2).

        This method calculates the transformation required to align CS1's axes with those of CS2, including translation and rotation.

        #### Parameters:
        - `CS1` (CoordinateSystem): The original coordinate system to be transformed.
        - `CS2` (CoordinateSystem): The target coordinate system to align with.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem instance that has been transformed to align with CS2.

        #### Example usage:
        ```python
        CS1 = CoordinateSystem(...)
        CS2 = CoordinateSystem(...)
        transformed_CS = CoordinateSystem.transform(CS1, CS2)
        ```
        """
        from abstract.vector import Vector3

        translation_vector = Vector3.subtract(CS2.Origin, CS1.Origin)

        rotation_matrix = CoordinateSystem.calculate_rotation_matrix(
            CS1.X_axis, CS1.Y_axis, CS1.Z_axis, CS2.X_axis, CS2.Y_axis, CS2.Z_axis)

        xaxis_transformed = Vector3.dot_product(rotation_matrix, CS1.X_axis)
        yaxis_transformed = Vector3.dot_product(rotation_matrix, CS1.Y_axis)
        zaxis_transformed = Vector3.dot_product(rotation_matrix, CS1.Z_axis)

        xaxis_normalized = Vector3.normalize(
            Vector3.from_matrix(xaxis_transformed))
        yaxis_normalized = Vector3.normalize(
            Vector3.from_matrix(yaxis_transformed))
        zaxis_normalized = Vector3.normalize(
            Vector3.from_matrix(zaxis_transformed))

        new_origin = Point.translate(CS1.Origin, translation_vector)
        new_CS = CoordinateSystem(
            new_origin, xaxis_normalized, yaxis_normalized, zaxis_normalized)

        return new_CS

    @staticmethod
    def translate_origin(origin1: Point, origin2: Point):
        """Translates the origin of a coordinate system from one point to another.

        #### Parameters:
        - `origin1` (Point): The original origin point.
        - `origin2` (Point): The new origin point to translate to.

        #### Returns:
        `Point`: The new origin point after translation.

        #### Example usage:
        ```python
        origin1 = Point(0, 0, 0)
        origin2 = Point(5, 5, 5)
        new_origin = CoordinateSystem.translate_origin(origin1, origin2)
        ```
        """
        origin1_n = Point.to_matrix(origin1)
        origin2_n = Point.to_matrix(origin2)

        new_origin_n = origin1_n + (origin2_n - origin1_n)
        return Point(new_origin_n[0], new_origin_n[1], new_origin_n[2])

    @staticmethod
    def calculate_rotation_matrix(xaxis1: Vector3, yaxis1: Vector3, zaxis1: Vector3, xaxis2: Vector3, yaxis2: Vector3, zaxis2: Vector3):
        """Calculates the rotation matrix needed to align one set of axes with another.

        #### Parameters:
        - `xaxis1`, `yaxis1`, `zaxis1`: The original axes vectors.
        - `xaxis2`, `yaxis2`, `zaxis2`: The target axes vectors to align with.

        #### Returns:
        A matrix representing the rotation required to align the first set of axes with the second.

        #### Example usage:
        ```python
        xaxis1 = Vector3(1, 0, 0)
        yaxis1 = Vector3(0, 1, 0)
        zaxis1 = Vector3(0, 0, 1)
        xaxis2 = Vector3(0, 1, 0)
        yaxis2 = Vector3(-1, 0, 0)
        zaxis2 = Vector3(0, 0, 1)
        rotation_matrix = CoordinateSystem.calculate_rotation_matrix(xaxis1, yaxis1, zaxis1, xaxis2, yaxis2, zaxis2)
        ```
        """
        from abstract.vector import Vector3

        def transpose(matrix):
            return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

        def matrix_multiply(matrix1, matrix2):
            result = []
            for i in range(len(matrix1)):
                row = []
                for j in range(len(matrix2[0])):
                    sum = 0
                    for k in range(len(matrix2)):
                        sum += matrix1[i][k] * matrix2[k][j]
                    row.append(sum)
                result.append(row)
            return result

        def matrix_inverse(matrix):
            determinant = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - \
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) + \
                matrix[0][2] * (matrix[1][0] * matrix[2][1] -
                                matrix[1][1] * matrix[2][0])
            if determinant == 0:
                raise ValueError("Matrix is not invertible")
            inv_det = 1.0 / determinant
            result = [[0] * 3 for _ in range(3)]
            result[0][0] = (matrix[1][1] * matrix[2][2] -
                            matrix[1][2] * matrix[2][1]) * inv_det
            result[0][1] = (matrix[0][2] * matrix[2][1] -
                            matrix[0][1] * matrix[2][2]) * inv_det
            result[0][2] = (matrix[0][1] * matrix[1][2] -
                            matrix[0][2] * matrix[1][1]) * inv_det
            result[1][0] = (matrix[1][2] * matrix[2][0] -
                            matrix[1][0] * matrix[2][2]) * inv_det
            result[1][1] = (matrix[0][0] * matrix[2][2] -
                            matrix[0][2] * matrix[2][0]) * inv_det
            result[1][2] = (matrix[0][2] * matrix[1][0] -
                            matrix[0][0] * matrix[1][2]) * inv_det
            result[2][0] = (matrix[1][0] * matrix[2][1] -
                            matrix[1][1] * matrix[2][0]) * inv_det
            result[2][1] = (matrix[0][1] * matrix[2][0] -
                            matrix[0][0] * matrix[2][1]) * inv_det
            result[2][2] = (matrix[0][0] * matrix[1][1] -
                            matrix[0][1] * matrix[1][0]) * inv_det
            return result

        R1_transpose = transpose([Vector3.to_matrix(
            xaxis1), Vector3.to_matrix(yaxis1), Vector3.to_matrix(zaxis1)])
        R2_transpose = transpose([Vector3.to_matrix(
            xaxis2), Vector3.to_matrix(yaxis2), Vector3.to_matrix(zaxis2)])

        return matrix_multiply(R2_transpose, matrix_inverse(R1_transpose))

    @staticmethod
    def normalize(self):
        """Normalizes the axes vectors of a given CoordinateSystem to unit vectors.

        This method ensures that the X, Y, and Z axes of the coordinate system are unit vectors (vectors of length 1), which is essential for many calculations involving directions and orientations in 3D space.

        #### Parameters:
        - `self` (CoordinateSystem): The coordinate system whose axes vectors are to be normalized.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem instance with normalized axes vectors.

        #### Example usage:
        ```python
        CS_before_normalization = CoordinateSystem(
            origin=Point(0, 0, 0),
            x_axis=Vector3(10, 0, 0),
            y_axis=Vector3(0, 10, 0),
            z_axis=Vector3(0, 0, 10)
        )
        CS_after_normalization = CoordinateSystem.normalize(CS_before_normalization)
        # Now, CS_after_normalization's X, Y, and Z axes are unit vectors.
        ```
        """
        self.X_axis = Vector3.normalize(self.X_axis)
        self.Y_axis = Vector3.normalize(self.Y_axis)
        self.Z_axis = Vector3.normalize(self.Z_axis)

    @staticmethod
    def move_local(cs_old, x: float, y: float, z: float):
        """Moves a CoordinateSystem locally along its own axes.

        #### Parameters:
        - `cs_old` (CoordinateSystem): The coordinate system to move.
        - `x` (float): The distance to move along the local X-axis.
        - `y` (float): The distance to move along the local Y-axis.
        - `z` (float): The distance to move along the local Z-axis.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem instance that has been moved according to the specified distances.

        #### Example usage:
        ```python
        cs_old = CoordinateSystem(...)
        moved_cs = CoordinateSystem.move_local(cs_old, 10, 0, 5)
        # The returned CoordinateSystem is moved 10 units along its X-axis and 5 units along its Z-axis.
        ```
        """
        from abstract.vector import Vector3
        # move coordinatesystem by y in local coordinates(not global)
        xloc_vect_norm = cs_old.X_axis
        xdisp = Vector3.scale(xloc_vect_norm, x)
        yloc_vect_norm = cs_old.X_axis
        ydisp = Vector3.scale(yloc_vect_norm, y)
        zloc_vect_norm = cs_old.X_axis
        zdisp = Vector3.scale(zloc_vect_norm, z)
        disp = Vector3.sum3(xdisp, ydisp, zdisp)
        CS = CoordinateSystem.translate(cs_old, disp)
        return CS

    @staticmethod
    def by_point_main_vector(NewOriginCoordinateSystem: Point, DirectionVectorZ: Vector3) -> 'CoordinateSystem':
        """Creates a CoordinateSystem with a specified origin and a main direction vector for the Z-axis.

        #### Parameters:
        - `NewOriginCoordinateSystem` (Point): The origin point of the new CoordinateSystem.
        - `DirectionVectorZ` (Vector3): The main direction vector to define the new Z-axis.

        #### Returns:
        `CoordinateSystem`: A CoordinateSystem instance with the specified origin and Z-axis orientation.

        #### Example usage:
        ```python
        new_origin = Point(0, 0, 0)
        main_direction = Vector3(0, 0, 1)
        coordinate_system = CoordinateSystem.by_point_main_vector(new_origin, main_direction)
        ```
        """
        vz = DirectionVectorZ  # LineVector and new Z-axis
        vz = Vector3.normalize(vz)  # NewZAxis
        vx = Vector3.perpendicular(vz)[0]  # NewXAxis
        try:
            vx = Vector3.normalize(vx)  # NewXAxisnormalized
        except:
            # In case of vertical element the length is zero
            vx = Vector3(1, 0, 0)
        vy = Vector3.perpendicular(vz)[1]  # NewYAxis
        try:
            vy = Vector3.normalize(vy)  # NewYAxisnormalized
        except:
            # In case of vertical element the length is zero
            vy = Vector3(0, 1, 0)
        CSNew = CoordinateSystem(NewOriginCoordinateSystem, vx, vy, vz)
        return CSNew

    def __str__(self):
        return f"{__class__.__name__}(Origin = " + f"{self.Origin}, X_axis = {self.Xaxis}, Y_Axis = {self.Y_axis}, Z_Axis = {self.Z_axis})"


X_axis = Vector3(1, 0, 0)
Vector3(0, 1, 0)
Vector3(0, 0, 1)
CSGlobal = CoordinateSystem(Point(0, 0, 0), X_axis, Y_Axis, Z_Axis)
