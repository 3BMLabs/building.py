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


"""This module provides tools to create points."""

__title__ = "point"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/point.py"


import sys
from pathlib import Path
import math

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.coords import Coords
from packages.helper import *

# [!not included in BP singlefile - end]

# from project.fileformat import project


class Point(Coords):
    """Represents a point in 3D space with x, y, and z coordinates."""
    def __init__(self, *args, **kwargs) -> 'Point':
        """Initializes a new Point instance with the given x, y, and z coordinates.

        - `x` (float): X-coordinate of the point.
        - `y` (float): Y-coordinate of the point.
        - `z` (float): Z-coordinate of the point.
        """
        super().__init__(*args, **kwargs)
        self.units = "mm"

    @staticmethod
    def distance_list(points: list['Point']) -> float:
        """Calculates distances between points in a list.
        
        #### Parameters:
        - `points` (list): List of points.

        #### Returns:
        `float`: Total distance calculated between all the points in the list.

        #### Example usage:
    	```python
        point_1 = Point(231, 13, 76)
        point_2 = Point(71, 12.3, -232)
        point_3 = Point(2, 71, -102)
        output = Point.distance_list([point_1, point_2, point_3])
        # [(<geometry.point.Point object at 0x00000226BD9CAB90>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 158.45090722365714), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BA3BCFD0>, 295.78539517697624), (<geometry.point.Point object at 0x00000226BF20F710>, <geometry.point.Point object at 0x00000226BD9CAB90>, 347.07994756251765)]
        ```
        """
        distances = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                distances.append(
                    (points[i], points[j], Point.distance(points[i], points[j])))
        distances.sort(key=lambda x: x[2])
        return distances

    @staticmethod
    def origin(point_1: 'Point', point_2: 'Point') -> 'Point':
        """Computes the midpoint between two points.        
        
        #### Parameters:
        - `point_1` (Point): First point.
        - `point_2` (Point): Second point.
        
        #### Returns:
        `Point`: Midpoint between the two input points.

        #### Example usage:
    	```python
        point_1 = Point(100.23, 182, 19)
        point_2 = Point(81, 0.1, -901)
        output = Point.origin(point_1, point_2)
        # Point(X = 90.615, Y = 91.050, Z = -441.000)
        ```
        """
        return Point(
            (point_1.x + point_2.x) / 2,
            (point_1.y + point_2.y) / 2,
            (point_1.z + point_2.z) / 2
        )

    @staticmethod
    def rotate_XY(point: 'Point', beta: float, dz: float) -> 'Point':
        """Rotates the point about the Z-axis by a given angle.        
        
        #### Parameters:
        - `point` (Point): Point to be rotated.
        - `beta` (float): Angle of rotation in degrees.
        - `dz` (float): Offset in the z-coordinate.

        #### Returns:
        `Point`: Rotated point.

        #### Example usage:
    	```python
        point_1 = Point(19, 30, 12.3)
        output = Point.rotate_XY(point_1, 90, 12)
        # Point(X = -30.000, Y = 19.000, Z = 24.300)
        ```
        """
        return Point(
            math.cos(math.radians(beta))*point.x -
            math.sin(math.radians(beta))*point.y,
            math.sin(math.radians(beta))*point.x +
            math.cos(math.radians(beta))*point.y,
            point.z + dz
        )

    @staticmethod
    def intersect(point_1: 'Point', point_2: 'Point') -> 'bool':
        """Checks if two points intersect.        
        
        #### Parameters:
        - `point_1` (Point): First point.
        - `point_2` (Point): Second point.

        #### Returns:
        `boolean`: True if points intersect, False otherwise.

        #### Example usage:
    	```python
        point_1 = Point(23, 1, 23)
        point_2 = Point(93, 0, -19)
        output = Point.intersect(point_1, point_2)
        # False
        ```
        """
        return point_1.x == point_2.x and point_1.y == point_2.y and point_1.z == point_2.z

    @staticmethod
    def from_matrix(list: list) -> 'Point':
        """Converts a list to a Point object.        
        
        #### Parameters:
        Converts a list to a Point object.

        #### Returns:
        `Point`: Point object created from the list.

        #### Example usage:
    	```python
        point_1 = [19, 30, 12.3]
        output = Point.from_matrix(point_1)
        # Point(X = 19.000, Y = 30.000, Z = 12.300)
        ```
        """
        return Point(list)


