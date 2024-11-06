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


"""This module provides tools to create curves
"""

import math
import sys
from pathlib import Path
from typing import Self, Union

from abstract.shape import Shape
from abstract.vector import Vector
from geometry.coords import to_array
from geometry.pointlist import PointList
from packages.helper import flatten

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.rect import Rect
from abstract.plane import Plane
from geometry.point import Point
from abstract.serializable import Serializable

# [!not included in BP singlefile - end]

class Line(Serializable):
    def __init__(self, start: Point, end: Point) -> 'Line':
        """Initializes a Line object with the specified start and end points.

        - `start` (Point): The starting point of the line segment.
        - `end` (Point): The ending point of the line segment.
        """
        #copy
        """The starting point of the line segment"""
        self.start = Point(start)
        """The ending point of the line segment."""
        self.end = Point(end)
        
    @property
    def mid(self) -> 'Point':
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
        return[Point(self.start), Point(self.end)]
    
    @property
    def segmentate(self, amount: int) -> list[Point]:
        """returns points along this line.

        Args:
            amount (int): the amount of samples to take

        Returns:
            list[Point]: a list of points sampled along this line
        """
        fraction_multiplier = 1.0 / (amount - 1)
        return [self.point_at_fraction(fraction) for fraction in range(0, 1.00001, fraction_multiplier)]
    
    def point_at_fraction(self, fraction: float) -> Point:
        """

        Args:
            fraction (float): a value from 0 to 1, describing the position in the line.

        Returns:
            Point: self.start for 0, self.end for 1
        """
        return self.start * (1 - fraction) + self.end * fraction
    
    @staticmethod
    def by_startpoint_direction_length(start: 'Point', direction: 'Vector', length: 'float') -> 'Line':
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
        norm = math.sqrt(direction.x ** 2 + direction.y **
                         2 + direction.z ** 2)
        normalized_direction = Vector(
            direction.x / norm, direction.y / norm, direction.z / norm)

        end_x = start.x + normalized_direction.x * length
        end_y = start.y + normalized_direction.y * length
        end_z = start.z + normalized_direction.z * length
        end_point = Point(end_x, end_y, end_z)

        return Line(start, end_point)

    # @classmethod
    def point_at_parameter(self, interval: 'float' = None) -> 'Point':
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
            devBy = 1/interval
            return Point((x1 + x2) / devBy, (y1 + y2) / devBy, (z1 + z2) / devBy)

    def intersects(self, other: 'Line') -> bool:
        """checks if two lines intersect with eachother.

        Args:
            other (Line): the line which may intersect with this rectangle

        Returns:
            bool: true if the lines cross eachother.
        """
        #ax + b = cx + d
        #ax = cx + d - b
        #ax - cx = d - b
        #(a - c)x = d - b
        #x = (d - b) / (a - c)
        
        #calculate a and c
        
        diff_self = self.end - self.start
        diff_other = other.end - other.start
        #a
        slope_self = math.inf if diff_self.x == 0 else diff_self.y / diff_self.x
        
        #c
        slope_other = math.inf if diff_other.x == 0 else diff_other.y / diff_other.x
        #handle edge cases
        #colinear
        if(slope_self == slope_other) :
            return False

        #b
        self_y_at_0 = self.start.y - self.start.x * slope_self
        
        #check if one slope is infinite (both infinite is handled by colinear)
        if other.start.x == other.end.x:
            self_y_at_line = self_y_at_0 + slope_self * other.start.x
            return other.start.y < self_y_at_line < other.end.y

        #d
        other_y_at_0 = other.start.y - other.start.x * slope_other

        if self.start.x == self.end.x:
            other_y_at_line = other_y_at_0 + slope_other * self.start.x
            return self.start.y < other_y_at_line < self.end.y
        
        intersection_x = (other_y_at_0 - self_y_at_0) / (slope_self - slope_other)
        
        return self.start.x < intersection_x < self.end.x

    def split(self, points: 'Union[Point, list[Point]]') -> 'list[Line]':
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
            sorted_points = sorted(
                points, key=lambda p: p.distance(p, self.end))
            lines = create_lines(sorted_points)
            return lines
        elif isinstance(points, Point):
            point = points
            lines.append(Line(start=self.start, end=point))
            lines.append(Line(start=point, end=self.end))
            return lines
        
    @property
    def length(self) -> 'float':
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
        """Computes the direction of the Line object.
        """
        return (self.end - self.start).normalized

    def __str__(self) -> 'str':
        """Returns a string representation of the Line object.

        #### Returns:
        `str`: A string representation of the Line object.

        #### Example usage:
        ```python

        ```          
        """
        return f"{__class__.__name__}(" + f"{self.start}, {self.end})"


