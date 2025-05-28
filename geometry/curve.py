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


"""This module provides tools to create curves"""

from abc import abstractmethod
import math
import sys
from pathlib import Path
from typing import Union

from abstract.matrix import Matrix
from abstract.segmentation import SegmentationSettings
from geometry.shape import Shape
from geometry.sphere import Sphere
from abstract.vector import Vector
from abstract.vector import to_array
from geometry.pointlist import PointList
from packages.helper import flatten


from geometry.rect import Rect
from abstract.vector import Point
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]


class Curve(Serializable):
    @property
    @abstractmethod
    def length(self) -> float:
        pass

    @property
    def start(self) -> Point:
        return self.point_at_fraction(0)

    @property
    def mid(self) -> Point:
        return self.point_at_fraction(0.5)

    @property
    def end(self) -> Point:
        return self.point_at_fraction(1)

    @property
    def dimensions(self) -> Point:
        return len(self.start)

    @dimensions.setter
    def dimensions(self, value):
        raise NotImplemented()

    @abstractmethod
    def point_at_fraction(fraction: float) -> Point:
        """
        Args:
            fraction (float): a value from 0 to 1, describing the position in the curve.

        Returns:
            Point: self.start for 0, self.end for 1
        """
        pass

    def segmentate(
        self, settings: SegmentationSettings = SegmentationSettings()
    ) -> "Polygon":
        """

        Args:
            max_angle (float): the maximum angle to keep a straight line. for example, if max_angle = PI/2 and an arc has an angle of PI, it will return 2 line segments.

        Returns:
            list[Point]: a list of points sampled along this line
        """
        segmentated_polygon = Polygon()
        self.segmentate_part(segmentated_polygon, settings)
        segmentated_polygon.append(self.end)
        return segmentated_polygon

    def segmentate_part(
        self, polygon_to_add_to: "Polygon", settings: SegmentationSettings
    ):
        """segmentates this curve as a part of the polygon. will not add self.end to the polygon.

        Args:
            polygon_to_add_to (Polygon): the polygon this curve will be a part of.
        """
        raise NotImplemented()