class CoordinateSystem:
    """Represents a coordinate system in 3D space defined by an origin point and normalized x, y, and z axis vectors."""
    def __init__(self, origin: Point, x_axis, y_axis, z_axis) -> 'CoordinateSystem':
        """Initializes a new CoordinateSystem instance with the given origin and axis vectors.
        The axis vectors are normalized to ensure they each have a length of 1, providing a standard basis for the coordinate system.

        - `origin` (Point): The origin point of the coordinate system.
        - `x_axis` (Vector): The initial vector representing the X-axis before normalization.
        - `y_axis` (Vector): The initial vector representing the Y-axis before normalization.
        - `z_axis` (Vector): The initial vector representing the Z-axis before normalization.
        """
        from abstract.vector import Vector
        
        self.Origin = origin
        self.X_axis = x_axis
        self.Y_axis = y_axis
        self.Z_axis = z_axis

    @classmethod
    def by_origin(coordinate_system, origin: Point) -> 'CoordinateSystem':
        """Creates a CoordinateSystem with a specified origin.

        #### Parameters:
        - `origin` (`Point`): The origin point of the new coordinate system.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem object with the specified origin.

        #### Example usage:
        ```python

        ```
        """
        from abstract.coordinatesystem import X_axis, Y_Axis, Z_Axis
        return coordinate_system(origin, x_axis=X_axis, y_axis=Y_Axis, z_axis=Z_Axis)

    @staticmethod
    def translate(cs_old, direction):
        """Translates a CoordinateSystem by a given direction vector.

        #### Parameters:
        - `cs_old` (CoordinateSystem): The original coordinate system to be translated.
        - `direction` (Vector): The direction vector along which the coordinate system is to be translated.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem object translated from the original one.

        #### Example usage:
        ```python

        ```
        """

        from abstract.vector import Vector
        new_origin = Point.translate(cs_old.Origin, direction)

        X_axis = Vector(1, 0, 0)

        Y_Axis = Vector(0, 1, 0)

        Z_Axis = Vector(0, 0, 1)

        CSNew = CoordinateSystem(
            new_origin, x_axis=X_axis, y_axis=Y_Axis, z_axis=Z_Axis)

        CSNew.Origin = new_origin
        return CSNew

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    @staticmethod
    def by_point_main_vector(self, new_origin_coordinatesystem: Point, DirectionVectorZ):
        """Creates a new CoordinateSystem at a given point, oriented along a specified direction vector.
        This method establishes a new coordinate system by defining its origin and its Z-axis direction. The X and Y axes are determined based on the given Z-axis to form a right-handed coordinate system. If the calculated X or Y axis has a zero length (in cases of alignment with the global Z-axis), default axes are used.

        #### Parameters:
        - `new_origin_coordinatesystem` (`Point`): The origin point of the new coordinate system.
        - `DirectionVectorZ` (Vector): The direction vector that defines the Z-axis of the new coordinate system.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem object oriented along the specified direction vector with its origin at the given point.

        #### Example usage:
        ```python

        ```
        """
        from abstract.vector import Vector
        vz = DirectionVectorZ
        vz = Vector.normalize(vz)
        vx = Vector.perpendicular(vz)[0]
        try:
            vx = Vector.normalize(vx)
        except:
            vx = Vector(1, 0, 0)
        vy = Vector.perpendicular(vz)[1]
        try:
            vy = Vector.normalize(vy)
        except:
            vy = Vector(0, 1, 0)
        CSNew = CoordinateSystem(new_origin_coordinatesystem, vx, vy, vz)
        return CSNew

    @staticmethod
    def move_local(cs_old, x: float, y: float, z: float):
        """Moves a CoordinateSystem in its local coordinate space by specified displacements.

        #### Parameters:
        - `cs_old` (CoordinateSystem): The original coordinate system to be moved.
        - `x` (float): The displacement along the local X-axis.
        - `y` (float): The displacement along the local Y-axis.
        - `z` (float): The displacement along the local Z-axis.

        #### Returns:
        `CoordinateSystem`: A new CoordinateSystem object moved in its local coordinate space.

        #### Example usage:
        ```python

        ```
        """
        
        from abstract.vector import Vector

        xloc_vect_norm = cs_old.X_axis
        xdisp = Vector.scale(xloc_vect_norm, x)
        yloc_vect_norm = cs_old.X_axis
        ydisp = Vector.scale(yloc_vect_norm, y)
        zloc_vect_norm = cs_old.X_axis
        zdisp = Vector.scale(zloc_vect_norm, z)
        disp = xdisp + ydisp + zdisp
        CS = CoordinateSystem.translate(cs_old, disp)
        return CS

    @staticmethod
    def translate_origin(origin1, origin2):
        """Calculates the translation needed to move from one origin to another.

        #### Parameters:
        - `origin1` (Point): The starting origin point.
        - `origin2` (Point): The ending origin point.

        #### Returns:
        `Point`: A new Point object representing the translated origin.

        #### Example usage:
        ```python
        
        ```
        """
        origin1_n = Point.to_matrix(origin1)
        origin2_n = Point.to_matrix(origin2)

        new_origin_n = origin1_n + (origin2_n - origin1_n)
        return Point(new_origin_n[0], new_origin_n[1], new_origin_n[2])

    @staticmethod
    def calculate_rotation_matrix(xaxis_1, yaxis_1, zaxis_1, xaxis_2, yaxis_2, zaxis_2):
        """Calculates the rotation matrix needed to align one coordinate system with another.

        #### Parameters:
        - `xaxis_1`, `yaxis_1`, `zaxis_1` (Vector): The axes of the initial coordinate system.
        - `xaxis_2`, `yaxis_2`, `zaxis_2` (Vector): The axes of the target coordinate system.

        #### Returns:
        Rotation Matrix (list of lists): A matrix representing the rotation needed to align the first coordinate system with the second.

        #### Example usage:
        ```python
        
        ```
        """
        from abstract.vector import Vector

        R1 = [Vector.to_matrix(xaxis_1), Vector.to_matrix(
            yaxis_1), Vector.to_matrix(zaxis_1)]

        R2 = [Vector.to_matrix(xaxis_2), Vector.to_matrix(
            yaxis_2), Vector.to_matrix(zaxis_2)]

        R1_transposed = list(map(list, zip(*R1)))
        R2_transposed = list(map(list, zip(*R2)))

        rotation_matrix = Vector.dot_product(Vector.from_matrix(
            R2_transposed), Vector.length(Vector.from_matrix(R1_transposed)))
        return rotation_matrix

    @staticmethod
    def normalize(point: Point) -> list:
        """Normalizes a vector to have a length of 1.
        This method calculates the normalized (unit) version of a given vector, making its length equal to 1 while preserving its direction. If the input vector has a length of 0 (i.e., it is a zero vector), the method returns the original vector.

        #### Parameters:
        - `point` (list of float): A vector represented as a list of three floats, corresponding to its x, y, and z components, respectively.

        #### Returns:
        list of float: The normalized vector as a list of three floats. If the original vector is a zero vector, returns the original vector.

        #### Example usage:
        ```python
        
        ```
        """
        norm = (point[0]**2 + point[1]**2 + point[2]**2)**0.5
        return [point[0] / norm, point[1] / norm, point[2] / norm] if norm > 0 else point


