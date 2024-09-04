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


"""This module provides tools for boundingbox
"""

__title__ = "coordinatesystem"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/boundingbox.py"

import copy
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.coords import Coords
from packages.helper import *
from geometry.solid import Extrusion
from abstract.vector import Vector
from abstract.coordinatesystem import CSGlobal
from geometry.curve import PolyCurve, Line
from geometry.point import Point
from geometry.geometry2d import PolyCurve2D
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]

class Rect(Serializable):
    """Represents a two-dimensional bounding box."""
    def __init__(self, p0: Coords, size: Coords):
        self.id = generateID()
        self.type = __class__.__name__
        self.points = []
        self.corners = []
        self.isClosed = True
        self.z = 0
        self.p0 = p0
        self.size = size
        

    
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
    
    def __str__(self):
        return __class__.__name__ + '(p0=' + str(self.p0)+',size=' + str(self.size) + ')'
    def __repr__(self):
        return str(self)

    def by_points(self, points: list[Point]) -> 'Rect':
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
        if axis_count == 0: raise ValueError("please provide points")

        self.points = points
        p0 = points[0]
        p1 = points[0]
        
        #it's faster to not skipt the first point than to check if it's the first point or revert to an index-based loop
        for p in points:
            for axis in range(axis_count):
                p0[axis] = min(p0[axis], p[axis])
                p1[axis] = max(p1[axis], p[axis])
                
        self.size = p1 - p0
        return self
    
    def expanded(self, border_size: float) -> 'Rect':
        return Rect(self.p0 - border_size, self.size + border_size * 2)
    
    @staticmethod
    def centered_at_origin(self, size: Vector) -> 'Rect':
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
    
    def collides(self, other:'Rect')->bool:
        """checks if two rectangles collide with eachother. <br>
        when they touch eachother exactly (f.e. a Rect with position [0] and size [1] and a rect with position [1] and size [1]), the function will return false.

        Args:
            other (Rect): the rectangle which may collide with this rectangle

        Returns:
            bool: true if the two rectangles overlap
        """
        for axis in range(len(self.p0)):
            if self.p0[axis] + self.size[axis] <= other.p0[axis] or other.p0[axis] + other.size[axis] <= self.p0[axis]:
                return False
        return True
    
    def contains(self, other:'Rect')->bool:
        for axis in range(len(self.p0)):
            if other.p0[axis] < self.p0[axis] or other.p0[axis] + other.size[axis] > self.p0[axis] + self.size[axis]:
                return False
        return True
    
    def substractFrom(self, other:'Rect')->list['Rect']:
        """cut the 'other' rectangle in pieces by substracting this rectangle from it

        Args:
            other (Rect): the rectangle to substract this rectangle from

        Returns:
            list[Rect]: a list of up to 4 rectangles for 2d (if the rect is in the center). CAUTION: THEY OVERLAP!
        """
        pieces:list[Rect] = []
        to_clone = other
        #check each axis
        for axis in range(len(self.p0)):
            self_p1 = self.p0[axis] + self.size[axis]
            other_p1 = other.p0[axis] + other.size[axis]
            if self_p1 < other_p1:
                diff = other_p1 - self_p1
                
                piece:Rect = copy.deepcopy(to_clone)
                
                piece.p0[axis] = self_p1
                
                piece.size[axis] = diff
                pieces.append(piece)
                #also crop other.
                #to_clone.size[axis] -= diff
            self_p0 = self.p0[axis]
            other_p0 = other.p0[axis]
            if self_p0 > other_p0:
                diff = self_p0 - other_p0
                piece:Rect = copy.deepcopy(to_clone)
                piece.size[axis] = diff
                pieces.append(piece)
                #to_clone.p0[axis] = self_p0
                #to_clone.size[axis] -= diff
        return pieces
    
    
    def get_corner(self, corner_index: int) -> Point:
        """

        Args:
            corner_index (int): corners are ordered like 0 -> 000, 1 -> 001, 2 -> 010, 011, 100 etc.
            where 0 = the minimum and 1 = the maximum

        Returns:
            Point: a corner
        """
        corner : Point = Point()
        for axis in range(len(self)):
            corner.append(self.p0[axis] + self.size[axis] if corner_index & 1 << axis else self.p0[axis])
        return corner
        

    def corners(self) -> 'list[Point]':
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
        corners:list[Point] = []
        axis_count = len(self.p0)
        for corner_index in range(2 << axis_count):
            corners.append(self.get_corner(corner_index))
        return corners

    def perimeter(self):
        return PolyCurve.by_points(self.corners())
    
    def to_cuboid(self) -> 'Extrusion':
        """Generates an extrusion representing a cuboid from the 3D bounding box dimensions.

        #### Returns:
        `Extrusion`: An Extrusion object that represents a cuboid, matching the dimensions and orientation of the bounding box.

        #### Example usage:
        ```python
        bbox2d = Rect().by_dimensions(length=100, width=50)
        cs = CoordinateSystem()
        bbox3d = BoundingBox3d().convert_boundingbox_2d(bbox2d, cs, height=30)
        cuboid = bbox3d.to_cuboid()
        # Generates a cuboid extrusion based on the 3D bounding box
        ```
        """
        pts = self.corners()
        pc = PolyCurve2D.by_points(pts)
        height = self.height
        cs = self.coordinatesystem
        dirXvector = Vector.angle_between(CSGlobal.Y_axis, cs.Y_axis)
        pcrot = pc.rotate(dirXvector)  # bug multi direction
        cuboid = Extrusion.by_polycurve_height_vector(
            pcrot, height, CSGlobal, cs.Origin, cs.Z_axis)
        return cuboid

    def to_axis(self, length: 'float' = 1000) -> 'list':
        """Generates lines representing the coordinate axes of the bounding box's coordinate system.

        This method creates three Line objects corresponding to the X, Y, and Z axes of the bounding box's coordinate system. Each line extends from the origin of the coordinate system in the direction of the respective axis.

        #### Parameters:
        - `length` (float, optional): The length of each axis line. Defaults to 1000 units.

        #### Returns:
        `list`: A list containing three Line objects representing the X, Y, and Z axes.

        #### Example usage:
        ```python
        # Assuming `bbox3d` is an instance of BoundingBox3d with a defined coordinate system
        axes_lines = bbox3d.to_axis(length=500)
        # This returns a list of three Line objects representing the X, Y, and Z axes of the bounding box's coordinate system, each 500 units long.
        ```
        """
        if length == None:
            length = 1000
        cs = self.coordinatesystem
        lnX = Line.by_startpoint_direction_length(cs.Origin, cs.X_axis, length)
        lnY = Line.by_startpoint_direction_length(cs.Origin, cs.Y_axis, length)
        lnZ = Line.by_startpoint_direction_length(cs.Origin, cs.Z_axis, length)
        return [lnX, lnY, lnZ]
