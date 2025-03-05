# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe	 *
# *   maarten@3bm.co.nl, jan@3bm.co.nl & jonathan@3bm.co.nl				 *
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)	*
# *   as published by the Free Software Foundation; either version 2 of	 *
# *   the License, or (at your option) any later version.				   *
# *   for detail see the LICENCE text file.								 *
# *																		 *
# *   This program is distributed in the hope that it will be useful,	   *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
# *   GNU Library General Public License for more details.				  *
# *																		 *
# *   You should have received a copy of the GNU Library General Public	 *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA																   *
# *																		 *
# ***************************************************************************


"""This module provides tools for matrices
"""

__title__ = "matrix"
__author__ = "Maarten, Jan & Jonathan"
__url__ = "./abstract/matrix.py"

import math
import sys
from pathlib import Path
import copy
import pickle
from functools import reduce


from abstract.serializable import Serializable
from abstract.vector import Vector
from geometry.pointlist import PointList
from abstract.vector import Vector
from geometry.rect import Rect
from abstract.vector import Point

# [!not included in BP singlefile - end]


class Matrix(Serializable, list[list]):
    """
    elements are ordered like [row][column] or [y][x]
    """

    def __init__(self, matrix: list[list] = [[1, 0], [0, 1]]) -> "Matrix":
        list.__init__(self, matrix)

    @property
    def cols(self) -> "int":
        """returns the width (x size) of this matrix in columns."""
        return len(self[0])

    @property
    def rows(self) -> "int":
        """returns the height (y size) of this matrix in columns."""
        return len(self)

    @property
    def dimensions(self) -> int:
        return len(self) - 1

    def get_row(self, row: int) -> Vector:
        """

        Args:
                col (int): the row index

        Returns:
                Vector: a row vector
        """
        return Vector(self[row])

    def get_col(self, col: int) -> Vector:
        """

        Args:
                col (int): the column index

        Returns:
                Vector: a column vector
        """
        return Vector([self[row][col] for row in range(self.rows)])

    @property
    def origin(self) -> Vector:
        col = self.cols - 1
        return Vector([self[row][col] for row in range(self.rows - 1)])

    def get_axis(self, axis) -> Vector:
        """

        Args:
            axis (_type_): _description_

        Returns:
            Vector: the vector you'd get if you multiplied a vector containing all 0's except 1 on this axis without translation with the matrix.
            for example: m.multiply_without_translation(Vector(0, 0, 1)) == m.get_axis(2)
        """
        return Vector([self[row][axis] for row in range(self.rows - 1)])

    position = origin

    @staticmethod
    def scale(scalar: Vector) -> "Matrix":
        """

        Args:
                dimensions (int): the amount of dimensions of this scaling matrix. is it 2d? 3d?
                scalar (float): _description_

        Returns:
                Matrix: a scaling matrix of size (dimensions + 1, dimensions + 1)
        """
        dimensions = len(scalar)
        match dimensions:
            case 1:
                arr = [[scalar[0], 0], [0, 1]]
            case 2:
                arr = [[scalar[0], 0, 0], [0, scalar[1], 0], [0, 0, 1]]
            case 3:
                arr = [
                    [scalar[0], 0, 0, 0],
                    [0, scalar[1], 0, 0],
                    [0, 0, scalar[2], 0],
                    [0, 0, 0, 1],
                ]
            case _:
                arr = [
                    [
                        (
                            (
                                scalar[row]
                                if row < dimensions and col < dimensions
                                else 1
                            )
                            if row == col
                            else 0
                        )
                        for col in range(dimensions + 1)
                    ]
                    for row in range(dimensions + 1)
                ]
        return Matrix(arr)

    @staticmethod
    def empty(rows: int, cols=None):
        """creates a matrix of size n x m (rows x columns or y * x or h * w)"""
        if cols == None:
            cols = rows
        return Matrix([[0 for col in range(cols)] for row in range(rows)])

    @staticmethod
    def identity(dimensions: int) -> "Matrix":
        return Matrix.scale(Vector([1] * dimensions))

    @staticmethod
    def translate(addition: Vector) -> "Matrix":
        """

        Args:
                origin (Vector): the matrix translates all points by this offset.

        Returns:
                Matrix:
        """
        matrix_size: int = len(addition) + 1
        return Matrix(
            [
                [
                    1 if col == row else addition[row] if col == len(addition) else 0
                    for col in range(matrix_size)
                ]
                for row in range(matrix_size)
            ]
        )

    @staticmethod
    def by_origin(origin: Vector) -> "Matrix":
        """

        Args:
                origin (Vector):

        Returns:
                Matrix: a transformation matrix using the default axes with a specified origin.
        """
        return Matrix.translate(origin)

    @staticmethod
    def by_origin_and_axes(origin: Point, axes: list[Vector]) -> "Matrix":
        """

        Args:
                origin (Point): the translation vector of this matrix
                axes (list[Vector]): the x, y and other axes of this matrix

        Returns:
                Matrix: a matrix with columns ordered like this:
                axes[0], axes[1], ..., axes[n], origin
                the bottom row is just an identity row.
        """
        matrix_size = len(axes) + 1
        return Matrix(
            [
                # copied columns
                (
                    [
                        axes[col][row] if col < len(axes) else origin[row]
                        for col in range(matrix_size)
                    ]
                    if row < len(origin)
                    else
                    # identity row
                    [0 if col < len(axes) else 1 for col in range(matrix_size)]
                )
                for row in range(matrix_size)
            ]
        )

    @staticmethod
    def by_origin_unit_axes(origin: Point, unit_axes: list[Vector]) -> "Matrix":
        """

        Args:
                origin (Point): the origin of the matrix. all points will get translated by this vector.
                unit_axes (list[Vector]): the axes of this matrix, as unit vectors. they will get normalized!

        Returns:
                Matrix: the final matrix
        """
        return Matrix.by_origin_and_axes(
            origin, axes=[axis.normalized for axis in unit_axes]
        )

    @staticmethod
    def by_rotation(axis: Vector, angle: float) -> "Matrix":
        """creates a rotation matrix to rotate something over the origin around an axis by a specified angle

        Returns:
                Matrix: a rotation matrix. when a point is multiplied with this matrix, it's rotated.
        """
        # https://stackoverflow.com/questions/6721544/circular-rotation-around-an-arbitrary-axis
        normalized_axis = axis.normalized
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        return Matrix(
            [
                [
                    cos_angle + normalized_axis.x * normalized_axis.x * (1 - cos_angle),
                    normalized_axis.x * normalized_axis.y * (1 - cos_angle)
                    - normalized_axis.z * sin_angle,
                    normalized_axis.x * normalized_axis.z * (1 - cos_angle)
                    + normalized_axis.y * sin_angle,
                ],
                [
                    normalized_axis.y * normalized_axis.x * (1 - cos_angle)
                    + normalized_axis.z * sin_angle,
                    cos_angle + normalized_axis.y * normalized_axis.y * (1 - cos_angle),
                    normalized_axis.y * normalized_axis.z * (1 - cos_angle)
                    - normalized_axis.x * sin_angle,
                ],
                [
                    normalized_axis.z * normalized_axis.x * (1 - cos_angle)
                    - normalized_axis.y * sin_angle,
                    normalized_axis.z * normalized_axis.y * (1 - cos_angle)
                    + normalized_axis.x * sin_angle,
                    cos_angle + normalized_axis.z * normalized_axis.z * (1 - cos_angle),
                ],
            ]
        )

    @staticmethod
    def by_rotation_around_pivot(pivot: Point, axis: Vector, angle: float) -> "Matrix":
        # from right to left:
        # - translate objects so the pivot is at the origin
        # - rotate objects around the origin
        # - translate objects back so the pivot is at its old location

        return (
            Matrix.translate(pivot)
            * Matrix.by_rotation(axis, angle)
            * Matrix.translate(-pivot)
        )

    def __mul__(self, other: "Matrix | Vector | Rect | PointList"):
        """CAUTION! MATRICES NEED TO MULTIPLY FROM RIGHT TO LEFT!
        for example: translate * rotate (rotate first, translate after)
        and: matrix * point (point first, multiplied by matrix after)"""
        if isinstance(other, Matrix):
            # multiply matrices with eachother
            # https://www.geeksforgeeks.org/multiplication-two-matrices-single-line-using-numpy-python/

            # visualisation of resulting sizes:
            # https://en.wikipedia.org/wiki/Matrix_multiplication

            # the number of columns (width) in the first matrix needs to be equal to the number of rows (height) in the second matrix
            # (look at for i in range(other.height))

            # we are multiplying row vectors of self with col vectors of other
            if self.cols == other.rows:
                resultRows = self.rows
                resultCols = other.cols
                result: Matrix = Matrix.empty(resultRows, resultCols)
                # explicit for loops
                for row in range(self.rows):
                    for col in range(other.cols):
                        for multiplyIndex in range(other.rows):
                            # this is the simple code, which would work if the number of self.cols was equal to other.rows
                            result[row][col] += (
                                self[row][multiplyIndex] * other[multiplyIndex][col]
                            )
            else:
                resultCols = max(self.cols, other.cols)
                resultRows = max(self.rows, other.rows)

                result: Matrix = Matrix.empty(resultRows, resultCols)

                # the size of the vector that we're multiplying.
                multiplyVectorSize = max(self.cols, other.rows)

                # explicit for loops
                for row in range(resultRows):
                    for col in range(resultCols):
                        for multiplyIndex in range(multiplyVectorSize):
                            # if an element doesn't exist in the matrix, we use an identity element.
                            selfValue = (
                                self[row][multiplyIndex]
                                if row < self.rows and multiplyIndex < self.cols
                                else 1 if multiplyIndex == row else 0
                            )
                            otherValue = (
                                other[multiplyIndex][col]
                                if col < other.cols and multiplyIndex < other.rows
                                else 1 if multiplyIndex == col else 0
                            )
                            result[row][col] += selfValue * otherValue

        elif isinstance(other, PointList):
            return other.__class__([self * p for p in other])
        # point comes in from top and comes out to the right:
        # |
        # v
        # a b
        # c d ->
        elif isinstance(other, Vector):
            result: Vector = Vector([0] * len(other))
            # loop over column vectors and multiply them with the vector. sum the results (multiplied col 1 + multiplied col 2) to get the final product!
            for col in range(self.cols):
                if col < len(other):
                    for row in range(len(result)):
                        result[row] += self[row][col] * other[col]
                else:
                    # otherValue = 1, just add the vector
                    for row in range(len(result)):
                        result[row] += self[row][col]
            return result
        elif isinstance(other, Rect):
            mp0 = self * other.p0
            mp1 = self * other.p1
            return Rect.by_points([mp0, mp1])
        else:
            # this causes python to check for rmul on the other type
            return NotImplemented
        return result

    transform = multiply = __mul__

    def multiply_without_translation(self, other: Vector) -> Vector:
        """this function just multiplies the coords by the matrix, but doesn't add anything to the result. good for sizes for example.

        Args:
                other (Vector): _description_

        Returns:
                _type_: _description_
        """
        result: Vector = Vector([0] * self.rows)
        for col in range(min(self.cols, len(other))):
            for row in range(self.rows):
                result[row] += self[row][col] * other[col]
        return result

    def get_col(self, col_index: int):
        return Vector([row[col_index] for row in self])

    def get_row(self, row_index: int):
        return Vector(self[row_index])

    @property
    def translation(self) -> Vector:
        """the translation is just the last column of the matrix

        Returns:
                Vector: the last column of this matrix, which gets added to the result when a point is multiplied by the matrix
        """
        return self.get_col(self.cols - 1)

    def cofactor(self, i: int, j: int) -> float:
        """Calculates the cofactor of element at position (i, j)."""
        minor_matrix = self.minor(i, j)
        return ((-1) ** (i + j)) * minor_matrix.determinant()

    def cofactor_matrix(self) -> "Matrix":
        """Returns the cofactor matrix."""
        return Matrix(
            [[self.cofactor(i, j) for j in range(self.cols)] for i in range(self.rows)]
        )

    def adjugate(self) -> "Matrix":
        """Returns the adjugate (or adjoint) of the matrix."""
        return self.cofactor_matrix().transpose()

    def determinant(self) -> float:
        """Calculates the determinant of the matrix."""
        if self.rows != self.cols:
            raise ValueError("Matrix must be square to compute determinant.")
        if self.rows == 1:
            return self[0][0]
        if self.rows == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        det = 0
        for c in range(self.cols):
            det += ((-1) ** c) * self[0][c] * self.minor(0, c).determinant()
        return det

    def minor(self, row_index: int, col_index: int) -> "Matrix":
        """Returns the minor of the matrix by removing the i-th row and j-th column."""
        return Matrix(
            [
                row[:col_index] + row[col_index + 1 :]
                for row in (self[:row_index] + self[row_index + 1 :])
            ]
        )

    def inverse(self) -> "Matrix":
        """Returns the inverse of the matrix if it exists."""

        determinant = self.determinant()
        if determinant == 0:
            raise ValueError("Matrix is not invertible (determinant is zero).")

        adjugate = self.adjugate()
        return Matrix([[element / determinant for element in row] for row in adjugate])

    def add(self, other: "Matrix"):
        if self.shape() != other.shape():
            raise ValueError("Matrices must have the same dimensions")
        return Matrix(
            [
                [self[i][j] + other.matrix[i][j] for j in range(len(self[0]))]
                for i in range(len(self))
            ]
        )

    def all(self, axis=None):
        if axis is None:
            return all(all(row) for row in self)
        elif axis == 0:
            return [
                all(self[row][col] for row in range(len(self)))
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [all(col) for col in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def any(self, axis=None):
        if axis is None:
            return any(any(row) for row in self)
        elif axis == 0:
            return [
                any(self[row][col] for row in range(len(self)))
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [any(col) for col in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def argmax(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self for item in sublist]
            return flat_list.index(max(flat_list))
        elif axis == 0:
            return [
                max(range(len(self)), key=lambda row: self[row][col])
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [max(range(len(row)), key=lambda col: row[col]) for row in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def argmin(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self for item in sublist]
            return flat_list.index(min(flat_list))
        elif axis == 0:
            return [
                min(range(len(self)), key=lambda row: self[row][col])
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [min(range(len(row)), key=lambda col: row[col]) for row in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def argpartition(self, kth, axis=0):
        def partition(arr, kth):
            pivot = arr[kth]
            less = [i for i in range(len(arr)) if arr[i] < pivot]
            equal = [i for i in range(len(arr)) if arr[i] == pivot]
            greater = [i for i in range(len(arr)) if arr[i] > pivot]
            return less + equal + greater

        if axis == 0:
            return [
                partition([self[row][col] for row in range(len(self))], kth)
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [partition(row, kth) for row in self]

    def argsort(self, axis=0):
        if axis == 0:
            return [
                [row for row, val in sorted(enumerate(col), key=lambda x: x[1])]
                for col in zip(*self)
            ]
        elif axis == 1:
            return [list(range(len(self[0]))) for _ in self]

    def astype(self, dtype):
        cast_matrix = [[dtype(item) for item in row] for row in self]
        return Matrix(cast_matrix)

    def byteswap(self, inplace=False):
        if inplace:
            for i in range(len(self)):
                for j in range(len(self[i])):
                    self[i][j] = ~self[i][j]
            return self
        else:
            new_matrix = [[~item for item in row] for row in self]
            return Matrix(new_matrix)

    def choose(self, choices, mode="raise"):
        if mode != "raise":
            raise NotImplementedError("Only 'raise' mode is implemented")

        chosen = [[choices[item] for item in row] for row in self]
        return Matrix(chosen)

    def compress(self, condition, axis=None):
        if axis == 0:
            compressed = [row for row, cond in zip(self, condition) if cond]
            return Matrix(compressed)
        else:
            raise NotImplementedError("Axis other than 0 is not implemented")

    def clip(self, min=None, max=None):
        clipped_matrix = []
        for row in self:
            clipped_row = [
                (
                    max
                    if max is not None and val > max
                    else min if min is not None and val < min else val
                )
                for val in row
            ]
            clipped_matrix.append(clipped_row)
        return Matrix(clipped_matrix)

    def conj(self):
        conjugated_matrix = [
            [complex(item).conjugate() for item in row] for row in self
        ]
        return Matrix(conjugated_matrix)

    def conjugate(self):
        return self.conj()

    def copy(self):
        copied_matrix = copy.deepcopy(self)
        return Matrix(copied_matrix)

    def cumprod(self, axis=None):
        if axis is None:
            flat_list = self.flatten()
            cumprod_list = []
            cumprod = 1
            for item in flat_list:
                cumprod *= item
                cumprod_list.append(cumprod)
            return Matrix([cumprod_list])
        else:
            raise NotImplementedError("Axis handling not implemented in this example")

    def cumsum(self, axis=None):
        if axis is None:
            flat_list = self.flatten()
            cumsum_list = []
            cumsum = 0
            for item in flat_list:
                cumsum += item
                cumsum_list.append(cumsum)
            return Matrix([cumsum_list])
        else:
            raise NotImplementedError("Axis handling not implemented in this example")

    def diagonal(self, offset=0):
        return [
            self[i][i + offset]
            for i in range(len(self))
            if 0 <= i + offset < len(self[i])
        ]

    def dump(self, file):
        with open(file, "wb") as f:
            pickle.dump(self, f)

    def dumps(self):
        return pickle.dumps(self)

    def fill(self, value):
        for i in range(len(self)):
            for j in range(len(self[i])):
                self[i][j] = value

    @staticmethod
    def from_points(from_point: Point, to_point: Point):
        Vz = Vector.by_two_points(from_point, to_point)
        Vz = Vz.normalized
        Vzglob = Vector(0, 0, 1)
        Vx = Vector.cross_product(Vz, Vzglob)
        if Vx.length == 0:
            Vx = Vector(1, 0, 0) if Vz.x != 1 else Vector(0, 1, 0)
        Vx = Vx.normalized
        Vy = Vector.cross_product(Vx, Vz)

        return Matrix(
            [
                [Vx.x, Vy.x, Vz.x, from_point.x],
                [Vx.y, Vy.y, Vz.y, from_point.y],
                [Vx.z, Vy.z, Vz.z, from_point.z],
                [0, 0, 0, 1],
            ]
        )

    def flatten(self):
        return [item for sublist in self for item in sublist]

    def getA(self):
        return self

    def getA1(self):
        return [item for sublist in self for item in sublist]

    def getH(self):
        conjugate_transposed = [
            [complex(self[j][i]).conjugate() for j in range(len(self))]
            for i in range(len(self[0]))
        ]
        return Matrix(conjugate_transposed)

    def getI(self):
        raise NotImplementedError(
            "Matrix inversion is a complex operation not covered in this simple implementation."
        )

    def getT(self):
        return self.transpose()

    def getfield(self, dtype, offset=0):
        raise NotImplementedError(
            "This method is conceptual and depends on structured data support within the Matrix."
        )

    def item(self, *args):
        if len(args) == 1:
            index = args[0]
            rows, cols = len(self), len(self[0])
            return self[index // cols][index % cols]
        elif len(args) == 2:
            return self[args[0]][args[1]]
        else:
            raise ValueError("Invalid number of indices.")

    def itemset(self, *args):
        if len(args) == 2:
            index, value = args
            rows, cols = len(self), len(self[0])
            self[index // cols][index % cols] = value
        elif len(args) == 3:
            row, col, value = args
            self[row][col] = value
        else:
            raise ValueError("Invalid number of arguments.")

    def max(self, axis=None):
        if axis is None:
            return max(item for sublist in self for item in sublist)
        elif axis == 0:
            return [
                max(self[row][col] for row in range(len(self)))
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [max(row) for row in self]
        else:
            raise ValueError("Invalid axis.")

    def mean(self, axis=None):
        if axis is None:
            flat_list = self.flatten()
            return sum(flat_list) / len(flat_list)
        elif axis == 0:
            return [
                sum(self[row][col] for row in range(len(self))) / len(self)
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [sum(row) / len(row) for row in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def min(self, axis=None):
        if axis is None:
            return min(item for sublist in self for item in sublist)
        elif axis == 0:
            return [
                min(self[row][col] for row in range(len(self)))
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [min(row) for row in self]
        else:
            raise ValueError("Invalid axis.")

    @staticmethod
    def zeros(rows, cols):
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])

    @staticmethod
    def participation(self):
        pass

    def prod(self, axis=None):
        if axis is None:
            return reduce(
                lambda x, y: x * y, [item for sublist in self for item in sublist], 1
            )
        elif axis == 0:
            return [
                reduce(
                    lambda x, y: x * y, [self[row][col] for row in range(len(self))], 1
                )
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [reduce(lambda x, y: x * y, row, 1) for row in self]
        else:
            raise ValueError("Invalid axis.")

    def ptp(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self for item in sublist]
            return max(flat_list) - min(flat_list)
        elif axis == 0:
            return [
                max([self[row][col] for row in range(len(self))])
                - min([self[row][col] for row in range(len(self))])
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [max(row) - min(row) for row in self]
        else:
            raise ValueError("Invalid axis.")

    def put(self, indices, values):
        if len(indices) != len(values):
            raise ValueError("Length of indices and values must match.")
        flat_list = self.ravel()
        for index, value in zip(indices, values):
            flat_list[index] = value

    @staticmethod
    def random(rows, cols):
        import random

        return Matrix([[random.random() for _ in range(cols)] for _ in range(rows)])

    def ravel(self):
        return [item for sublist in self for item in sublist]

    def repeat(self, repeats, axis=None):
        if axis is None:
            flat_list = self.ravel()
            repeated = [item for item in flat_list for _ in range(repeats)]
            return Matrix([repeated])
        elif axis == 0:
            repeated_matrix = [row for row in self for _ in range(repeats)]
        elif axis == 1:
            repeated_matrix = [
                [item for item in row for _ in range(repeats)] for row in self
            ]
        else:
            raise ValueError("Invalid axis.")
        return Matrix(repeated_matrix)

    def reshape(self, rows, cols):
        flat_list = self.flatten()
        if len(flat_list) != rows * cols:
            raise ValueError("The total size of the new array must be unchanged.")
        reshaped = [flat_list[i * cols : (i + 1) * cols] for i in range(rows)]
        return Matrix(reshaped)

    def resize(self, new_rows, new_cols):
        return Matrix(
            [
                [
                    (
                        self[row][col]
                        if (col < self.cols and row < self.rows)
                        else (1 if row == col else 0)
                    )
                    for col in range(new_cols)
                ]
                for row in range(new_rows)
            ]
        )

    def round(self, decimals=0):
        rounded_matrix = [[round(item, decimals) for item in row] for row in self]
        return Matrix(rounded_matrix)

    def searchsorted(self, v, side="left"):
        flat_list = self.flatten()
        i = 0
        if side == "left":
            while i < len(flat_list) and flat_list[i] < v:
                i += 1
        elif side == "right":
            while i < len(flat_list) and flat_list[i] <= v:
                i += 1
        else:
            raise ValueError("side must be 'left' or 'right'")
        return i

    def setfield(self, val, dtype, offset=0):
        raise NotImplementedError(
            "Structured data operations are not supported in this Matrix class."
        )

    def setflags(self, write=None, align=None, uic=None):
        print("This Matrix class does not support setting flags directly.")

    def shape(self):
        return len(self), len(self[0])

    def sort(self, axis=-1):
        if axis == -1 or axis == 1:
            for row in self:
                row.sort()
        elif axis == 0:
            transposed = [
                [self[j][i] for j in range(len(self))] for i in range(len(self[0]))
            ]
            for row in transposed:
                row.sort()
            self = [
                [transposed[j][i] for j in range(len(transposed))]
                for i in range(len(transposed[0]))
            ]
        else:
            raise ValueError("Axis out of range.")

    def squeeze(self):
        squeezed_matrix = [row for row in self if any(row)]
        return Matrix(squeezed_matrix)

    def std(self, axis=None, ddof=0):
        var = self.var(axis=axis, ddof=ddof)
        if isinstance(var, list):
            return [x**0.5 for x in var]
        else:
            return var**0.5

    def subtract(self, other):
        if self.shape() != other.shape():
            raise ValueError("Matrices must have the same dimensions")
        return Matrix(
            [
                [self[i][j] - other.matrix[i][j] for j in range(len(self[0]))]
                for i in range(len(self))
            ]
        )

    def sum(self, axis=None):
        if axis is None:
            return sum(sum(row) for row in self)
        elif axis == 0:
            return [
                sum(self[row][col] for row in range(len(self)))
                for col in range(len(self[0]))
            ]
        elif axis == 1:
            return [sum(row) for row in self]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def swapaxes(self, axis1, axis2):
        if axis1 == 0 and axis2 == 1 or axis1 == 1 and axis2 == 0:
            return Matrix(
                [[self[j][i] for j in range(len(self))] for i in range(len(self[0]))]
            )
        else:
            raise ValueError("Axis values out of range for a 2D matrix.")

    def take(self, indices, axis=None):
        if axis is None:
            flat_list = [item for sublist in self for item in sublist]
            return Matrix([flat_list[i] for i in indices])
        elif axis == 0:
            return Matrix([self[i] for i in indices])
        else:
            raise ValueError("Axis not supported or out of range for a 2D matrix.")

    def tofile(self, fid, sep="", format="%s"):
        if isinstance(fid, str):
            with open(fid, "wb" if sep == "" else "w") as f:
                self._write_to_file(f, sep, format)
        else:
            self._write_to_file(fid, sep, format)

    def _write_to_file(self, file, sep, format):
        if sep == "":
            file.write(self.tobytes())
        else:
            for row in self:
                line = sep.join(format % item for item in row) + "\n"
                file.write(line)

    def __str__(self):
        # '\n'.join([str(row) for row in self])
        # vs code doesn't work with new lines
        return "Matrix(" + list.__str__(self) + ")"

    def trace(self, offset=0):
        rows, cols = len(self), len(self[0])
        return sum(
            self[i][i + offset]
            for i in range(min(rows, cols - offset))
            if 0 <= i + offset < cols
        )

    def transpose(self):
        transposed = [
            [self[j][i] for j in range(len(self))] for i in range(len(self[0]))
        ]
        return Matrix(transposed)

    def var(self, axis=None, ddof=0):
        if axis is None:
            flat_list = self.flatten()
            mean = sum(flat_list) / len(flat_list)
            return sum((x - mean) ** 2 for x in flat_list) / (len(flat_list) - ddof)
        elif axis == 0 or axis == 1:
            means = self.mean(axis=axis)
            if axis == 0:
                return [
                    sum((self[row][col] - means[col]) ** 2 for row in range(len(self)))
                    / (len(self) - ddof)
                    for col in range(len(self[0]))
                ]
            else:
                return [
                    sum((row[col] - means[idx]) ** 2 for col in range(len(row)))
                    / (len(row) - ddof)
                    for idx, row in enumerate(self)
                ]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def _validate(self):
        rows = len(self)
        cols = len(self[0]) if rows > 0 else 0
        return rows, cols


CoordinateSystem = Matrix