class Line(Curve):
    def __init__(self, start: Point, end: Point) -> "Line":
        """Initializes a Line object with the specified start and end points.

        - `start` (Point): The starting point of the line segment.
        - `end` (Point): The ending point of the line segment.
        """
        # copy
        """The starting point of the line segment"""
        self._start = Point(start)
        """The ending point of the line segment."""
        self._end = Point(end)

    @property
    def start(self) -> "Point":
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self) -> "Point":
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    @Curve.dimensions.setter
    def dimensions(self, value):
        self._start.dimensions = value
        self._end.dimensions = value

    @property
    def mid(self) -> "Point":
        """Computes the midpoint of the Line object.

        #### Returns:
        `Point`: The midpoint of the Line object.

        #### Example usage:
        ```python

        ```
        """
        return (self.start + self.end) * 0.5

    @property
    def angle(self) -> float:
        return (self.end - self.start).angle

    @property
    def points(self) -> list[Point]:
        return [Point(self.start), Point(self.end)]

    def segmentate_part(self, polygon_to_add_to: "Polygon", max_angle: float):
        polygon_to_add_to.append(Point(self.start))

    def __rmul__(self, transformer) -> "Line":
        return Line(transformer * self.start, transformer * self.end)

    def point_at_fraction(self, fraction: float) -> Point:
        return self.start * (1 - fraction) + self.end * fraction

    @staticmethod
    def by_start_end(start: "Point", end: "Point") -> "Line":
        return Line(start, end)

    @staticmethod
    def by_startpoint_direction_length(
        start: "Point", direction: "Vector", length: "float"
    ) -> "Line":
        """Creates a line segment starting from a given point in the direction of a given vector with a specified length.

        #### Parameters:
        - `start` (Point): The starting point of the line segment.
        - `direction` (Vector): The direction vector of the line segment.
        - `length` (float): The length of the line segment.

        #### Returns:
        `Line`: A new Line object representing the line segment.

        #### Example usage:
        ```python

        ```
        """
        norm = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        normalized_direction = Vector(
            direction.x / norm, direction.y / norm, direction.z / norm
        )

        end_x = start.x + normalized_direction.x * length
        end_y = start.y + normalized_direction.y * length
        end_z = start.z + normalized_direction.z * length
        end_point = Point(end_x, end_y, end_z)

        return Line(start, end_point)

    # @classmethod
    def point_at_parameter(self, interval: "float" = None) -> "Point":
        """Computes the point on the Line object at a specified parameter value.

        #### Parameters:
        - `interval` (float): The parameter value determining the point on the line. Default is None, which corresponds to the midpoint.

        #### Returns:
        `Point`: The point on the Line object corresponding to the specified parameter value.

        #### Example usage:
        ```python

        ```
        """
        if interval == None:
            interval = 0.0
        x1, y1, z1 = self.start.x, self.start.y, self.start.z
        x2, y2, z2 = self.end.x, self.end.y, self.end.z
        if float(interval) == 0.0:
            return self.start
        else:
            devBy = 1 / interval
            return Point((x1 + x2) / devBy, (y1 + y2) / devBy, (z1 + z2) / devBy)

    def intersects(self, other: "Line") -> bool:
        """checks if two lines intersect with eachother.

        Args:
            other (Line): the line which may intersect with this rectangle

        Returns:
            bool: true if the lines cross eachother.
        """
        # ax + b = cx + d
        # ax = cx + d - b
        # ax - cx = d - b
        # (a - c)x = d - b
        # x = (d - b) / (a - c)

        # calculate a and c

        diff_self = self.end - self.start
        diff_other = other.end - other.start
        # a
        slope_self = math.inf if diff_self.x == 0 else diff_self.y / diff_self.x

        # c
        slope_other = math.inf if diff_other.x == 0 else diff_other.y / diff_other.x
        # handle edge cases
        # colinear
        if slope_self == slope_other:
            return False

        # b
        self_y_at_0 = self.start.y - self.start.x * slope_self

        # check if one slope is infinite (both infinite is handled by colinear)
        if other.start.x == other.end.x:
            self_y_at_line = self_y_at_0 + slope_self * other.start.x
            return other.start.y < self_y_at_line < other.end.y

        # d
        other_y_at_0 = other.start.y - other.start.x * slope_other

        if self.start.x == self.end.x:
            other_y_at_line = other_y_at_0 + slope_other * self.start.x
            return self.start.y < other_y_at_line < self.end.y

        intersection_x = (other_y_at_0 - self_y_at_0) / (slope_self - slope_other)

        return self.start.x < intersection_x < self.end.x

    def split(self, points: "Union[Point, list[Point]]") -> "list[Line]":
        """Splits the Line object at the specified point(s).

        #### Parameters:
        - `points` (Point or List[Point]): The point(s) at which the Line object will be split.

        #### Returns:
        `List[Line]`: A list of Line objects resulting from the split operation.

        #### Example usage:
        ```python

        ```
        """
        lines = []
        if isinstance(points, list):
            points.extend([self.start, self.end])
            sorted_points = sorted(points, key=lambda p: p.distance(p, self.end))
            lines = create_lines(sorted_points)
            return lines
        elif isinstance(points, Point):
            point = points
            lines.append(Line(start=self.start, end=point))
            lines.append(Line(start=point, end=self.end))
            return lines

    @property
    def length(self) -> "float":
        """Computes the length of the Line object.

        #### Returns:
        `float`: The length of the Line object.

        #### Example usage:
        ```python

        ```
        """
        return (self.end - self.start).magnitude

    @property
    def direction(self) -> Vector:
        """Computes the direction of the Line object."""
        return (self.end - self.start).normalized

    def __str__(self) -> "str":
        """Returns a string representation of the Line object.

        #### Returns:
        `str`: A string representation of the Line object.

        #### Example usage:
        ```python

        ```
        """
        return f"{__class__.__name__}(" + f"{self.start}, {self.end})"


