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


"""This module provides tools for vectors
"""

__title__ = "vector"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/vector.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import *

# [!not included in BP singlefile - end]


class Vector3:
    def __init__(self, x, y, z):
        self.id = generateID()
        self.type = __class__.__name__
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

        self.x = x
        self.y = y
        self.z = z

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    @staticmethod
    def deserialize(data):
        return Vector3(data['x'], data['y'], data['z'])

    @staticmethod
    def sum(vector_1, vector_2):
        return Vector3(
            vector_1.x + vector_2.x,
            vector_1.y + vector_2.y,
            vector_1.z + vector_2.z
        )

    @staticmethod
    def sum3(vector_1, vector_2, vector_3):
        return Vector3(
            vector_1.x + vector_2.x + vector_3.x,
            vector_1.y + vector_2.y + vector_3.y,
            vector_1.z + vector_2.z + vector_3.z
        )

    @staticmethod
    def diff(vector_1, vector_2):
        return Vector3(
            vector_1.x - vector_2.x,
            vector_1.y - vector_2.y,
            vector_1.z - vector_2.z
        )

    @staticmethod
    def subtract(vector_1, vector_2):
        return Vector3(
            vector_1.x - vector_2.x,
            vector_1.y - vector_2.y,
            vector_1.z - vector_2.z
        )

    @staticmethod
    def divide(vector_1, vector_2):
        return Vector3(
            vector_1.x / vector_2.x,
            vector_1.y / vector_2.y,
            vector_1.z / vector_2.z
        )

    @staticmethod
    def square(vector_1):
        return Vector3(
            vector_1.x ** 2,
            vector_1.y ** 2,
            vector_1.z ** 2
        )

    @staticmethod
    def to_point(vector_1):
        from geometry.point import Point
        return Point(x=vector_1.x, y=vector_1.y, z=vector_1.z)

    @staticmethod
    def to_line(vector_1, vector_2):
        from geometry.point import Point
        from geometry.curve import Line
        return Line(start=Point(x=vector_1.x, y=vector_1.y, z=vector_1.z), end=Point(x=vector_2.x, y=vector_2.y, z=vector_2.z))

    @staticmethod
    def by_line(line_1):
        return Vector3(line_1.dx, line_1.dy, line_1.dz)

    @staticmethod
    def line_by_length(vector_1, length: float):
        return None
        # return Line(start = Point(x=vector_1.x,y=vector_1.y,z=vector_1.z), end = Point(x=vector_2.x,y=vector_2.y,z=vector_2.z))

    @staticmethod
    def cross_product(vector_1, vector_2):
        return Vector3(
            vector_1.y*vector_2.z - vector_1.z*vector_2.y,
            vector_1.z*vector_2.x - vector_1.x*vector_2.z,
            vector_1.x*vector_2.y - vector_1.y*vector_2.x
        )

    @staticmethod
    def dot_product(vector_1, vector_2):
        return vector_1.x*vector_2.x+vector_1.y*vector_2.y+vector_1.z*vector_2.z

    @staticmethod
    def product(number, vector_1):
        return Vector3(
            vector_1.x*number,
            vector_1.y*number,
            vector_1.z*number
        )

    @staticmethod
    def length(vector_1):
        return math.sqrt(vector_1.x*vector_1.x+vector_1.y*vector_1.y+vector_1.z*vector_1.z)

    @staticmethod
    def pitch(vector_1, angle):
        return Vector3(
            vector_1.x,
            vector_1.y*math.cos(angle) - vector_1.z*math.sin(angle),
            vector_1.y*math.sin(angle) + vector_1.z*math.cos(angle)
        )

    @staticmethod
    def angle_between(vector_1, vector_2):
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
    def angle_radian_between(vector_1, vector_2):
        return math.acos((Vector3.dot_product(vector_1, vector_2)/(Vector3.length(vector_1)*Vector3.length(vector_2))))

    @staticmethod
    def angle_between_YZ(vector_1, vector_2):  # X Axis degrees
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
    def angle_between_XZ(vector_1, vector_2):  # Y Axis degrees
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
    def angle_between_XY(vector_1, vector_2):  # Z Axis degrees
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
    def value(vector_1):
        roundValue = 4
        return (round(vector_1.x, roundValue), round(vector_1.y, roundValue), round(vector_1.z, roundValue))

    @staticmethod
    def reverse(vector_1):
        return Vector3(
            vector_1.x*-1,
            vector_1.y*-1,
            vector_1.z*-1
        )

    @staticmethod
    def perpendicular(vector_1):
        lokX = Vector3(vector_1.y, -vector_1.x, 0)
        lokZ = Vector3.cross_product(vector_1, lokX)
        if lokZ.z < 0:
            lokZ = Vector3.reverse(lokZ)
        return lokX, lokZ

    @staticmethod
    def normalize(vector_1):
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
    def by_two_points(p1, p2):
        return Vector3(
            p2.x-p1.x,
            p2.y-p1.y,
            p2.z-p1.z
        )

    @staticmethod
    def rotate_XY(vector_1, Beta):
        return Vector3(
            math.cos(Beta)*vector_1.x - math.sin(Beta)*vector_1.y,
            math.sin(Beta)*vector_1.x + math.cos(Beta)*vector_1.y,
            vector_1.z
        )

    @staticmethod
    def scale(vector_1, scalefactor):
        return Vector3(
            vector_1.x * scalefactor,
            vector_1.y * scalefactor,
            vector_1.z * scalefactor
        )

    @staticmethod
    def new_length(vector_1, newlength: float):
        scale = newlength / Vector3.length(vector_1)

        return Vector3.scale(vector_1, scale)

    @staticmethod
    def to_matrix(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def from_matrix(self):
        return Vector3(
            self[0],
            self[1],
            self[2]
        )

    def __str__(self):
        return f"{__class__.__name__}(" + f"X = {self.x:.3f}, Y = {self.y:.3f}, Z = {self.z:.3f})"


XAxis = Vector3(1, 0, 0)

YAxis = Vector3(0, 1, 0)

ZAxis = Vector3(0, 0, 1)
