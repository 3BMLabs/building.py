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


"""This module provides tools for planes
"""

__title__ = "plane"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/plane.py"

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from abstract.vector import *

# [!not included in BP singlefile - end]


class Plane:
    # Plane is an infinite element in space defined by a point and a normal
    """The `Plane` class represents an infinite plane in 3D space, defined uniquely by an origin point and a normal vector, along with two other vectors lying on the plane, providing a complete basis for defining plane orientation and position."""
    def __init__(self):
        """"Initializes a new Plane instance.

        - `Origin` (Point): The origin point of the plane, which also lies on the plane.
        - `Normal` (Vector): A vector perpendicular to the plane, defining its orientation.
        - `v1` (Vector): A vector lying on the plane, typically representing the "x" direction on the plane.
        - `v2` (Vector): Another vector on the plane, perpendicular to `v1` and typically representing the "y" direction on the plane.
        """
        self.Origin = Point(0, 0, 0)
        self.Normal = Vector(x=0, y=0, z=1)
        self.vector_1 = Vector(x=1, y=0, z=0)
        self.vector_2 = Vector(x=0, y=1, z=0)

    @classmethod
    def by_two_vectors_origin(cls, vector_1: Vector, vector_2: Vector, origin: Point) -> 'Plane':
        """Creates a Plane defined by two vectors and an origin point.
        This method establishes a plane using two vectors that lie on the plane and an origin point. The normal is calculated as the cross product of the two vectors, ensuring it is perpendicular to the plane.

        #### Parameters:
            vector_1 (Vector): The first vector on the plane.
            vector_2 (Vector): The second vector on the plane, should not be parallel to vector_1.
            origin (Point): The origin point of the plane, lying on the plane.

        #### Returns:
            Plane: A Plane instance defined by the given vectors and origin.
        
        #### Example usage:
        ```python

        ```
        """
        p1 = Plane()
        p1.Normal = Vector.normalize(Vector.cross_product(vector_1, vector_2))
        p1.Origin = origin
        p1.vector_1 = vector_1
        p1.vector_2 = vector_2
        return p1

    def __str__(self) -> str:
        """Generates a string representation of the Plane.

        #### Returns:
            str: A string describing the Plane with its origin, normal, and basis vectors.
         
        #### Example usage:
        ```python

        ```
        """

        return f"{__class__.__name__}(" + f"{self.Origin}, {self.Normal}, {self.vector_1}, {self.vector_2})"

    # TODO
    # byLineAndPoint
    # byOriginNormal
    # byThreePoints