class Arc(Curve):
    def __init__(self, matrix: "Matrix", angle: float) -> None:
        self.matrix, self.angle = matrix, angle

    @Curve.dimensions.setter
    def dimensions(self, value):
        dimensions = self.dimensions
        if value > dimensions:
            # assuming it's a 4x4 and needs to be a 3x3. remove the 3rd row and column
            self.matrix = self.matrix.minor(value, value)
        else:
            # assuming it's a 3x3 and needs to be a 4x4.
            # insert identity rows
            output_matrix = []

            for row in range(value):
                if row < dimensions - 1:
                    get_row = row
                elif row == value:
                    get_row = dimensions - 1
                else:
                    output_matrix.append([0] * value)
                    continue
                source_row = self.matrix[get_row]
                output_matrix.append(
                    source_row[0 : dimensions - 1]
                    + [0] * (value - dimensions)
                    + source_row[dimensions - 1]
                )

            self.matrix = Matrix(output_matrix)

    @staticmethod
    def by_start_mid_end(start: Point, mid: Point, end: Point) -> "Arc|Line":
        # construct a matrix from a plane
        # x = (start - origin).normalized
        # y
        # https://stackoverflow.com/questions/13977354/build-circle-from-3-points-in-3d-space-implementation-in-c-or-c
        # triangle "edges"
        start_to_mid = mid - start
        start_to_end = end - start
        mid_to_end = end - mid

        # triangle normal
        y_cross = Vector.cross_product(start_to_mid, start_to_end)

        y_length_squared = (
            y_cross.length_squared if len(start) > 2 else y_cross * y_cross
        )
        if y_length_squared < 10e-14:
            return Line(
                start, end
            )  # area of the triangle is too small (you may additionally check the points for colinearity if you are paranoid)

        # helpers
        offset_multiplier = 0.5 / y_length_squared
        # calculate dot products
        tt = Vector.dot_product(start_to_mid, start_to_mid)
        uu = Vector.dot_product(start_to_end, start_to_end)

        # result circle
        origin = (
            start
            + (
                start_to_end * tt * start_to_end.dot_product(mid_to_end)
                - start_to_mid * uu * start_to_mid.dot_product(mid_to_end)
            )
            * offset_multiplier
        )
        # radius = math.sqrt(tt * uu * (mid_to_end*mid_to_end) * iwsl2*0.5)

        x_axis = start - origin
        normalized_x_axis = x_axis.normalized
        radius = x_axis.length

        if len(start) == 2:
            # 2d
            normalized_y_axis = Vector.cross_product(normalized_x_axis)
            arc_matrix = Matrix.by_origin_and_axes(
                origin,
                [
                    x_axis,
                    (normalized_y_axis if y_cross > 0 else -normalized_y_axis) * radius,
                ],
            )
        else:  # 3d

            normalized_z_axis = y_cross / math.sqrt(y_length_squared)
            # TODO: z axis is pointing the other way when the angle is more than PI
            # dot_product = Vector.dot_product(normalized_x_axis, normalized_end_direction)
            # if dot_product >
            normalized_y_axis = Vector.cross_product(
                normalized_z_axis, normalized_x_axis
            )
            # to get the angle, multiply the end point inversely by the matrix and measure its angle.
            arc_matrix = Matrix.by_origin_and_axes(
                origin, [x_axis, normalized_y_axis * radius, normalized_z_axis]
            )
        inverse = arc_matrix.inverse()
        angle = (inverse * end).angle
        if angle < 0:
            angle += math.pi * 2

        return Arc(arc_matrix, angle)

    def segmentate_part(
        self, polygon_to_add_to: "Polygon", settings: SegmentationSettings
    ):
        segment_count = math.ceil(self.angle / settings.max_angle)
        interval = 1.0 / segment_count
        for i in range(segment_count):
            polygon_to_add_to.append(self.point_at_fraction(i * interval))

    @Curve.dimensions.setter
    def dimensions(self, value):
        self.matrix.dimensions

    @property
    def start(self) -> Point:
        """

        Returns:
            Point: the starting point of this arc
        """
        return self.matrix.get_axis(0) + self.matrix.origin

    @property
    def radius(self) -> float:
        """

        Returns:
            Point: the radius of the circle this arc is a part of
        """
        return self.matrix.multiply_without_translation(
            Vector.x_axis if self.matrix.dimensions > 2 else Vector.x_axis_2
        ).magnitude

    @property
    def origin(self) -> Point:
        """

        Returns:
            Point: the center of the circle this arc is a part of
        """
        return self.matrix.translation

    @property
    def length(self) -> float:
        """

        Returns:
            Point: the length of this arc
        """
        return self.angle * self.radius

    def __rmul__(self, transformer) -> "PolyCurve":
        return Arc(transformer * self.matrix, self.angle)

    def point_at_fraction(self, fraction: float):
        """

        #### Example usage:
        ```python
        #counter-clockwise arc with center 0,0
        arc = Arc.by_start_mid_end(Point(-1,0), Point(0,1), Point(1, 0))
        #the point at fraction 0.5 is (0,1)

        #clockwise arc with center 0,0
        arc = Arc.by_start_mid_end(Point(-1,0), Point(0, -1), Point(1, 0))
        #the point at fraction 0.5 is (0,-1)
        ```

        Args:
            fraction (float): a value from 0 (start) to (end)

        Returns:
            Point: a point on the arc at a certain fraction
        """
        angle_vector = Vector.by_angle(self.angle * fraction)
        angle_vector.dimensions = self.matrix.dimensions
        return self.matrix * angle_vector

    @property
    def centroid(self) -> "Point":
        """

        Returns:
            Point: the center of mass of this arc object
        """
        origin = self.origin
        radius = self.radius
        angle = self.angle
        # the distance of the centroid of the arc to its origin
        centroid_distance = (2 / 3) * (
            (radius * (math.sin(angle) ** 3))
            / (angle - math.sin(angle) * math.cos(angle))
        )
        return origin + centroid_distance * ((self.mid - origin) / radius)

    def __str__(self) -> "str":
        """Generates a string representation of the Arc object.

        #### Returns:
        `str`: A string that represents the Arc object.
        """
        return f"{__class__.__name__}.by_start_mid_end(start={self.start}, mid={self.mid}, end={self.end})"


