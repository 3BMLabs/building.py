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


"""This module provides tools to create 2D profiles 
"""

__title__ = "geometry2d"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/geometry2d.py"


import sys, math
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from packages.helper import *
from abstract.vector import Vector
from geometry.point import transform_point_2
from abstract.plane import Plane
from abstract.coordinatesystem import CoordinateSystem
from project.fileformat import project
# [!not included in BP singlefile - end]


class Vector2:
    def __init__(self, x, y) -> None:
        self.id = generateID()
        self.type = __class__.__name__
        self.x: float = 0.0
        self.y: float = 0.0
        self.x = x
        self.y = y

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def deserialize(data):
        x = data['x']
        y = data['y']
        return Vector2(x, y)

    @staticmethod
    def by_two_points(p1, p2):
        return Vector2(
            p2.x-p1.x,
            p2.y-p1.y
        )

    @staticmethod
    def length(v1):
        return math.sqrt(v1.x * v1.x + v1.y * v1.y)

    @staticmethod
    def scale(v1, scalefactor):
        return Vector2(
            v1.x * scalefactor,
            v1.y * scalefactor
        )

    @staticmethod
    def normalize(v1, axis=-1, order=2):
        v1_mat = Vector2.to_matrix(v1)
        l2_norm = math.sqrt(v1_mat[0]**2 + v1_mat[1]**2)
        if l2_norm == 0:
            l2_norm = 1

        normalized_v = [v1_mat[0] / l2_norm, v1_mat[1] / l2_norm]

        return Vector2(normalized_v[0], normalized_v[1])

    @staticmethod
    def to_matrix(self):
        return [self.x, self.y]

    @staticmethod
    def from_matrix(self):
        return Vector2(self[0], self[1])

    @staticmethod  # inwendig product, if zero, then vectors are perpendicular
    def dot_product(v1, v2):
        return v1.x*v2.x+v1.y*v2.y

    @staticmethod
    def angle_between(v1, v2):
        return math.degrees(math.acos((Vector2.dot_product(v1, v2)/(Vector2.length(v1) * Vector2.length(v2)))))

    @staticmethod
    def angle_radian_between(v1, v2):
        return math.acos((Vector2.dot_product(v1, v2)/(Vector2.length(v1) * Vector2.length(v2))))

    @staticmethod  # Returns vector perpendicular on the two vectors
    def cross_product(v1, v2):
        return Vector(
            v1.y - v2.y,
            v2.x - v1.x,
            v1.x*v2.y - v1.y*v2.x
        )

    @staticmethod
    def reverse(v1):
        return Vector2(
            v1.x*-1,
            v1.y*-1
        )

    @staticmethod
    def sum(vector_1: 'Vector2', vector_2: 'Vector2') -> 'Vector2':
        """Adds two vectors element-wise.        
        
        #### Parameters:
        - `vector_1` (Vector2): First vector.
        - `vector_2` (Vector2): Second vector.

        Returns:
        `Vector2`: Sum of the two input vectors.

        #### Example usage:

        ```python
        vector_1 = Vector2(19, 18)
        vector_2 = Vector2(8, 17)
        output = Vector2.sum(vector_1, vector_2)
        # Vector()
        ```
        """
        return Vector2(
            vector_1.x + vector_2.x,
            vector_1.y + vector_2.y
        )

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}(X = {self.x:.3f}, Y = {self.y:.3f})"


