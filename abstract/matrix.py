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


"""This module provides tools for matrixces
"""

__title__ = "matrix"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/matrix.py"

import sys
from pathlib import Path
import copy
import pickle
from functools import reduce
import struct

sys.path.append(str(Path(__file__).resolve().parents[1]))

from project.fileformat import *
from geometry.point import Point
from abstract.vector import *

# [!not included in BP singlefile - end]

class Matrix:
    def __init__(self, matrix=None):
        if matrix is None:
            self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        else:
            self.matrix = matrix

    def add(self, other):
        if self.shape() != other.shape():
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])

    def all(self, axis=None):
        if axis is None:
            return all(all(row) for row in self.matrix)
        elif axis == 0:
            return [all(self.matrix[row][col] for row in range(len(self.matrix))) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [all(col) for col in self.matrix]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def any(self, axis=None):
        if axis is None:
            return any(any(row) for row in self.matrix)
        elif axis == 0:
            return [any(self.matrix[row][col] for row in range(len(self.matrix))) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [any(col) for col in self.matrix]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def argmax(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self.matrix for item in sublist]
            return flat_list.index(max(flat_list))
        elif axis == 0:
            return [max(range(len(self.matrix)), key=lambda row: self.matrix[row][col]) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [max(range(len(row)), key=lambda col: row[col]) for row in self.matrix]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def argmin(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self.matrix for item in sublist]
            return flat_list.index(min(flat_list))
        elif axis == 0:
            return [min(range(len(self.matrix)), key=lambda row: self.matrix[row][col]) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [min(range(len(row)), key=lambda col: row[col]) for row in self.matrix]
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
            return [partition([self.matrix[row][col] for row in range(len(self.matrix))], kth) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [partition(row, kth) for row in self.matrix]

    def argsort(self, axis=0):
        if axis == 0:
            return [[row for row, val in sorted(enumerate(col), key=lambda x: x[1])] for col in zip(*self.matrix)]
        elif axis == 1:
            return [list(range(len(self.matrix[0]))) for _ in self.matrix]

    def astype(self, dtype):
        cast_matrix = [[dtype(item) for item in row] for row in self.matrix]
        return Matrix(cast_matrix)

    def byteswap(self, inplace=False):
        if inplace:
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    self.matrix[i][j] = ~self.matrix[i][j]
            return self
        else:
            new_matrix = [[~item for item in row] for row in self.matrix]
            return Matrix(new_matrix)

    def choose(self, choices, mode='raise'):
        if mode != 'raise':
            raise NotImplementedError("Only 'raise' mode is implemented")

        chosen = [[choices[item] for item in row] for row in self.matrix]
        return Matrix(chosen)

    def compress(self, condition, axis=None):
        if axis == 0:
            compressed = [row for row, cond in zip(
                self.matrix, condition) if cond]
            return Matrix(compressed)
        else:
            raise NotImplementedError("Axis other than 0 is not implemented")

    def clip(self, min=None, max=None):
        clipped_matrix = []
        for row in self.matrix:
            clipped_row = [max if max is not None and val >
                           max else min if min is not None and val < min else val for val in row]
            clipped_matrix.append(clipped_row)
        return Matrix(clipped_matrix)

    def conj(self):
        conjugated_matrix = [[complex(item).conjugate()
                              for item in row] for row in self.matrix]
        return Matrix(conjugated_matrix)

    def conjugate(self):
        return self.conj()

    def copy(self):
        copied_matrix = copy.deepcopy(self.matrix)
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
            raise NotImplementedError(
                "Axis handling not implemented in this example")

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
            raise NotImplementedError(
                "Axis handling not implemented in this example")

    def diagonal(self, offset=0):
        return [self.matrix[i][i + offset] for i in range(len(self.matrix)) if 0 <= i + offset < len(self.matrix[i])]

    def dump(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.matrix, f)

    def dumps(self):
        return pickle.dumps(self.matrix)

    def fill(self, value):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j] = value

    @staticmethod
    def from_points(from_point: Point, to_point: Point):
        Vz = Vector3.by_two_points(from_point, to_point)
        Vz = Vector3.normalize(Vz)
        Vzglob = Vector3(0, 0, 1)
        Vx = Vector3.cross_product(Vz, Vzglob)
        if Vector3.length(Vx) == 0:
            Vx = Vector3(1, 0, 0) if Vz.x != 1 else Vector3(0, 1, 0)
        Vx = Vector3.normalize(Vx)
        Vy = Vector3.cross_product(Vx, Vz)

        return Matrix([
            [Vx.x, Vy.x, Vz.x, from_point.x],
            [Vx.y, Vy.y, Vz.y, from_point.y],
            [Vx.z, Vy.z, Vz.z, from_point.z],
            [0, 0, 0, 1]
        ])

    def flatten(self):
        return [item for sublist in self.matrix for item in sublist]

    def getA(self):
        return self.matrix

    def getA1(self):
        return [item for sublist in self.matrix for item in sublist]

    def getH(self):
        conjugate_transposed = [[complex(self.matrix[j][i]).conjugate() for j in range(
            len(self.matrix))] for i in range(len(self.matrix[0]))]
        return Matrix(conjugate_transposed)

    def getI(self):
        raise NotImplementedError(
            "Matrix inversion is a complex operation not covered in this simple implementation.")

    def getT(self):
        return self.transpose()

    def getfield(self, dtype, offset=0):
        raise NotImplementedError(
            "This method is conceptual and depends on structured data support within the Matrix.")

    def item(self, *args):
        if len(args) == 1:
            index = args[0]
            rows, cols = len(self.matrix), len(self.matrix[0])
            return self.matrix[index // cols][index % cols]
        elif len(args) == 2:
            return self.matrix[args[0]][args[1]]
        else:
            raise ValueError("Invalid number of indices.")

    def itemset(self, *args):
        if len(args) == 2:
            index, value = args
            rows, cols = len(self.matrix), len(self.matrix[0])
            self.matrix[index // cols][index % cols] = value
        elif len(args) == 3:
            row, col, value = args
            self.matrix[row][col] = value
        else:
            raise ValueError("Invalid number of arguments.")

    def max(self, axis=None):
        if axis is None:
            return max(item for sublist in self.matrix for item in sublist)
        elif axis == 0:
            return [max(self.matrix[row][col] for row in range(len(self.matrix))) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [max(row) for row in self.matrix]
        else:
            raise ValueError("Invalid axis.")

    def mean(self, axis=None):
        if axis is None:
            flat_list = self.flatten()
            return sum(flat_list) / len(flat_list)
        elif axis == 0:
            return [sum(self.matrix[row][col] for row in range(len(self.matrix))) / len(self.matrix) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [sum(row) / len(row) for row in self.matrix]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def min(self, axis=None):
        if axis is None:
            return min(item for sublist in self.matrix for item in sublist)
        elif axis == 0:
            return [min(self.matrix[row][col] for row in range(len(self.matrix))) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [min(row) for row in self.matrix]
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
            return reduce(lambda x, y: x * y, [item for sublist in self.matrix for item in sublist], 1)
        elif axis == 0:
            return [reduce(lambda x, y: x * y, [self.matrix[row][col] for row in range(len(self.matrix))], 1) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [reduce(lambda x, y: x * y, row, 1) for row in self.matrix]
        else:
            raise ValueError("Invalid axis.")

    def ptp(self, axis=None):
        if axis is None:
            flat_list = [item for sublist in self.matrix for item in sublist]
            return max(flat_list) - min(flat_list)
        elif axis == 0:
            return [max([self.matrix[row][col] for row in range(len(self.matrix))]) - min([self.matrix[row][col] for row in range(len(self.matrix))]) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [max(row) - min(row) for row in self.matrix]
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
        return [item for sublist in self.matrix for item in sublist]

    def repeat(self, repeats, axis=None):
        if axis is None:
            flat_list = self.ravel()
            repeated = [item for item in flat_list for _ in range(repeats)]
            return Matrix([repeated])
        elif axis == 0:
            repeated_matrix = [
                row for row in self.matrix for _ in range(repeats)]
        elif axis == 1:
            repeated_matrix = [
                [item for item in row for _ in range(repeats)] for row in self.matrix]
        else:
            raise ValueError("Invalid axis.")
        return Matrix(repeated_matrix)

    def reshape(self, rows, cols):
        flat_list = self.flatten()
        if len(flat_list) != rows * cols:
            raise ValueError(
                "The total size of the new array must be unchanged.")
        reshaped = [flat_list[i * cols:(i + 1) * cols] for i in range(rows)]
        return Matrix(reshaped)

    def resize(self, new_shape):
        new_rows, new_cols = new_shape
        current_rows, current_cols = len(self.matrix), len(
            self.matrix[0]) if self.matrix else 0
        if new_rows < current_rows:
            self.matrix = self.matrix[:new_rows]
        else:
            for _ in range(new_rows - current_rows):
                self.matrix.append([0] * current_cols)
        for row in self.matrix:
            if new_cols < current_cols:
                row[:] = row[:new_cols]
            else:
                row.extend([0] * (new_cols - current_cols))

    def round(self, decimals=0):
        rounded_matrix = [[round(item, decimals)
                           for item in row] for row in self.matrix]
        return Matrix(rounded_matrix)

    def searchsorted(self, v, side='left'):
        flat_list = self.flatten()
        i = 0
        if side == 'left':
            while i < len(flat_list) and flat_list[i] < v:
                i += 1
        elif side == 'right':
            while i < len(flat_list) and flat_list[i] <= v:
                i += 1
        else:
            raise ValueError("side must be 'left' or 'right'")
        return i

    def setfield(self, val, dtype, offset=0):
        raise NotImplementedError(
            "Structured data operations are not supported in this Matrix class.")

    def setflags(self, write=None, align=None, uic=None):
        print("This Matrix class does not support setting flags directly.")

    def shape(self):
        return len(self.matrix), len(self.matrix[0])

    def sort(self, axis=-1):
        if axis == -1 or axis == 1:
            for row in self.matrix:
                row.sort()
        elif axis == 0:
            transposed = [[self.matrix[j][i] for j in range(
                len(self.matrix))] for i in range(len(self.matrix[0]))]
            for row in transposed:
                row.sort()
            self.matrix = [[transposed[j][i] for j in range(
                len(transposed))] for i in range(len(transposed[0]))]
        else:
            raise ValueError("Axis out of range.")

    def squeeze(self):
        squeezed_matrix = [row for row in self.matrix if any(row)]
        return Matrix(squeezed_matrix)

    def std(self, axis=None, ddof=0):
        var = self.var(axis=axis, ddof=ddof)
        if isinstance(var, list):
            return [x ** 0.5 for x in var]
        else:
            return var ** 0.5

    def subtract(self, other):
        if self.shape() != other.shape():
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.matrix[i][j] - other.matrix[i][j] for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))])

    def sum(self, axis=None):
        if axis is None:
            return sum(sum(row) for row in self.matrix)
        elif axis == 0:
            return [sum(self.matrix[row][col] for row in range(len(self.matrix))) for col in range(len(self.matrix[0]))]
        elif axis == 1:
            return [sum(row) for row in self.matrix]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def swapaxes(self, axis1, axis2):
        if axis1 == 0 and axis2 == 1 or axis1 == 1 and axis2 == 0:
            return Matrix([[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))])
        else:
            raise ValueError("Axis values out of range for a 2D matrix.")

    def take(self, indices, axis=None):
        if axis is None:
            flat_list = [item for sublist in self.matrix for item in sublist]
            return Matrix([flat_list[i] for i in indices])
        elif axis == 0:
            return Matrix([self.matrix[i] for i in indices])
        else:
            raise ValueError(
                "Axis not supported or out of range for a 2D matrix.")

    def tobytes(self):
        byte_array = bytearray()
        for row in self.matrix:
            for item in row:
                byte_array.extend(struct.pack('i', item))
        return bytes(byte_array)

    def tofile(self, fid, sep="", format="%s"):
        if isinstance(fid, str):
            with open(fid, 'wb' if sep == "" else 'w') as f:
                self._write_to_file(f, sep, format)
        else:
            self._write_to_file(fid, sep, format)

    def _write_to_file(self, file, sep, format):
        if sep == "":
            file.write(self.tobytes())
        else:
            for row in self.matrix:
                line = sep.join(format % item for item in row) + "\n"
                file.write(line)

    def tostring(self):
        for row in self.matrix:
            print(' '.join(map(str, row)))

    def trace(self, offset=0):
        rows, cols = len(self.matrix), len(self.matrix[0])
        return sum(self.matrix[i][i + offset] for i in range(min(rows, cols - offset)) if 0 <= i + offset < cols)

    def transpose(self):
        transposed = [[self.matrix[j][i] for j in range(
            len(self.matrix))] for i in range(len(self.matrix[0]))]
        return Matrix(transposed)

    def var(self, axis=None, ddof=0):
        if axis is None:
            flat_list = self.flatten()
            mean = sum(flat_list) / len(flat_list)
            return sum((x - mean) ** 2 for x in flat_list) / (len(flat_list) - ddof)
        elif axis == 0 or axis == 1:
            means = self.mean(axis=axis)
            if axis == 0:
                return [sum((self.matrix[row][col] - means[col]) ** 2 for row in range(len(self.matrix))) / (len(self.matrix) - ddof) for col in range(len(self.matrix[0]))]
            else:
                return [sum((row[col] - means[idx]) ** 2 for col in range(len(row))) / (len(row) - ddof) for idx, row in enumerate(self.matrix)]
        else:
            raise ValueError("Axis must be None, 0, or 1")

    def _validate(self):
        rows = len(self.matrix)
        cols = len(self.matrix[0]) if rows > 0 else 0
        return rows, cols