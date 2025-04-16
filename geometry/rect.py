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


"""This module provides tools for boundingboxes and rectangles"""

__title__ = "rect"
__author__ = "Maarten & Jonathan & JohnHeikens"
__url__ = "./abstract/boundingbox.py"

import copy
import sys


from geometry.shape import Shape
from abstract.vector import Vector
from abstract.vector import Point
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]


class Rect(Serializable, Shape):
    """Represents a two-dimensional bounding box."""

    def __init__(self, *args, **kwargs):
        """@
        #### Example usage:
        ```python
        rect = Rect(3, 4) # x 3, width 4
        rect2 = Rect(z=10) # x 0, y 0, z 10, width 0, length 0, height 0
        rect3 = Rect(Vector(y=8), Vector(x = 4)) # x 0, y 8, width 4, length 0
        ```
        """

        # first half = for position
        half: int = len(args) // 2
        self.p0 = Point(*args[0:half])
        # second half for size
        self.size = Vector(*args[half:])

        for kwarg in kwargs.items():
            try:
                offset = self.p0.set_axis(kwarg[0], kwarg[1])
                if offset != None:
                    self.size.change_axis_count(offset)
            except ValueError:
                axis_index = Rect.size_axis_index(kwarg[0])
                offset = self.size.set_axis(axis_index, kwarg[1])
                if offset != None:
                    self.p0.change_axis_count(offset)

        Serializable.__init__(self)

    def change_axis_count(self, axis_count: int):
        self.p0.change_axis_count(axis_count)
        self.size.change_axis_count(axis_count)

    @staticmethod
    def size_axis_index(axis) -> int:
        return ["width", "length", "height"].index(axis)

    @property
    def width(self):
        return self.size.x

    @width.setter
    def width(self, value):
        self.size.x = value

    @property
    def length(self):
        return self.size.y

    @length.setter
    def length(self, value):
        self.size.y = value

    @property
    def height(self):
        return self.size.z

    @height.setter
    def height(self, value):
        self.size.z = value

    w = width
    l = length
    h = height

    @property
    def center(self):
        return self.p0 + self.size * 0.5

    @center.setter
    def center(self, value):
        self.p0 = value - (self.size * 0.5)

    centroid = center

    @property
    def x(self):
        return self.p0.x

    @x.setter
    def x(self, value):
        self.p0.x = value

    @property
    def y(self):
        return self.p0.y

    @y.setter
    def y(self, value):
        self.p0.y = value

    @property
    def z(self):
        return self.p0.z

    @z.setter
    def z(self, value):
        self.p0.z = value

    def area(self):
        return self.size.volume()

    @property
    def p1(self):
        return self.p0 + self.size

    def __str__(self):
        return (
            __class__.__name__ + "(p0=" + str(self.p0) + ",size=" + str(self.size) + ")"
        )

    @staticmethod
    def by_points(points: list[Point]) -> "Rect":
        """Constructs a bounding box based on a list of points.

        Calculates the minimum and maximum values from the points to define the corners of the bounding box.

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

        axis_count = len(points[0])
        if axis_count == 0:
            raise ValueError("please provide points")

        # copy
        p0 = Point(points[0])
        p1 = Point(points[0])

        # it's faster to not skip the first point than to check if it's the first point or revert to an index-based loop
        for p in points:
            for axis in range(axis_count):
                p0[axis] = min(p0[axis], p[axis])
                p1[axis] = max(p1[axis], p[axis])
        return Rect(p0, p1 - p0)

    def expanded(self, border_size: float) -> "Rect":
        return Rect(self.p0 - border_size, self.size + border_size * 2)

    @staticmethod
    def centered_at_origin(size: Vector) -> "Rect":
        """Constructs a rect with specified dimensions, centered at the origin.

        #### Parameters:
        - `size` (Vector): The size of the bounding box.

        #### Returns:
        `Rect`: The bounding box instance with dimensions centered at the origin.

        #### Example usage:
        ```python
        bbox = Rect().centered_at_origin(length=100, width=50)
        # Rect centered at origin with specified length and width
        ```
        """

        return Rect(size * -0.5, size)

    @staticmethod
    def by_size(size: Vector) -> "Rect":
        """Constructs a rect with specified dimensions, with its pos0 at the origin.

        #### Parameters:
        - `size` (Vector): The size of the rectangle

        #### Returns:
        `Rect`: The rect instance with dimensions centered at the origin.

        #### Example usage:
        ```python
        rect = Rect().by_size(length=100, width=50)
        # Rect(x=0, y=0, width = 100, length = 100)
        ```
        """
        return Rect(Vector([0] * len(size)), size)

    def collides(self, other: "Rect") -> bool:
        """checks if two rectangles collide with eachother. <br>
        when they touch eachother exactly (f.e. a Rect with position [0] and size [1] and a rect with position [1] and size [1]), the function will return false.

        Args:
                other (Rect): the rectangle which may collide with this rectangle

        Returns:
                bool: true if the two rectangles overlap
        """
        for axis in range(len(self.p0)):
            if (
                self.p0[axis] + self.size[axis] <= other.p0[axis]
                or other.p0[axis] + other.size[axis] <= self.p0[axis]
            ):
                return False
        return True

    def contains(self, other: "Rect") -> bool:
        for axis in range(len(self.p0)):
            if (
                other.p0[axis] < self.p0[axis]
                or other.p0[axis] + other.size[axis] > self.p0[axis] + self.size[axis]
            ):
                return False
        return True

    def substractFrom(self, other: "Rect") -> list["Rect"]:
        """cut the 'other' rectangle in pieces by substracting this rectangle from it

        Args:
                other (Rect): the rectangle to substract this rectangle from

        Returns:
                list[Rect]: a list of up to 4 rectangles for 2d (if the rect is in the center). CAUTION: THEY OVERLAP!
        """
        pieces: list[Rect] = []
        to_clone = other
        # check each axis
        for axis in range(len(self.p0)):
            self_p1 = self.p0[axis] + self.size[axis]
            other_p1 = other.p0[axis] + other.size[axis]
            if self_p1 < other_p1:
                diff = other_p1 - self_p1

                piece: Rect = copy.deepcopy(to_clone)

                piece.p0[axis] = self_p1

                piece.size[axis] = diff
                pieces.append(piece)
                # also crop other.
                # to_clone.size[axis] -= diff
            self_p0 = self.p0[axis]
            other_p0 = other.p0[axis]
            if self_p0 > other_p0:
                diff = self_p0 - other_p0
                piece: Rect = copy.deepcopy(to_clone)
                piece.size[axis] = diff
                pieces.append(piece)
                # to_clone.p0[axis] = self_p0
                # to_clone.size[axis] -= diff
        return pieces

    @staticmethod
    def outer(children: list["Rect"]) -> "Rect":
        """creates a rectangle containing child rectangles.

        Args:
                children (list[&#39;Rect&#39;]): the children to contain in the rectangle

        Returns:
                Rect: the bounds
        """
        p0 = children[0].p0
        p1 = children[0].p1
        for i in range(1, len(children)):
            child = children[i]
            for axis_index in range(len(p0)):
                p0[axis_index] = min(child.p0[axis_index], p0[axis_index])
                p1[axis_index] = max(
                    child.p0[axis_index] + child.size[axis_index], p1[axis_index]
                )
        return Rect(p0, p1 - p0)

    def get_corner(self, corner_index: int) -> Point:
        """

        Args:
                corner_index (int): corners are ordered like 0 -> 000, 1 -> 001, 2 -> 010, 011, 100 etc.
                where 0 = the minimum and 1 = the maximum

        Returns:
                Point: a corner
        """
        corner: Point = Point()
        for axis in range(len(self.p0)):
            corner.append(
                self.p0[axis] + self.size[axis]
                if corner_index & 1 << axis
                else self.p0[axis]
            )
        return corner

    def corners(self, axis_count=None) -> "list[Point]":
        """Calculates the corners of the bounding.

        #### Returns:
        `list[Point]`: A list of Point objects representing the corners of the bounding box.

        #### Example usage:
        ```python
        bbox3d = Rect(Point(1, 1, 1), Vector(2, 2, 2))
        corners = bbox3d.corners()
        Returns a list of eight points representing the corners of the bounding box
        ```
        """
        corners: list[Point] = []
        if axis_count == None:
            axis_count = len(self.p0)
        for corner_index in range(2 << axis_count):
            corners.append(self.get_corner(corner_index))
        return corners