def transform_point(point_local: Point, coordinate_system_old: CoordinateSystem, new_origin: Point, direction_vector) -> Point:
    """Transforms a point from one coordinate system to another based on a new origin and a direction vector.
    This function calculates the new position of a point when the coordinate system is changed. The new coordinate system is defined by a new origin point and a direction vector that specifies the orientation of the Z-axis. The X and Y axes are computed to form a right-handed coordinate system. This method takes into account the original position of the point in the old coordinate system to accurately calculate its position in the new coordinate system.

    #### Parameters:
    - `point_local` (Point): The point to be transformed, given in the local coordinate system.
    - `coordinate_system_old` (CoordinateSystem): The original coordinate system the point is in.
    - `new_origin` (Point): The origin of the new coordinate system.
    - `direction_vector` (Vector): The direction vector defining the new Z-axis of the coordinate system.

    #### Returns:
    Point: The transformed point in the new coordinate system.

    #### Example usage:
    ```python
    
    ```
    """
    from abstract.vector import Vector

    direction_vector = Vector.to_matrix(direction_vector)
    new_origin = Point.to_matrix(new_origin)
    vz_norm = Vector.length(Vector(*direction_vector))
    vz = [direction_vector[0] / vz_norm, direction_vector[1] /
          vz_norm, direction_vector[2] / vz_norm]

    vx = [-vz[1], vz[0], 0]
    vx_norm = Vector.length(Vector(*vx))

    if vx_norm == 0:
        vx = [1, 0, 0]
    else:
        vx = [vx[0] / vx_norm, vx[1] / vx_norm, vx[2] / vx_norm]

    vy = Vector.cross_product(Vector(*vz), Vector(*vx))
    vy_norm = Vector.length(vy)
    if vy_norm != 0:
        vy = [vy.x / vy_norm, vy.y / vy_norm, vy.z / vy_norm]
    else:
        vy = [0, 1, 0]

    point_1 = point_local
    CSNew = CoordinateSystem(Point.from_matrix(new_origin), Vector.from_matrix(
        vx), Vector.from_matrix(vy), Vector.from_matrix(vz))
    vector_1 = Point.difference(coordinate_system_old.Origin, CSNew.Origin)

    vector_2 = Vector.product(point_1.x, CSNew.X_axis)
    vector_3 = Vector.product(point_1.y, CSNew.Y_axis)
    vector_4 = Vector.product(point_1.z, CSNew.Z_axis)
    vtot = Vector(vector_1.x + vector_2.x + vector_3.x + vector_4.x, vector_1.y + vector_2.y +
                   vector_3.y + vector_4.y, vector_1.z + vector_2.z + vector_3.z + vector_4.z)
    pointNew = Point.translate(Point(0, 0, 0), vtot)

    return pointNew


def transform_point_2(PointLocal: Point, CoordinateSystemNew: CoordinateSystem) -> Point:
    """Transforms a point from its local coordinate system to a new coordinate system.
    This function translates a point based on its local coordinates (x, y, z) within its current coordinate system to a new position in a specified coordinate system. The transformation involves scaling the local coordinates by the axes vectors of the new coordinate system and sequentially translating the point along these axes vectors starting from the new origin.

    #### Parameters:
    - `PointLocal` (`Point`): The point in its local coordinate system to be transformed.
    - `CoordinateSystemNew` (`CoordinateSystem`): The new coordinate system to which the point is to be transformed.

    #### Returns:
    `Point`: The point transformed into the new coordinate system.

    #### Example usage:
    ```python
    
    ```
    """
    from abstract.vector import Vector
    pn = Point.translate(CoordinateSystemNew.Origin, Vector.scale(
        CoordinateSystemNew.X_axis, PointLocal.x))
    pn2 = Point.translate(pn, Vector.scale(
        CoordinateSystemNew.Y_axis, PointLocal.y))
    pn3 = Point.translate(pn2, Vector.scale(
        CoordinateSystemNew.Z_axis, PointLocal.z))
    return pn3