def create_lines(points: 'list[Point]') -> 'list[Line]':
    """Creates a list of Line objects from a list of points.
    This function generates line segments connecting consecutive points in the list.

    #### Parameters:
    - `points` (List[Point]): A list of points.

    #### Returns:
    `List[Line]`: A list of Line objects representing the line segments connecting the points.

    #### Example usage:
    ```python

    ```      
    """
    lines = []
    for i in range(len(points)-1):
        line = Line(points[i], points[i+1])
        lines.append(line)
    return lines


class Arc(Line):
    def __init__(self, startPoint: 'Point', midPoint: 'Point', endPoint: 'Point') -> 'Arc':
        """Initializes an Arc object with start, mid, and end points.
        This constructor calculates and assigns the arc's origin, plane, radius, start angle, end angle, angle in radians, area, length, units, and coordinate system based on the input points.
        
        the mid point should really be in the center; we don't support warped arcs.

        - `startPoint` (Point): The starting point of the arc.
        - `midPoint` (Point): The mid point of the arc which defines its curvature.
        - `endPoint` (Point): The ending point of the arc.
        """
        #for the midpoint to be in the middle, the distance between the midpoint and the start and the end should be the same, no matter the angle.
        if not math.isclose(Point.distance_squared(startPoint, midPoint), Point.distance_squared(midPoint, endPoint), rel_tol= 1.0 / 0x100):
            raise ValueError('midpoint is not in the center')
        super().__init__(startPoint, endPoint)
        
        self.mid = midPoint

        #self.origin = self.origin_arc()
        #vector_1 = Vector(x=1, y=0, z=0)
        #vector_2 = Vector(x=0, y=1, z=0)
        #self.plane = Plane.by_two_vectors_origin(
        #    vector_1,
        #    vector_2,
        #    self.origin
        #)
        #self.radius = self.radius_arc()
        #self.startAngle = 0
        #self.endAngle = 0
        #self.angle_radian = self.angle_radian()
        #self.area = 0
        #self.length = self.length()
        #self.units = project.units
        
    @property
    def radius(self) -> 'float':
        """Calculates and returns the radius of the arc.
        The radius is computed based on the distances between the start, mid, and end points of the arc.

        #### Returns:
        `float`: The radius of the arc.

        #### Example usage:
        ```python
        radius = arc.radius_arc()
        # radius will be the calculated radius of the arc
        ```
        """
        a = Point.distance(self.start, self.mid)
        b = Point.distance(self.mid, self.end)
        c = Point.distance(self.end, self.start)
        s = (a + b + c) / 2
        A = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
        
        if abs(A) < 1e-6:
            return float('inf')
        else:
            R = (a * b * c) / (4 * A)
            return R

    @property
    def points(self) -> list[Point]:
        return[Point(self.start), Point(self.mid), Point(self.end)]
            
    #https://calcresource.com/geom-circularsegment.html
    @property
    def area(self) -> 'float':
        return ((self.angle - math.sin(self.angle)) / 2) * (self.radius ** 2)
    
    @property
    def origin(self) -> 'Point':
        """Calculates and returns the origin of the arc.
        The origin is calculated based on the geometric properties of the arc defined by its start, mid, and end points.

        #### Returns:
        `Point`: The calculated origin point of the arc.

        #### Example usage:
        ```python
        origin = arc.origin_arc()
        # origin will be the calculated origin point of the arc
        ```
        """
        start_to_end = self.end - self.start
        half_start_end = start_to_end * 0.5
        b = half_start_end.magnitude
        radius = self.radius
        x = math.sqrt(radius * radius - b * b)
        #mid point as if this was a straight line
        mid = self.start + half_start_end
        #substract the curved mid point from the straight line mid point
        to_center = mid - self.mid
        #change length to x
        to_center.magnitude = x
        center = mid + to_center
        return center

    @property
    def centroid(self) -> 'Point':
        origin = self.origin
        radius = self.radius
        angle = self.angle
        #the distance of the centroid of the arc to its origin
        centroid_distance = (2 / 3) * ((radius * (math.sin(angle) ** 3)) / (angle - math.sin(angle) * math.cos(angle)))
        return origin + centroid_distance * ((self.mid - origin) / radius)
        
    @property
    def angle(self) -> 'float':
        """Calculates and returns the total angle of the arc in radians.
        The angle is determined based on the vectors defined by the start, mid, and end points with respect to the arc's origin.

        #### Returns:
        `float`: The total angle of the arc in radians.

        #### Example usage:
        ```python
        angle = arc.angle_radian()
        # angle will be the total angle of the arc in radians
        ```
        """
        origin = self.origin
        vector_1 = self.end - origin
        vector_2 = self.start - origin
        vector_3 = self.mid - origin
        vector_4 = vector_1 + vector_2
        try:
            v4b = Vector.new_length(vector_4, self.radius)
            if Vector.value(vector_3) == Vector.value(v4b):
                angle = Vector.angle_between(vector_1, vector_2)
            else:
                angle = 2*math.pi-Vector.angle_between(vector_1, vector_2)
            return angle
        except:
            angle = 2*math.pi-Vector.angle_between(vector_1, vector_2)
            return angle
        
    @property
    def length(self) -> 'float':
        """Calculates and returns the length of the arc.
        The length is calculated using the geometric properties of the arc defined by its start, mid, and end points.

        #### Returns:
        `float`: The length of the arc.

        #### Example usage:
        ```python
        length = arc.length()
        # length will be the calculated length of the arc
        ```
        """
        try:
            x1, y1, z1 = self.start.x, self.start.y, self.start.z
            x2, y2, z2 = self.mid.x, self.mid.y, self.mid.z
            x3, y3, z3 = self.end.x, self.end.y, self.end.z

            r1 = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5 / 2
            a = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
            b = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2 + (z3 - z2) ** 2)
            c = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2 + (z3 - z1) ** 2)
            cos_angle = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
            m1 = math.acos(cos_angle)
            arc_length = r1 * m1

            return arc_length
        except:
            return 0
    
    @staticmethod
    def segmented_arc(arc: 'Arc', count: 'int') -> 'list':
        """Divides the arc into segments and returns a list of line segments.
        This method uses the `points_at_parameter` method to generate points along the arc at specified intervals and then creates line segments between these consecutive points.

        #### Parameters:
        - `arc` (Arc): The arc object.
        - `count` (int): The number of segments (and thus the number of points - 1) to create.

        #### Returns:
        `list`: A list of line segments (`Line` objects) representing the divided arc.

        #### Example usage:
        ```python
        arc = Arc(startPoint, midPoint, endPoint)
        segments = Arc.segmented_arc(arc, 3)
        # segments will be a list of 2 lines dividing the arc into 3 segments
        ```
        """
        pnts = Arc.points_at_parameter(arc, count)
        i = 0
        lines = []
        for j in range(len(pnts) - 1):
            lines.append(Line(pnts[i], pnts[i + 1]))
            i = i + 1
        return lines

    def __str__(self) -> 'str':
        """Generates a string representation of the Arc object.

        #### Returns:
        `str`: A string that represents the Arc object.

        #### Example usage:
        ```python
        arc = Arc(startPoint, midPoint, endPoint)
        print(arc)
        # Output: Arc()
        ```
        """
        return f"{__class__.__name__}()"