class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.id = generateID()
        self.type = __class__.__name__
        self.x = x
        self.y = y
        self.x = float(x)
        self.y = float(y)
        self.value = self.x, self.y
        self.units = "mm"

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def deserialize(data):
        x = data['x']
        y = data['y']
        return Point2D(x, y)

    def __id__(self):
        return f"id:{self.id}"

    def translate(self, vector: Vector2):
        x = self.x + vector.x
        y = self.y + vector.y
        p1 = Point2D(x, y)
        return p1

    @staticmethod
    def dot_product(p1, p2):
        return p1.x*p2.x+p1.y*p2.y

    def rotate(self, rotation):
        x = self.x
        y = self.y
        r = math.sqrt(x * x + y * y)
        rotationstart = math.degrees(math.atan2(y, x))
        rotationtot = rotationstart + rotation
        xn = round(math.cos(math.radians(rotationtot)) * r, 3)
        yn = round(math.sin(math.radians(rotationtot)) * r, 3)
        p1 = Point2D(xn, yn)
        return p1

    def __str__(self) -> str:
        return f"{__class__.__name__}(X = {self.x:.3f}, Y = {self.y:.3f})"

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    @staticmethod
    def midpoint(point1, point2):
        return Point2D((point2.x-point1.x)/2, (point2.y-point1.y)/2)

    @staticmethod
    def to_pixel(point1, Xmin, Ymin, TotalWidth, TotalHeight, ImgWidthPix: int, ImgHeightPix: int):
        # Convert Point to pixel on a image given a deltaX, deltaY, Width of the image etc.
        x = point1.x
        y = point1.y
        xpix = math.floor(((x - Xmin) / TotalWidth) * ImgWidthPix)
        # min vanwege coord stelsel Image.Draw
        ypix = ImgHeightPix - \
            math.floor(((y - Ymin) / TotalHeight) * ImgHeightPix)
        return xpix, ypix


def transform_point_2D(PointLocal1: Point2D, CoordinateSystemNew: CoordinateSystem):
    # Transform point from Global Coordinatesystem to a new Coordinatesystem
    # CSold = CSGlobal
    from abstract.vector import Vector
    from geometry.point import Point
    PointLocal = Point(PointLocal1.x, PointLocal1.y, 0)
    # pn = Point.translate(CoordinateSystemNew.Origin, Vector.scale(CoordinateSystemNew.Xaxis, PointLocal.x))
    # pn2 = Point2D.translate(pn, Vector.scale(CoordinateSystemNew.Y_axis, PointLocal.y))
    pn3 = Point2D.translate(PointLocal, Vector2(
        CoordinateSystemNew.Origin.x, CoordinateSystemNew.Origin.y))
    # pn3 = Point2D(pn.x,pn.y)
    return pn3


class Line2D:
    def __init__(self, start, end) -> None:
        self.type = __class__.__name__
        self.start: Point2D = start
        self.end: Point2D = end
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        self.dx = self.start.x-self.end.x
        self.dy = self.start.y-self.end.y
        self.vector2: Vector2 = Vector2.by_two_points(self.start, self.end)
        self.vector2_normalised = Vector2.normalize(self.vector2)
        self.length = self.length()
        self.id = generateID()

    def serialize(self):
        return {
            'type': self.type,
            'start': self.start.serialize(),
            'end': self.end.serialize(),
            'x': self.x,
            'y': self.y,
            'dx': self.dx,
            'dy': self.dy,
            'length': self.length,
            'id': self.id
        }

    @staticmethod
    def deserialize(data):
        start_point = Point2D.deserialize(data['start'])
        end_point = Point2D.deserialize(data['end'])
        return Line2D(start_point, end_point)

    def __id__(self):
        return f"id:{self.id}"

    def mid_point(self):
        vect = Vector2.scale(self.vector2, 0.5)
        mid = Point2D.translate(self.start, vect)
        return mid

    def length(self):
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy))

    def f_line(self):
        # returns line for Folium(GIS)
        return [[self.start.y, self.start.x], [self.end.y, self.end.x]]

    def __str__(self):
        return f"{__class__.__name__}(" + f"Start: {self.start}, End: {self.end})"


# class Arc2D:
#     def __init__(self, pntxy1, pntxy2, pntxy3) -> None:
#         self.id = generateID()
#         self.type = __class__.__name__
#         self.start: Point2D = pntxy1
#         self.mid: Point2D = pntxy2
#         self.end: Point2D = pntxy3
#         self.origin = self.origin_arc()
#         self.angle_radian = self.angle_radian()
#         self.radius = self.radius_arc()
#         self.normal = Vector(0, 0, 1)
#         self.xdir = Vector(1, 0, 0)
#         self.ydir = Vector(0, 1, 0)
#         self.coordinatesystem = self.coordinatesystem_arc()

#     def serialize(self):
#         id_value = str(self.id) if not isinstance(
#             self.id, (str, int, float)) else self.id
#         return {
#             'id': id_value,
#             'type': self.type,
#             'start': self.start.serialize(),
#             'mid': self.mid.serialize(),
#             'end': self.end.serialize(),
#             'origin': self.origin,
#             'angle_radian': self.angle_radian,
#             'coordinatesystem': self.coordinatesystem
#         }

