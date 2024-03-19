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
    def __init__(self, origin: Point, x_axis, y_axis, z_axis):
        self.id = generateID()
        self.type = __class__.__name__
        self.Origin = origin
        self.Xaxis = Vector3.normalize(x_axis)
        self.Y_axis = Vector3.normalize(y_axis)
        self.Z_axis = Vector3.normalize(z_axis)

    def serialize(self):
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
    def deserialize(data):
        origin = Point.deserialize(data['Origin'])
        x_axis = Vector3.deserialize(data['Xaxis'])
        y_axis = Vector3.deserialize(data['Y_axis'])
        z_axis = Vector3.deserialize(data['Z_axis'])
        return CoordinateSystem(origin, x_axis, y_axis, z_axis)

    # @classmethod
    # def by_origin(self, origin: Point):
    #     self.Origin = origin
    #     self.Xaxis = X_axis
    #     self.Y_axis = YAxis
    #     self.Z_axis = ZAxis
    #     return self

    @classmethod
    def by_origin(self, origin: Point):
        from abstract.coordinatesystem import X_axis, YAxis, ZAxis
        return self(origin, x_axis=X_axis, y_axis=YAxis, z_axis=ZAxis)

    # @staticmethod
    # def translate(CSOld, direction):
    #     CSNew = CoordinateSystem(CSOld.Origin, CSOld.Xaxis, CSOld.Y_axis, CSOld.Z_axis)
    #     new_origin = Point.translate(CSNew.Origin, direction)
    #     CSNew.Origin = new_origin
    #     return CSNew

    @staticmethod
    def translate(CSOld, direction: Vector3):
        from abstract.vector import Vector3
        pt = CSOld.Origin
        new_origin = Point.translate(pt, direction)

        X_axis = Vector3(1, 0, 0)

        YAxis = Vector3(0, 1, 0)

        ZAxis = Vector3(0, 0, 1)

        CSNew = CoordinateSystem(
            new_origin, x_axis=X_axis, y_axis=YAxis, z_axis=ZAxis)

        CSNew.Origin = new_origin
        return CSNew

    @staticmethod
    def transform(CS1, CS2):  # incorrect output
        """
        Transforms CS1 into the coordinate system defined by CS2.
        :param CS1: The original CoordinateSystem instance.
        :param CS2: The target CoordinateSystem instance.
        :return: A new CoordinateSystem instance aligned with CS2.
        """
        from abstract.vector import Vector3

        translation_vector = Vector3.subtract(CS2.Origin, CS1.Origin)

        rotation_matrix = CoordinateSystem.calculate_rotation_matrix(
            CS1.Xaxis, CS1.Y_axis, CS1.Z_axis, CS2.Xaxis, CS2.Y_axis, CS2.Z_axis)

        xaxis_transformed = Vector3.dot_product(rotation_matrix, CS1.Xaxis)
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
        origin1_n = Point.to_matrix(origin1)
        origin2_n = Point.to_matrix(origin2)

        new_origin_n = origin1_n + (origin2_n - origin1_n)
        return Point(new_origin_n[0], new_origin_n[1], new_origin_n[2])

    @staticmethod
    def calculate_rotation_matrix(xaxis1: Vector3, yaxis1: Vector3, zaxis1: Vector3, xaxis2: Vector3, yaxis2: Vector3, zaxis2: Vector3):
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
        """
        Normalizes the axes of the coordinate system to make them unit vectors.
        """
        self.Xaxis = Vector3.normalize(self.Xaxis)
        self.Y_axis = Vector3.normalize(self.Y_axis)
        self.Z_axis = Vector3.normalize(self.Z_axis)

    @staticmethod
    def move_local(CSOld, x: float, y: float, z: float):
        from abstract.vector import Vector3
        # move coordinatesystem by y in local coordinates(not global)
        xloc_vect_norm = CSOld.Xaxis
        xdisp = Vector3.scale(xloc_vect_norm, x)
        yloc_vect_norm = CSOld.Xaxis
        ydisp = Vector3.scale(yloc_vect_norm, y)
        zloc_vect_norm = CSOld.Xaxis
        zdisp = Vector3.scale(zloc_vect_norm, z)
        disp = Vector3.sum3(xdisp, ydisp, zdisp)
        CS = CoordinateSystem.translate(CSOld, disp)
        return CS

    @staticmethod
    def by_point_main_vector(self, NewOriginCoordinateSystem: Point, DirectionVectorZ: Vector3):
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
        return f"{__class__.__name__}(Origin = " + f"{self.Origin}, X_axis = {self.Xaxis}, YAxis = {self.Y_axis}, ZAxis = {self.Z_axis})"


X_axis = Vector3(1, 0, 0)
Vector3(0, 1, 0)
Vector3(0, 0, 1)
CSGlobal = CoordinateSystem(Point(0, 0, 0), X_axis, YAxis, ZAxis)