class Polygon(PointList):
    """Represents a polygon composed of points."""
    def __init__(self, *args) -> 'Polygon':
        
        super().__init__(to_array(*args))


    @property
    def closed(self) -> bool: return self[0] == self[-1]
    
    @property
    def points(self) -> list[Point]:
        return [Point(p) for p in self]
    
    @closed.setter
    def closed(self, value) -> Self:
        """Closes the PolyCurve by connecting the last point to the first point, or opens it by removing the last point if it's a duplicate of the first point
        #### Example usage:
        ```python
            c:PolyCurve = PolyCurve(Point(1,3),Point(4,3),Point(2,6))
            c.closed = true #Point(1,3) just got added to the back of the list
        ```
        """
        if value != self.closed:
            if value:
                #copy. else, when operators are executed, it will execute the operator twice on the same reference
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
        return [Line(self[point_index], self[point_index + 1]) for point_index in range(len(self) - 1)]

    @property
    def is_rectangle(self) -> bool:
        """the polycurve should be wound counter-clockwise and the first line should be in the x direction

        Returns:
            bool: if this curve is a rectangle, i.e. it has 4 corner points
        """
        if len(self) == 4 or self.closed and len(self) == 5:
            if self[0].y == self[1].y and self[1].x == self[2].x and self[2].y == self[3].y and self[3].x == self[0].x:
                return True
        else: return False

    def contains(self, p: 'Point') -> bool:
        """checks if the point is inside the polygon

        Args:
            p (Point): _description_

        Returns:
            bool: _description_
        """
        #yoinked this from stack overflow, looks clean
        #https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
        
        # Ray tracing
        n = len(self)
        inside = False
    
        p1 = self[0]
        for i in range(n + 1 if self.closed else n):
            p2 = self[i % n]
            if p.y > min(p1.y,p2.y):
                if p.y <= max(p1.y,p2.y):
                    if p.x <= max(p1.x,p2.x):
                        if p1.y != p2.y:
                            xints = (p.y-p1.y)*(p2.x-p1.x)/(p2.y-p1.y)+p1.x
                        if p1.x == p2.x or p.x <= xints:
                            inside = not inside
            p1 = p2
    
        return inside

    def intersects(self, other: 'PolyCurve') -> bool:
        """checks if two polycurves intersect with eachother. caution! this is brute force.

        Args:
            other (PolyCurve): the PolyCurve which may intersect with this rectangle

        Returns:
            bool: true if any of the lines of the two polygons cross eachother.
        """
        #before doing such an expensive method, let's check if our bounds cross first.
        if self.bounds.collides(other.bounds):
            other_curves = other.curves
            for c in self.curves:
                for other_c in other_curves:
                    if(c.intersects(other_c)):return True
        return False
    
    def collides(self, other: 'Polygon') -> bool:
        """checks if two polygons collide with eachother.

        Args:
            other (Polygon): the polygon which may collide with this rectangle

        Returns:
            bool: true if two polygons overlap
        """
        #hopefully, most of the time we contain a point of the other.
        return self.contains(other[0]) or other.contains(self[0]) or self.intersects(other)

    @classmethod
    def by_points(self, points: 'list[Point]') -> 'Polygon':
        """Creates a Polygon from a list of points.

        #### Parameters:
        - `points` (list[Point]): The list of points defining the Polygon.

        #### Returns:
        `Polygon`: The created Polygon object.

        #### Example usage:
        ```python

        ```        
        """
        if len(points) < 3:
            print("Error: Polygon must have at least 3 unique points.")
            return None

        _points = []

        for point in points: #Convert all to Point
            if point.type == "Point":
                _points.append(Point(point.x, point.y, 0))
            else:
                _points.append(point)

        if Point.to_matrix(_points[0]) == Point.to_matrix(_points[-1]):
            _points.pop()

        seen = set()
        unique_points = [p for p in _points if not (p in seen or seen.add(p))]

        polygon = Polygon()
        polygon.points = unique_points

        num_points = len(unique_points)
        for i in range(num_points):
            next_index = (i + 1) % num_points
            polygon.curves.append(Line(start=unique_points[i], end=unique_points[next_index]))

        return polygon

    @staticmethod
    def rectangular(rect: Rect) -> 'Polygon':
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
            #2d rectangle
            not_used_axis_index = 2

        axis0 = 1 if not_used_axis_index == 0 else 0
        axis1 = 1 if not_used_axis_index == 2 else 2

        rect_p1 = rect.p1
        curve_p0 = rect.p0
        #clone
        curve_p1 = Point(rect.p0)
        curve_p1[axis0] = rect_p1[axis0]

        curve_p2 = rect_p1
        curve_p3 = Point(rect.p0)
        curve_p3[axis1] = rect_p1[axis1]
        return Polygon(curve_p0, curve_p1, curve_p2, curve_p3)

    @staticmethod
    def by_joined_curves(lines: 'list[Line]') -> 'Polygon':
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
            if lines[i].end != lines[i+1].start:
                raise ValueError("Error: Curves must be contiguous to form a Polygon.")

        #if lines[0].start != lines[-1].end:
        #    lines.append(Line(lines[-1].end, lines[0].start))

        return Polygon([line.start for line in lines] + [lines[-1].end])
    
    @property
    def area(self) -> 'float':  # shoelace formula
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
    def centroid(self) -> 'Point':
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
            
            #https://stackoverflow.com/questions/5271583/center-of-gravity-of-a-polygon
            

            Cx, Cy = 0.0, 0.0
            for i in range(num_points):
                x0, y0 = self[i-1].x, self[i-1].y
                x1, y1 = self[i].x, self[i].y
                factor = (x0 * y1 - x1 * y0)
                Cx += (x0 + x1) * factor
                Cy += (y0 + y1) * factor

            Cx /= (6.0 * area)
            Cy /= (6.0 * area)

            return Point(Cx, Cy)
        else:
            raise ValueError("this polycurve is not closed")

    def length(self) -> 'float':
        """Calculates the total length of the Polygon.

        #### Returns:
        `float`: The total length of the Polygon.

        #### Example usage:
        ```python

        ```
        """
        lst = []
        for line in self.curves:
            lst.append(line.length)

        return sum(i.length for i in self.curves)




    def __str__(self) -> 'str':
        """Returns a string representation of the PolyCurve.

        #### Returns:
        `str`: The string representation of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        return f"{__class__.__name__} (points: {list.__str__(self)})"

class PolyCurve(Serializable, list[Line], Shape):
    """Stores lines, which could possibly be arcs"""
    def __init__(self, *args):
        """Initializes a PolyCurve object, which is unclosed by default.
        

        """
        
        
        #self.points:list[Point] = to_array(*args)

        #self.approximateLength = None
        #self.graphicsStyleId = None
        #self.isCyclic = None
        #self.isElementGeometry = None
        #self.isReadOnly = None
        #self.length = self.length()
        #self.period = None
        #self.reference = None
        #self.visibility = None
        super().__init__(to_array(*args))
    
    @property
    def points(self) -> list[Point]:
        p = []
        for l in self:
            p.extend(l.points)
        return p
    
    @property
    def closed(self) -> 'bool':
        return self[0].start == self[-1].end
    @closed.setter
    def closed(self, value : bool):
        if value != self.closed:
            if value:
                #just fill the gap using a straight line
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
            raise ValueError("the polycurve needs to be closed in order to calculate its area")
        area:float = 0
        for line in self:
            if isinstance(line, Arc):
                origin = line.origin
                area += (line.start.x - line.end.x) * origin.y
                #now that we added the 'rectangle', let's add the sine wave
                
                #the arc is part of a circle. the circle can be represented as two opposite cosine waves, with the circle center being at 0, 0.
                #to calculate the area, we'll be using the integral of the cosine wave, which is the sine wave.
                radius = (line.origin - line.start).magnitude
                
                #area is negative if y < 0
                #area is measured from the -x side here, so at -radius, area == 0 and at +radius, area == circle_area
                #https://www.desmos.com/calculator/ykynwhoue6
                get_area = lambda pos : math.copysign((math.sin(((pos.x - origin.x) / radius) * (math.pi / 2)) + 1) * radius, pos.y - origin.y)
                start_area = get_area(line.start)
                end_area = get_area(line.end)
                
                integral_area = start_area - end_area
                if integral_area < 0:
                    circle_area = (radius * radius) * math.pi
                    integral_area += circle_area
                area += integral_area
            else:
                #check direction of line
                #start - end, for counterclockwiseness
                #when start.x < end.x, this is a bottom line. we'll substract this from the area.
                dx = line.start.x - line.end.x
                averagey = (line.start.y + line.end.y) / 2
                area += dx * averagey
        return area
    
    @property
    def length(self) -> 'float':
        """Calculates the total length of the PolyCurve.

        #### Returns:
        `float`: The total length of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """

        return sum(curve.length for curve in self)

    def scale(self, scale_factor: 'float') -> 'PolyCurve':
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
                arcie = Arc(Point.product(scale_factor, i.start),
                            Point.product(scale_factor, i.end))
                arcie.mid = Point.product(scale_factor, i.mid)
                crvs.append(arcie)
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.product(scale_factor, i.start),
                            Point.product(scale_factor, i.end)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.by_joined_curves(crvs)
        return crv
    
    #TODO finish function
    @property
    def centroid(self) -> 'Point':
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
        
        #now check if any lines are arcs. in that case, we need to adjust the centroid a bit
        
        for i in range(len(self)):
            current_line = self[i]
            if isinstance(current_line, Arc):
                #https://pickedshares.com/en/center-of-area-of-%E2%80%8B%E2%80%8Bgeometric-figures/#circlesegment
                #calculate the centroid
                arc_centroid = current_line.centroid
                arc_area = current_line.area
                
                total_area += arc_area
                #now that we have the centroid, we also need to calculate the area, and multiply the centroid by the area to give it a 'weight'
                weighted_centroid += arc_centroid * arc_area
        
        return weighted_centroid / total_area
    
    #def area(self) -> 'float':  # shoelace formula
    #    """Calculates the area enclosed by the PolyCurve using the shoelace formula.