#     @staticmethod
#     def deserialize(data):
#         start_point = Point2D.deserialize(data['start'])
#         mid_point = Point2D.deserialize(data['mid'])
#         end_point = Point2D.deserialize(data['end'])
#         arc = Arc2D(start_point, mid_point, end_point)

#         arc.origin = data.get('origin')
#         arc.angle_radian = data.get('angle_radian')
#         arc.coordinatesystem = data.get('coordinatesystem')

#         return arc

#     def __id__(self):
#         return f"id:{self.id}"

#     def points(self):
#         # returns point on the curve
#         return (self.start, self.mid, self.end)

#     def coordinatesystem_arc(self):
#         vx2d = Vector2.by_two_points(self.origin, self.start)  # Local X-axe
#         vx = Vector(vx2d.x, vx2d.y, 0)
#         vy = Vector(vx.y, vx.x * -1, 0)
#         vz = Vector(0, 0, 1)
#         self.coordinatesystem = CoordinateSystem(self.origin, Vector.normalize(
#             vx), Vector.normalize(vy), Vector.normalize(vz))
#         return self.coordinatesystem

#     def angle_radian(self):
#         v1 = Vector2.by_two_points(self.origin, self.end)
#         v2 = Vector2.by_two_points(self.origin, self.start)
#         angle = Vector2.angle_radian_between(v1, v2)
#         return angle

#     def origin_arc(self):
#         # calculation of origin of arc #Todo can be simplified for sure
#         Vstartend = Vector2.by_two_points(self.start, self.end)
#         halfVstartend = Vector2.scale(Vstartend, 0.5)
#         # half distance between start and end
#         b = 0.5 * Vector2.length(Vstartend)
#         try:
#             # distance from start-end line to origin
#             x = math.sqrt(Arc2D.radius_arc(self) *
#                           Arc2D.radius_arc(self) - b * b)
#         except:
#             x = 0
#         mid = Point2D.translate(self.start, halfVstartend)
#         v2 = Vector2.by_two_points(self.mid, mid)
#         v3 = Vector2.normalize(v2)
#         tocenter = Vector2.scale(v3, x)
#         center = Point2D.translate(mid, tocenter)
#         self.origin = center
#         return center

#     def radius_arc(self):
#         a = Vector2.length(Vector2.by_two_points(self.start, self.mid))
#         b = Vector2.length(Vector2.by_two_points(self.mid, self.end))
#         c = Vector2.length(Vector2.by_two_points(self.end, self.start))
#         s = (a + b + c) / 2
#         A = math.sqrt(s * (s-a) * (s-b) * (s-c))
#         R = (a * b * c) / (4 * A)
#         return R

#     @staticmethod
#     def points_at_parameter(arc, count: int):
#         # ToDo can be simplified. Now based on the 3D variant
#         d_alpha = arc.angle_radian / (count - 1)
#         alpha = 0
#         pnts = []
#         for i in range(count):
#             pnts.append(Point2D(arc.radius * math.cos(alpha),
#                         arc.radius * math.sin(alpha)))
#             alpha = alpha + d_alpha
#         CSNew = arc.coordinatesystem
#         pnts2 = []
#         for i in pnts:
#             pnts2.append(transform_point_2D(i, CSNew))
#         return pnts2

#     @staticmethod
#     def segmented_arc(arc, count):
#         pnts = Arc2D.points_at_parameter(arc, count)
#         i = 0
#         lines = []
#         for j in range(len(pnts)-1):
#             lines.append(Line2D(pnts[i], pnts[i+1]))
#             i = i + 1
#         return lines

#     def __str__(self):
#         return f"{__class__.__name__}({self.start},{self.mid},{self.end})"