class Polygon(PointList):
    """Represents a polygon composed of points."""

    def __init__(self, *args) -> "Polygon":

        super().__init__(to_array(*args))

    @property
    def closed(self) -> bool:
        return self[0] == self[-1]

    @property
    def points(self) -> list[Point]:
        return [Point(p) for p in self]

    @closed.setter
    def closed(self, value) -> "Polygon":
        """Closes the PolyCurve by connecting the last point to the first point, or opens it by removing the last point if it's a duplicate of the first point
        #### Example usage:
        ```python
            c:PolyCurve = PolyCurve(Point(1,3),Point(4,3),Point(2,6))
            c.closed = true #Point(1,3) just got added to the back of the list
        ```
        """
        if value != self.closed:
            if value:
                # copy. else, when operators are executed, it will execute the operator twice on the same reference
                self.append(Vector(self[0]))
            else:
                del self[-1]
        return self

    @property
    def curves(self) -> list[Line]:
        """this function won't close the polycurve!

        Returns:
            list[Line]: the curves connecting this polycurve
        """
        return [
            Line(self[point_index], self[point_index + 1])
            for point_index in range(len(self) - 1)
        ]

    @property
    def is_rectangle(self) -> bool:
        """the polycurve should be wound counter-clockwise and the first line should be in the x direction

        Returns:
            bool: if this curve is a rectangle, i.e. it has 4 corner points
        """
        if len(self) == 4 or self.closed and len(self) == 5:
            if (
                self[0].y == self[1].y
                and self[1].x == self[2].x
                and self[2].y == self[3].y
                and self[3].x == self[0].x
            ):
                return True
        else:
            return False

    def contains(self, p: "Point") -> bool:
        """checks if the point is inside the polygon

        Args:
            p (Point): _description_

        Returns:
            bool: _description_
        """
        # yoinked this from stack overflow, looks clean
        # https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

        # Ray tracing
        n = len(self)
        inside = False

        p1 = self[0]
        for i in range(n + 1 if self.closed else n):
            p2 = self[i % n]
            if p.y > min(p1.y, p2.y):
                if p.y <= max(p1.y, p2.y):
                    if p.x <= max(p1.x, p2.x):
                        if p1.y != p2.y:
                            xints = (p.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                        if p1.x == p2.x or p.x <= xints:
                            inside = not inside
            p1 = p2

        return inside

    def intersects(self, other: "PolyCurve") -> bool:
        """checks if two polycurves intersect with eachother. caution! this is brute force.

        Args:
            other (PolyCurve): the PolyCurve which may intersect with this rectangle

        Returns:
            bool: true if any of the lines of the two polygons cross eachother.
        """
        # before doing such an expensive method, let's check if our bounds cross first.
        if self.bounds.collides(other.bounds):
            other_curves = other.curves
            for c in self.curves:
                for other_c in other_curves:
                    if c.intersects(other_c):
                        return True
        return False

    def collides(self, other: "Polygon") -> bool:
        """checks if two polygons collide with eachother.

        Args:
            other (Polygon): the polygon which may collide with this rectangle

        Returns:
            bool: true if two polygons overlap
        """
        # hopefully, most of the time we contain a point of the other.
        return (
            self.contains(other[0]) or other.contains(self[0]) or self.intersects(other)
        )

    @classmethod
    def by_points(self, points: "list[Point]") -> "Polygon":
        """Creates a Polygon from a list of points.

        #### Parameters:
        - `points` (list[Point]): The list of points defining the Polygon.

        #### Returns:
        `Polygon`: The created Polygon object.

        #### Example usage:
        ```python

        ```
        """
        return Polygon(points)

    @staticmethod
    def rectangular(rect: Rect) -> "Polygon":
        """Creates a rectangle in a given plane.

        #### Parameters:
        - `rect` (Rect): The rectangle to use as reference. one axis of its size should be 0 or a ValueError will occur!
        - `width` (float): The width of the rectangle.
        - `height` (float): The height of the rectangle.

        #### Returns:
        `Polygon`: The rectangle Polygon.

        #### Example usage:
        ```python
        ```
        """
        try:
            not_used_axis_index = rect.size.index(0)
        except:
            # 2d rectangle
            not_used_axis_index = 2

        axis0 = 1 if not_used_axis_index == 0 else 0
        axis1 = 1 if not_used_axis_index == 2 else 2

        rect_p1 = rect.p1
        curve_p0 = rect.p0
        # clone
        curve_p1 = Point(rect.p0)
        curve_p1[axis0] = rect_p1[axis0]

        curve_p2 = rect_p1
        curve_p3 = Point(rect.p0)
        curve_p3[axis1] = rect_p1[axis1]
        return Polygon(curve_p0, curve_p1, curve_p2, curve_p3)

    @staticmethod
    def by_joined_curves(lines: "list[Line]") -> "Polygon":
        """returns an unclosed polygon from the provided lines, with each point being the starting point of each line.
        creates a shallow copy of the lines provided!

        Args:
            lines (list[Line]): the starting point of every line provided will be used. segments are expected to be continuous. (lines[0].end == lines[1].start)

        Returns:
            Polygon: an unclosed polygon.
        """
        if not lines:
            print("Error: At least one curve is required to form a Polygon.")
            sys.exit()

        for i in range(len(lines) - 1):
            if lines[i].end != lines[i + 1].start:
                raise ValueError("Error: Curves must be contiguous to form a Polygon.")

        return Polygon([line.start for line in lines] + [lines[-1].end])

    @property
    def area(self) -> "float":  # shoelace formula
        """Calculates the area enclosed by the Polygon using the shoelace formula.

        #### Returns:
        `float`: The area enclosed by the Polygon.

        #### Example usage:
        ```python

        ```
        """
        if len(self) < 3:
            return "Polygon has less than 3 points!"

        num_points = len(self)
        S1, S2 = 0, 0

        for i in range(num_points):
            S1 += self[i - 1].x * self[i].y
            S2 += self[i - 1].y * self[i].x

        area = 0.5 * abs(S1 - S2)
        return area

    @property
    def centroid(self) -> "Point":
        """Calculates the centroid of the Polygon in 2D. we assume that the polygon doesn't intersect itself.

        #### Returns:
        `Point`: The centroid point of the Polygon.

        #### Example usage:
        ```python

        ```
        """
        if self.closed:
            num_points = len(self)
            if num_points < 3:
                return "Polygon has less than 3 points!"

            area = self.area

            # https://stackoverflow.com/questions/5271583/center-of-gravity-of-a-polygon

            Cx, Cy = 0.0, 0.0
            for i in range(num_points):
                x0, y0 = self[i - 1].x, self[i - 1].y
                x1, y1 = self[i].x, self[i].y
                factor = x0 * y1 - x1 * y0
                Cx += (x0 + x1) * factor
                Cy += (y0 + y1) * factor

            Cx /= 6.0 * area
            Cy /= 6.0 * area

            return Point(Cx, Cy)
        else:
            raise ValueError("this polycurve is not closed")

    @property
    def length(self) -> "float":
        """Calculates the total length of the Polygon.

        #### Returns:
        `float`: The total length of the Polygon.

        #### Example usage:
        ```python

        ```
        """
        lst = []
        for line in self.lines:
            lst.append(line.length)

        return sum(i.length for i in self.lines)

    def __str__(self) -> "str":
        """Returns a string representation of the PolyCurve.

        #### Returns:
        `str`: The string representation of the PolyCurve.

        #### Example usage:
        ```python

        ```
        """
        return f"{__class__.__name__} (points: {list.__str__(self)})"


class PolyCurve(list[Line], Shape, Curve):
    """Stores lines, which could possibly be arcs"""

    def __init__(self, *args):
        """Initializes a PolyCurve object, which is unclosed by default."""

        super().__init__(to_array(*args))

    # properties
    @property
    def start(self):
        return self[0].start

    @property
    def end(self):
        return self[-1].end

    @property
    def points(self) -> list[Point]:
        p = []
        for l in self:
            # TODO: remove duplicate points
            p.extend(l.points)
        return p

    @property
    def closed(self) -> "bool":
        return self[0].start == self[-1].end

    @closed.setter
    def closed(self, value: bool):
        if value != self.closed:
            if value:
                # just fill the gap using a straight line
                self.append(Line(self[-1].end, self[0].start))
            else:
                del self[-1]

    @property
    def area(self):
        """Calculates the area of the 2d PolyCurve.

        Returns:
            float: The area of the 2d poly curve.

        we are assuming the PolyCurve is wound counter-clockwise and is closed.
        """
        if not self.closed:
            raise ValueError(
                "the polycurve needs to be closed in order to calculate its area"
            )
        area: float = 0
        for line in self:
            if isinstance(line, Arc):
                origin = line.origin
                area += (line.start.x - line.end.x) * origin.y
                # now that we added the 'rectangle', let's add the sine wave

                # the arc is part of a circle. the circle can be represented as two opposite cosine waves, with the circle center being at 0, 0.
                # to calculate the area, we'll be using the integral of the cosine wave, which is the sine wave.
                radius = (line.origin - line.start).magnitude

                # area is negative if y < 0
                # area is measured from the -x side here, so at -radius, area == 0 and at +radius, area == circle_area
                # https://www.desmos.com/calculator/ykynwhoue6
                get_area = lambda pos: math.copysign(
                    (math.sin(((pos.x - origin.x) / radius) * (math.pi / 2)) + 1)
                    * radius,
                    pos.y - origin.y,
                )
                start_area = get_area(line.start)
                end_area = get_area(line.end)

                integral_area = start_area - end_area
                if integral_area < 0:
                    circle_area = (radius * radius) * math.pi
                    integral_area += circle_area
                area += integral_area
            else:
                # check direction of line
                # start - end, for counterclockwiseness
                # when start.x < end.x, this is a bottom line. we'll substract this from the area.
                dx = line.start.x - line.end.x
                averagey = (line.start.y + line.end.y) / 2
                area += dx * averagey
        return area

    @property
    def length(self) -> "float":
        """Calculates the total length of the PolyCurve.

        #### Returns:
        `float`: The total length of the PolyCurve.

        #### Example usage:
        ```python

        ```
        """

        return sum(curve.length for curve in self)

    # operators
    def __rmul__(self, transformer) -> "PolyCurve":
        return PolyCurve([transformer * curve for curve in self])

    # functions
    def segmentate_part(
        self, polygon_to_add_to: "Polygon", settings: SegmentationSettings
    ):
        for curve in self:
            curve.segmentate_part(polygon_to_add_to, settings)

    def scale(self, scale_factor: "float") -> "PolyCurve":
        """Scales the PolyCurve object by the given factor.

        #### Parameters:
        - `scale_factor`: The scaling factor.

        #### Returns:
        `PolyCurve`: Scaled PolyCurve object.

        #### Example usage:
        ```python

        ```
        """
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                arcie = Arc(scale_factor * i.start, scale_factor * i.end)
                arcie.mid = scale_factor * i.mid
                crvs.append(arcie)
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(scale_factor * i.start, scale_factor * i.end))
            else:
                print("Curvetype not found")
        crv = PolyCurve.by_joined_curves(crvs)
        return crv

    # static functions
    # TODO finish function
    @property
    def centroid(self) -> "Point":
        """Calculates the centroid of the PolyCurve. in 2D

        #### Returns:
        `Point`: The centroid point of the PolyCurve.

        #### Example usage:
        ```python

        ```
        """
        poly = Polygon.by_joined_curves(self)
        total_area = poly.area
        weighted_centroid = poly.centroid * total_area

        # now check if any lines are arcs. in that case, we need to adjust the centroid a bit

        for i in range(len(self)):
            current_line = self[i]
            if isinstance(current_line, Arc):
                # https://pickedshares.com/en/center-of-area-of-%E2%80%8B%E2%80%8Bgeometric-figures/#circlesegment
                # calculate the centroid
                arc_centroid = current_line.centroid
                arc_area = current_line.area

                total_area += arc_area
                # now that we have the centroid, we also need to calculate the area, and multiply the centroid by the area to give it a 'weight'
                weighted_centroid += arc_centroid * arc_area

        return weighted_centroid / total_area

    @classmethod
    def by_joined_curves(self, curvelst: "list[Curve]") -> "PolyCurve":
        """Creates a PolyCurve from a list of joined Line curves.

        #### Parameters:
        - `curvelst` (list[Line]): The list of Line curves to join.

        #### Returns:
        `PolyCurve`: The created PolyCurve object.

        #### Example usage:
        ```python

        ```
        """
        return PolyCurve(curvelst)

    @staticmethod
    def by_polygon(polygon: Polygon):
        return PolyCurve(polygon.curves)

    @staticmethod
    def by_points(points: "list[Point]") -> "PolyCurve":
        """Creates a PolyCurve from a list of points.

        #### Parameters:
        - `points` (list[Point]): The list of points defining the PolyCurve.

        #### Returns:
        `PolyCurve`: The created PolyCurve object.

        #### Example usage:
        ```python

        ```
        """
        return PolyCurve(Polygon(points).curves)

    @classmethod
    def unclosed_by_points(cls, points: "list[Point]") -> "PolyCurve":
        """Creates an unclosed PolyCurve from a list of points.

        #### Parameters:
        - `points` (list[Point]): The list of points defining the PolyCurve.

        #### Returns:
        `PolyCurve`: The created unclosed PolyCurve object.

        #### Example usage:
        ```python

        ```
        """
        plycrv = PolyCurve()
        for index, point in enumerate(points):
            plycrv.points.append(point)
            try:
                nextpoint = points[index + 1]
                plycrv.curves.append(Line(start=point, end=nextpoint))
            except:
                pass
        return plycrv