#
    #    #### Returns:
    #    `float`: The area enclosed by the PolyCurve.
#
    #    #### Example usage:
    #    ```python
#
    #    ```        
    #    """
    #    if self.closed:
    #        if len(self.points) < 3:
    #            return "Polygon has less than 3 points!"
#
    #        num_points = len(self.points)
    #        S1, S2 = 0, 0
#
    #        for i in range(num_points):
    #            x, y = self.points[i].x, self.points[i].y
    #            if i == num_points - 1:
    #                x_next, y_next = self.points[0].x, self.points[0].y
    #            else:
    #                x_next, y_next = self.points[i + 1].x, self.points[i + 1].y
#
    #            S1 += x * y_next
    #            S2 += y * x_next
#
    #        area = 0.5 * abs(S1 - S2)
    #        return area
    #    else:
    #        print("Polycurve is not closed, no area!")
    #        return None
        


    @classmethod
    def by_joined_curves(self, curvelst: 'list[Line]') -> 'PolyCurve':
        """Creates a PolyCurve from a list of joined Line curves.

        #### Parameters:
        - `curvelst` (list[Line]): The list of Line curves to join.

        #### Returns:
        `PolyCurve`: The created PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        for curve in curvelst:
            if curve.length == 0:
                curvelst.remove(curve)
                # print("Error: Curve length cannot be zero.")
                # sys.exit()

        plycrv = PolyCurve()
        for index, curve in enumerate(curvelst):
            if index == 0:
                plycrv.points.append(curve.start)
                plycrv.points.append(curve.end)
            else:
                plycrv.points.append(curve.end)

        return plycrv
    
    @staticmethod
    def by_polygon(polygon: Polygon):
        return PolyCurve(polygon.curves)

    @staticmethod
    def by_points(points: 'list[Point]') -> Self:
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
    def unclosed_by_points(cls, points: 'list[Point]') -> 'PolyCurve':
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

    @staticmethod
    # Create segmented polycurve. Arcs, elips will be translated to straight lines
    def segment(self, count: 'int') -> 'PolyCurve':
        """Segments the PolyCurve into straight lines.

        #### Parameters:
        - `count` (int): The number of segments.

        #### Returns:
        `PolyCurve`: The segmented PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        crvs = []  # add isClosed
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc.segmented_arc(i, count))
            elif i.__class__.__name__ == "Line":
                crvs.append(i)
        crv = flatten(crvs)
        pc = PolyCurve.by_joined_curves(crv)
        return pc