class Arc2D:
    def __init__(self, startPoint: 'Point2D', midPoint: 'Point2D', endPoint: 'Point2D') -> 'Arc2D':
        """Initializes an Arc object with start, mid, and end points.
        This constructor calculates and assigns the arc's origin, plane, radius, start angle, end angle, angle in radians, area, length, units, and coordinate system based on the input points.

        - `startPoint` (Point2D): The starting point of the arc.
        - `midPoint` (Point2D): The mid point of the arc which defines its curvature.
        - `endPoint` (Point2D): The ending point of the arc.
        """
        self.id = generateID()
        self.type = __class__.__name__
        self.start = startPoint
        self.mid = midPoint
        self.end = endPoint
        self.origin = self.origin_arc()
        vector_1 = Vector(x=1, y=0, z=0)
        vector_2 = Vector(x=0, y=1, z=0)
        self.plane = Plane.by_two_vectors_origin(
            vector_1,
            vector_2,
            self.origin
        )
        self.radius = self.radius_arc()
        self.startAngle = 0
        self.endAngle = 0
        self.angle_radian = self.angle_radian()
        self.area = 0
        self.length = self.length()
        self.units = project.units
        self.coordinatesystem = None #self.coordinatesystem_arc()

    def distance(self, point_1: 'Point2D', point_2: 'Point2D') -> float:
        """Calculates the Euclidean distance between two points in 3D space.

        #### Parameters:
        - `point_1` (Point2D): The first point.
        - `point_2` (Point2D): The second point.

        #### Returns:
        `float`: The Euclidean distance between `point_1` and `point_2`.

        #### Example usage:
        ```python
        point1 = Point2D(1, 2)
        point2 = Point2D(4, 5)
        distance = arc.distance(point1, point2)
        # distance will be the Euclidean distance between point1 and point2
        ```
        """
        return math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2)

    def coordinatesystem_arc(self) -> 'CoordinateSystem':
        """Calculates and returns the coordinate system of the arc.
        The coordinate system is defined by the origin of the arc and the normalized vectors along the local X, Y, and Z axes.

        #### Returns:
        `CoordinateSystem`: The coordinate system of the arc.

        #### Example usage:
        ```python
        coordinatesystem = arc.coordinatesystem_arc()
        # coordinatesystem will be an instance of CoordinateSystem representing the arc's local coordinate system
        ```
        """
        vx = Vector2.by_two_points(self.origin, self.start)  # Local X-axe
        vector_2 = Vector2.by_two_points(self.end, self.origin)
        vz = Vector2.cross_product(vx, vector_2)  # Local Z-axe
        vy = Vector2.cross_product(vx, vz)  # Local Y-axe
        self.coordinatesystem = CoordinateSystem(self.origin, Vector2.normalize(vx), Vector2.normalize(vy),
                                                 Vector2.normalize(vz))
        return self.coordinatesystem

    def radius_arc(self) -> 'float':
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
        a = self.distance(self.start, self.mid)
        b = self.distance(self.mid, self.end)
        c = self.distance(self.end, self.start)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s - a) * (s - b) * (s - c))
        R = (a * b * c) / (4 * A)
        return R

    def origin_arc(self) -> 'Point2D':
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
        # calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector2.by_two_points(self.start, self.end)
        halfVstartend = Vector2.scale(Vstartend, 0.5)
        # half distance between start and end
        b = 0.5 * Vector2.length(Vstartend)
        # distance from start-end line to origin
        # print(Arc2D.radius_arc(self), Arc2D.radius_arc(self), b)
        try:
            x = math.sqrt(Arc2D.radius_arc(self) * Arc2D.radius_arc(self) - b * b)
        except:
            x = 0
        mid = Point2D.translate(self.start, halfVstartend)
        vector_2 = Vector2.by_two_points(self.mid, mid)
        vector_3 = Vector2.normalize(vector_2)
        tocenter = Vector2.scale(vector_3, x)
        center = Point2D.translate(mid, tocenter)
        return center

    def angle_radian(self) -> 'float':
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
        vector_1 = Vector2.by_two_points(self.origin, self.end)
        vector_2 = Vector2.by_two_points(self.origin, self.start)
        vector_3 = Vector2.by_two_points(self.origin, self.mid)
        vector_4 = Vector2.sum(vector_1, vector_2)
        try:
            v4b = Vector2.new_length(vector_4, self.radius)
            if Vector2.value(vector_3) == Vector2.value(v4b):
                angle = Vector2.angle_radian_between(vector_1, vector_2)
            else:
                angle = 2*math.pi-Vector2.angle_radian_between(vector_1, vector_2)
            return angle
        except:
            angle = 2*math.pi-Vector2.angle_radian_between(vector_1, vector_2)
            return angle

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
        x1, y1, z1 = self.start.x, self.start.y, 0
        x2, y2, z2 = self.mid.x, self.mid.y, 0
        x3, y3, z3 = self.end.x, self.end.y, 0

        r1 = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5 / 2
        a = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        b = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2 + (z3 - z2) ** 2)
        c = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2 + (z3 - z1) ** 2)
        cos_angle = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        m1 = math.acos(cos_angle)
        arc_length = r1 * m1

        return arc_length

    @staticmethod
    def points_at_parameter(arc: 'Arc2D', count: 'int') -> 'list':
        """Generates a list of points along the arc at specified intervals.
        This method divides the arc into segments based on the `count` parameter and calculates points at these intervals along the arc.

        #### Parameters:
        - `arc` (Arc2D): The arc object.
        - `count` (int): The number of points to generate along the arc.

        #### Returns:
        `list`: A list of points (`Point2D` objects) along the arc.

        #### Example usage:
        ```python
        arc = Arc2D(startPoint, midPoint, endPoint)
        points = Arc2D.points_at_parameter(arc, 5)
        # points will be a list of 5 points along the arc
        ```
        """
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angle_radian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point2D(arc.radius * math.cos(alpha),
                        arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        cs_new = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transform_point_2(i, cs_new))
        return pnts2

    @staticmethod
    def segmented_arc(arc: 'Arc2D', count: 'int') -> 'list':
        """Divides the arc into segments and returns a list of line segments.
        This method uses the `points_at_parameter` method to generate points along the arc at specified intervals and then creates line segments between these consecutive points.

        #### Parameters:
        - `arc` (Arc2D): The arc object.
        - `count` (int): The number of segments (and thus the number of points - 1) to create.

        #### Returns:
        `list`: A list of line segments (`Line` objects) representing the divided arc.

        #### Example usage:
        ```python
        arc = Arc2D(startPoint, midPoint, endPoint)
        segments = Arc2D.segmented_arc(arc, 3)
        # segments will be a list of 2 lines dividing the arc into 3 segments
        ```
        """
        pnts = Arc2D.points_at_parameter(arc, count)
        i = 0
        lines = []
        for j in range(len(pnts) - 1):
            lines.append(Line2D(pnts[i], pnts[i + 1]))
            i = i + 1
        return lines

    def draw_arc_point(cx: 'float', cy: 'float', radius: 'float', angle_degrees: 'float') -> 'Point2D':
        """
        Calculates a point on the arc given its center, radius, and an angle in degrees.

        Parameters:
        - cx (float): The x-coordinate of the arc's center.
        - cy (float): The y-coordinate of the arc's center.
        - radius (float): The radius of the arc.
        - angle_degrees (float): The angle in degrees from the start point of the arc, 
        measured clockwise from the positive x-axis.

        Returns:
        Point2D: The calculated point on the arc represented as a `Point2D` object with the calculated x and y coordinates.
        """
        angle_radians = math.radians(angle_degrees)
        x = cx + radius * math.cos(angle_radians)
        y = cy + radius * math.sin(angle_radians)
        return Point2D(x, y)


    def __str__(self) -> 'str':
        """Generates a string representation of the Arc2D object.

        #### Returns:
        `str`: A string that represents the Arc2D object.

        #### Example usage:
        ```python
        arc = Arc2D(startPoint, midPoint, endPoint)
        print(arc)
        # Output: Arc2D()
        ```
        """
        return f"{__class__.__name__}()"