class Circle:
    """Represents a circle with a specific radius, plane, and length.
    """
    def __init__(self, radius: 'float', plane: 'Plane', length: 'float') -> 'Circle':
        """The Circle class defines a circle by its radius, the plane it lies in, and its calculated length (circumference).

        - `radius` (float): The radius of the circle.
        - `plane` (Plane): The plane in which the circle lies.
        - `length` (float): The length (circumference) of the circle. Automatically calculated during initialization.
        """
        self.radius = radius
        self.plane = plane
        self.length = length
        
        pass  # Curve

    def __id__(self):
        """Returns the ID of the Circle.

        #### Returns:
        `str`: The ID of the Circle in the format "id:{self.id}".
        """

    def __str__(self) -> 'str':
        """Generates a string representation of the Circle object.

        #### Returns:
        `str`: A string that represents the Circle object.

        #### Example usage:
        ```python
        circle = Circle(radius, plane, length)
        print(circle)
        # Output: Circle(...)
        ```
        """


class Ellipse:
    """Represents an ellipse defined by its two radii and the plane it lies in."""
    def __init__(self, firstRadius: 'float', secondRadius: 'float', plane: 'Plane') -> 'Ellipse':
        """The Ellipse class describes an ellipse through its major and minor radii and the plane it occupies.
            
        - `firstRadius` (float): The first (major) radius of the ellipse.
        - `secondRadius` (float): The second (minor) radius of the ellipse.
        - `plane` (Plane): The plane in which the ellipse lies.
        """
        self.firstRadius = firstRadius
        self.secondRadius = secondRadius
        self.plane = plane
        
        pass  # Curve

    def __id__(self):
        """Returns the ID of the Ellipse.

        #### Returns:
        `str`: The ID of the Ellipse in the format "id:{self.id}".
        """
        return f"id:{self.id}"

    def __str__(self) -> 'str':
        """Generates a string representation of the Ellipse object.

        #### Returns:
        `str`: A string that represents the Ellipse object.

        #### Example usage:
        ```python
        ellipse = Ellipse(firstRadius, secondRadius, plane)
        print(ellipse)
        # Output: Ellipse(...)
        ```
        """
        return f"{__class__.__name__}({self})"