class PolyCurve2D:
    def __init__(self) -> None:
        self.id = generateID()
        self.type = __class__.__name__
        self.curves = []
        self.points2D = []
        self.segmentcurves = None
        self.width = None
        self.height = None
        self.approximateLength = None
        self.graphicsStyleId = None
        self.isClosed = None
        self.isCyclic = None
        self.isElementGeometry = None
        self.isReadOnly = None
        self.length = self.length()
        self.period = None
        self.reference = None
        self.visibility = None

    def serialize(self):
        curves_serialized = [curve.serialize() if hasattr(
            curve, 'serialize') else str(curve) for curve in self.curves]
        points_serialized = [point.serialize() if hasattr(
            point, 'serialize') else str(point) for point in self.points2D]

        return {
            'type': self.type,
            'curves': curves_serialized,
            'points2D': points_serialized,
            'segmentcurves': self.segmentcurves,
            'width': self.width,
            'height': self.height,
            'approximateLength': self.approximateLength,
            'graphicsStyleId': self.graphicsStyleId,
            'id': self.id,
            'isClosed': self.isClosed,
            'isCyclic': self.isCyclic,
            'isElementGeometry': self.isElementGeometry,
            'isReadOnly': self.isReadOnly,
            'period': self.period,
            'reference': self.reference,
            'visibility': self.visibility
        }

    @staticmethod
    def deserialize(data):
        polycurve = PolyCurve2D()
        polycurve.segmentcurves = data.get('segmentcurves')
        polycurve.width = data.get('width')
        polycurve.height = data.get('height')
        polycurve.approximateLength = data.get('approximateLength')
        polycurve.graphicsStyleId = data.get('graphicsStyleId')
        polycurve.id = data.get('id')
        polycurve.isClosed = data.get('isClosed')
        polycurve.isCyclic = data.get('isCyclic')
        polycurve.isElementGeometry = data.get('isElementGeometry')
        polycurve.isReadOnly = data.get('isReadOnly')
        polycurve.period = data.get('period')
        polycurve.reference = data.get('reference')
        polycurve.visibility = data.get('visibility')

        if 'curves' in data:
            for curve_data in data['curves']:
                curve = Line2D.deserialize(curve_data)
                polycurve.curves.append(curve)

        if 'points2D' in data:
            for point_data in data['points2D']:
                point = Point2D.deserialize(point_data)
                polycurve.points2D.append(point)

        return polycurve

    def __id__(self):
        return f"id:{self.id}"

    @classmethod  # curves or curves?
    def by_joined_curves(cls, curves):
        if not curves or len(curves) < 1:
            raise ValueError(
                "At least one curve is required to create a PolyCurve2D.")

        polycurve = cls()
        for curve in curves:
            if not polycurve.points2D or polycurve.points2D[-1] != curve.start:
                polycurve.points2D.append(curve.start)
            polycurve.curves.append(curve)
            polycurve.points2D.append(curve.end)

        polycurve.isClosed = polycurve.points2D[0].value == polycurve.points2D[-1].value
        if project.autoclose == True and polycurve.isClosed == False:
            polycurve.curves.append(
                Line2D(start=curves[-1].end, end=curves[0].start))
            polycurve.points2D.append(curves[0].start)
            polycurve.isClosed = True
        return polycurve

    def points(self):
        for i in self.curves:
            self.points2D.append(i.start)
            self.points2D.append(i.end)
        return self.points2D

    def centroid(self) -> Point2D:
        if not self.isClosed or len(self.points2D) < 3:
            return "Polygon has less than 3 points or is not closed!"

        num_points = len(self.points2D)
        signed_area = 0
        centroid_x = 0
        centroid_y = 0

        for i in range(num_points):
            x0, y0 = self.points2D[i].x, self.points2D[i].y
            if i == num_points - 1:
                x1, y1 = self.points2D[0].x, self.points2D[0].y
            else:
                x1, y1 = self.points2D[i + 1].x, self.points2D[i + 1].y

            cross = x0 * y1 - x1 * y0
            signed_area += cross
            centroid_x += (x0 + x1) * cross
            centroid_y += (y0 + y1) * cross

        signed_area *= 0.5
        centroid_x /= (6.0 * signed_area)
        centroid_y /= (6.0 * signed_area)

        return Point2D(x=round(centroid_x, project.decimals), y=round(centroid_y, project.decimals))

    @staticmethod
    def from_polycurve_3D(PolyCurve):
        points = []
        for pt in PolyCurve.points:
            points.append(Point2D(pt.x, pt.y))
        plycrv = PolyCurve2D.by_points(points)
        return plycrv

    def area(self) -> float:  # shoelace formula
        if not self.isClosed or len(self.points2D) < 3:
            return "Polygon has less than 3 points or is not closed!"

        num_points = len(self.points2D)
        area = 0

        for i in range(num_points):
            x0, y0 = self.points2D[i].x, self.points2D[i].y
            if i == num_points - 1:
                x1, y1 = self.points2D[0].x, self.points2D[0].y
            else:
                x1, y1 = self.points2D[i + 1].x, self.points2D[i + 1].y

            area += x0 * y1 - x1 * y0

        area = abs(area) / 2.0
        return area

    def close(self) -> bool:
        if self.curves[0] == self.curves[-1]:
            return self
        else:
            self.curves.append(self.curves[0])
            plycrv = PolyCurve2D()
            for curve in self.curves:
                plycrv.curves.append(curve)
        return plycrv

    def scale(self, scalefactor):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                arcie = Arc2D(Point2D.product(scalefactor, i.start),
                              Point2D.product(scalefactor, i.end))
                arcie.mid = Point2D.product(scalefactor, i.mid)
                crvs.append(arcie)
            elif i.__class__.__name__ == "Line":
                crvs.append(Line2D(Point2D.product(
                    scalefactor, i.start), Point2D.product(scalefactor, i.end)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.by_joined_curves(crvs)
        return crv

    @classmethod
    def by_points(cls, points):
        if not points or len(points) < 2:
            pass

        polycurve = cls()
        for i in range(len(points)):
            polycurve.points2D.append(points[i])
            if i < len(points) - 1:
                polycurve.curves.append(
                    Line2D(start=points[i], end=points[i+1]))

        polycurve.isClosed = points[0] == points[-1]
        if project.autoclose == True:
            polycurve.curves.append(Line2D(start=points[-1], end=points[0]))
            polycurve.points2D.append(points[0])
            polycurve.isClosed = True
        return polycurve

    def get_width(self) -> float:
        x_values = [point.x for point in self.points2D]
        y_values = [point.y for point in self.points2D]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        left_top = Point2D(x=min_x, y=max_y)
        left_bottom = Point2D(x=min_x, y=min_y)
        right_top = Point2D(x=max_x, y=max_y)
        right_bottom = Point2D(x=max_x, y=min_y)
        self.width = abs(Point2D.distance(left_top, right_top))
        self.height = abs(Point2D.distance(left_top, left_bottom))
        return self.width

    def length(self) -> float:
        lst = []
        for line in self.curves:
            lst.append(line.length)

        return sum(i.length for i in self.curves)

    @staticmethod
    def by_polycurve_2D(PolyCurve2D):
        plycrv = PolyCurve2D()
        curves = []
        for i in PolyCurve2D.curves:
            if i.__class__.__name__ == "Arc2D":
                curves.append(Arc2D(Point2D(i.start.x, i.start.y), Point2D(
                    i.mid.x, i.mid.y), Point2D(i.end.x, i.end.y)))
            elif i.__class__.__name__ == "Line2D":
                curves.append(
                    Line2D(Point2D(i.start.x, i.start.y), Point2D(i.end.x, i.end.y)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        plycrv.points = pnts
        plycrv.curves = curves
        return plycrv

    def multi_split(self, lines: Line2D):
        lines = flatten(lines)
        new_polygons = []
        for index, line in enumerate(lines):
            if index == 0:
                n_p = self.split(line, returnlines=True)
                if n_p != None:
                    for nxp in n_p:
                        if nxp != None:
                            new_polygons.append(n_p)
            else:
                for new_poly in flatten(new_polygons):
                    n_p = new_poly.split(line, returnlines=True)
                    if n_p != None:
                        for nxp in n_p:
                            if nxp != None:
                                new_polygons.append(n_p)
        project.objects.append(flatten(new_polygons))
        return flatten(new_polygons)

    def translate(self, vector2d: Vector2):
        crvs = []
        v1 = vector2d
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.translate(v1),
                            i.mid.translate(v1), i.end.translate(v1)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.translate(v1), i.end.translate(v1)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.by_joined_curves(crvs)
        return crv

    @staticmethod
    def copy_translate(pc, vector3d: Vector):
        crvs = []
        v1 = vector3d
        for i in pc.curves:
            if i.__class__.__name__ == "Line":
                crvs.append(Line2D(Point2D.translate(i.start, v1),
                            Point2D.translate(i.end, v1)))
            else:
                print("Curvetype not found")

        PCnew = PolyCurve2D.by_joined_curves(crvs)
        return PCnew

    def rotate(self, rotation):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(i.start.rotate(rotation),
                            i.mid.rotate(rotation), i.end.rotate(rotation)))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(i.start.rotate(
                    rotation), i.end.rotate(rotation)))
            else:
                print("Curvetype not found")
        crv = PolyCurve2D.by_joined_curves(crvs)
        return crv

    @staticmethod
    def boundingbox_global_CS(PC):
        x = []
        y = []
        for i in PC.curves():
            x.append(i.start.x)
            y.append(i.start.y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        bbox = PolyCurve2D.by_points([Point2D(xmin, ymin), Point2D(
            xmax, ymin), Point2D(xmax, ymax), Point2D(xmin, ymax), Point2D(xmin, ymin)])
        return bbox

    @staticmethod
    def bounds(PC):
        # returns xmin,xmax,ymin,ymax,width,height of polycurve 2D
        x = []
        y = []
        for i in PC.curves:
            x.append(i.start.x)
            y.append(i.start.y)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        width = xmax-xmin
        height = ymax-ymin
        return xmin, xmax, ymin, ymax, width, height

    @classmethod
    def unclosed_by_points(self, points: Point2D):
        plycrv = PolyCurve2D()
        for index, point in enumerate(points):
            plycrv.points2D.append(point)
            try:
                nextpoint = points[index + 1]
                plycrv.curves.append(Line2D(start=point, end=nextpoint))
            except:
                pass
        return plycrv

    @staticmethod
    def polygon(self):
        points = []
        for i in self.curves:
            if i == Arc2D:
                points.append(i.start, i.mid)
            else:
                points.append(i.start)
        points.append(points[0])
        return points

    @staticmethod
    def segment(self, count):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D.segmented_arc(i, count))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(i)
        crv = flatten(crvs)
        pc = PolyCurve2D.by_joined_curves(crv)
        return pc

    def to_polycurve_3D(self):
        from geometry.geometry2d import PolyCurve2D
        from geometry.geometry2d import Point2D
        from geometry.geometry2d import Line2D
        from geometry.geometry2d import Arc2D

        p1 = PolyCurve2D()
        curves = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                curves.append(Arc2D(Point2D(i.start.x, i.start.y), Point2D(i.middle.x, i.middle.y),
                                    Point2D(i.end.x, i.end.y)))
            elif i.__class__.__name__ == "Line":
                curves.append(
                    Line2D(Point2D(i.start.x, i.start.y), Point2D(i.end.x, i.end.y)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        p1.points2D = pnts
        p1.curves = curves
        return p1

    @staticmethod
    def transform_from_origin(polycurve, startpoint: Point2D, directionvector: Vector):
        crvs = []
        for i in polycurve.curves:
            if i.__class__.__name__ == "Arc2D":
                crvs.append(Arc2D(transform_point_2D(i.start, project.CSGlobal, startpoint, directionvector),
                                  transform_point_2D(
                                      i.mid, project.CSGlobal, startpoint, directionvector),
                                  transform_point_2D(
                                      i.end, project.CSGlobal, startpoint, directionvector)
                                  ))
            elif i.__class__.__name__ == "Line2D":
                crvs.append(Line2D(start=transform_point_2D(i.start, project.CSGlobal, startpoint, directionvector),
                                   end=transform_point_2D(
                                       i.end, project.CSGlobal, startpoint, directionvector)
                                   ))
            else:
                print(i.__class__.__name__ + "Curvetype not found")
        pc = PolyCurve2D()
        pc.curves = crvs
        return pc

    def __str__(self):
        l = len(self.points2D)
        return f"{__class__.__name__}, ({l} points)"


class Surface2D:
    def __init__(self) -> None:
        pass  # PolyCurve2D
        self.id = generateID()
        self.type = __class__.__name__

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Profile2D:
    def __init__(self) -> None:
        self.id = generateID()
        self.type = __class__.__name__

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class ParametricProfile2D:
    def __init__(self) -> None:
        self.type = __class__.__name__
        self.id = generateID()

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"
