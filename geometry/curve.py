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

import sys
from pathlib import Path
from typing import Union

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.plane import Plane
from packages.helper import *
from abstract.vector import *
from geometry.point import Point
from project.fileformat import project
from abstract.coordinatesystem import CoordinateSystem, CSGlobal
from geometry.point import transform_point


# [!not included in BP singlefile - end]

class Line:
    def __init__(self, start: 'Point', end: 'Point') -> 'Line':
        """Initializes a Line object with the specified start and end points.

        - `start` (Point): The starting point of the line segment.
        - `end` (Point): The ending point of the line segment.
        """
        self.id = generateID()
        self.type = __class__.__name__
        self.start: Point = start
        self.end: Point = end
        self.x = [self.start.x, self.end.x]
        self.y = [self.start.y, self.end.y]
        try:
            self.z = [self.start.z, self.end.z]
        except:
            self.z = 0

        self.dx = self.end.x-self.start.x
        self.dy = self.end.y-self.start.y
        try:
            self.dz = self.end.z-self.start.z
        except:
            self.dz = 0
        self.length = self.length()
        self.vector: Vector3 = Vector3.by_two_points(start, end)
        self.vector_normalised = Vector3.normalize(self.vector)

    def serialize(self) -> 'dict':
        """Serializes the Line object into a dictionary.

        #### Returns:
        `dict`: A dictionary containing the serialized data of the Line object.

        #### Example usage:
        ```python

        ```         
        """
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        start_serialized = self.start.serialize() if hasattr(
            self.start, 'serialize') else str(self.start)
        end_serialized = self.end.serialize() if hasattr(
            self.end, 'serialize') else str(self.end)

        # Serialize vector if it has a serialize method, otherwise convert to string representation
        vector_serialized = self.vector.serialize() if hasattr(
            self.vector, 'serialize') else str(self.vector)
        vector_normalized_serialized = self.vector_normalised.serialize() if hasattr(
            self.vector_normalised, 'serialize') else str(self.vector_normalised)

        return {
            'id': id_value,
            'type': self.type,
            'start': start_serialized,
            'end': end_serialized,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'dx': self.dx,
            'dy': self.dy,
            'dz': self.dz,
            'length': self.length,
            'vector': vector_serialized,
            'vector_normalised': vector_normalized_serialized
        }

    @staticmethod
    def deserialize(data: 'dict'):
        """Deserializes the data dictionary into a Line object.

        #### Parameters:
        - `data` (dict): The dictionary containing the serialized data of the Line object.

        #### Returns:
        `Line`: A Line object reconstructed from the serialized data.

        #### Example usage:
        ```python

        ```          
        """
        start_point = Point.deserialize(data['start'])
        end_point = Point.deserialize(data['end'])

        instance = Line(start_point, end_point)

        instance.id = data.get('id')
        instance.type = data.get('type')
        instance.x = data.get('x')
        instance.y = data.get('y')
        instance.z = data.get('z')
        instance.dx = data.get('dx')
        instance.dy = data.get('dy')
        instance.dz = data.get('dz')
        instance.length = data.get('length')

        if 'vector' in data and hasattr(Vector3, 'deserialize'):
            instance.vector = Vector3.deserialize(data['vector'])
        else:
            instance.vector = data['vector']

        if 'vector_normalised' in data and hasattr(Vector3, 'deserialize'):
            instance.vector_normalised = Vector3.deserialize(
                data['vector_normalised'])
        else:
            instance.vector_normalised = data['vector_normalised']

        return instance

    @staticmethod
    def by_startpoint_direction_length(start: 'Point', direction: 'Vector3', length: 'float') -> 'Line':
        """Creates a line segment starting from a given point in the direction of a given vector with a specified length.

        #### Parameters:
        - `start` (Point): The starting point of the line segment.
        - `direction` (Vector3): The direction vector of the line segment.
        - `length` (float): The length of the line segment.

        #### Returns:
        `Line`: A new Line object representing the line segment.

        #### Example usage:
        ```python

        ```          
        """
        norm = math.sqrt(direction.x ** 2 + direction.y **
                         2 + direction.z ** 2)
        normalized_direction = Vector3(
            direction.x / norm, direction.y / norm, direction.z / norm)

        end_x = start.x + normalized_direction.x * length
        end_y = start.y + normalized_direction.y * length
        end_z = start.z + normalized_direction.z * length
        end_point = Point(end_x, end_y, end_z)

        return Line(start, end_point)

    def translate(self, direction: 'Vector3') -> 'Line':
        """Translates the Line object by a given direction vector.

        #### Parameters:
        - `direction` (Vector3): The direction vector by which the line segment will be translated.

        #### Returns:
        `Line`: The translated Line object.

        #### Example usage:
        ```python

        ```          
        """
        self.start = Point.translate(self.start, direction)
        self.end = Point.translate(self.end, direction)
        return self

    @staticmethod
    def translate_2(line: 'Line', direction: 'Vector3') -> 'Line':
        """Translates the specified Line object by a given direction vector.

        #### Parameters:
        - `line` (Line): The Line object to be translated.
        - `direction` (Vector3): The direction vector by which the line segment will be translated.

        #### Returns:
        `Line`: The translated Line object.

        #### Example usage:
        ```python

        ```          
        """
        line.start = Point.translate(line.start, direction)
        line.end = Point.translate(line.end, direction)
        return line

    @staticmethod
    def transform(line: 'Line', cs_new: 'CoordinateSystem') -> 'Line':
        """Transforms the Line object to a new coordinate system.

        #### Parameters:
        - `line` (Line): The Line object to be transformed.
        - `cs_new` (CoordinateSystem): The new coordinate system to which the Line object will be transformed.

        #### Returns:
        `Line`: The transformed Line object.

        #### Example usage:
        ```python

        ```          
        """
        ln = Line(start=line.start, end=line.end)
        ln.start = transform_point_2(ln.start, cs_new)
        ln.end = transform_point_2(ln.end, cs_new)
        return ln

    def offset(line: 'Line', vector: 'Vector3') -> 'Line':
        """Offsets the Line object by a given vector.

        #### Parameters:
        - `line` (Line): The Line object to be offset.
        - `vector` (Vector3): The vector by which the Line object will be offset.

        #### Returns:
        `Line`: The offset Line object.

        #### Example usage:
        ```python

        ```          
        """
        start = Point(line.start.x + vector.x, line.start.y +
                      vector.y, line.start.z + vector.z)
        end = Point(line.end.x + vector.x, line.end.y +
                    vector.y, line.end.z + vector.z)
        return Line(start=start, end=end)

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

    def mid_point(self) -> 'Point':
        """Computes the midpoint of the Line object.

        #### Returns:
        `Point`: The midpoint of the Line object.

        #### Example usage:
        ```python

        ```          
        """
        vect = Vector3.scale(self.vector, 0.5)
        mid = Point.translate(self.start, vect)
        return mid

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

    def length(self) -> 'float':
        """Computes the length of the Line object.

        #### Returns:
        `float`: The length of the Line object.

        #### Example usage:
        ```python

        ```          
        """
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy) + self.dz * self.dz)

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


class PolyCurve:
    def __init__(self):
        """Initializes a PolyCurve object.
        
        - `id` (int): The unique identifier of the arc.
        - `type` (str): The type of the arc.
        - `start` (Point): The start point of the arc.
        - `mid` (Point): The mid point of the arc.
        - `end` (Point): The end point of the arc.
        - `origin` (Point): The origin point of the arc.
        - `plane` (Plane): The plane containing the arc.
        - `radius` (float): The radius of the arc.
        - `startAngle` (float): The start angle of the arc in radians.
        - `endAngle` (float): The end angle of the arc in radians.
        - `angle_radian` (float): The total angle of the arc in radians.
        - `area` (float): The area of the arc.
        - `length` (float): The length of the arc.
        - `units` (str): The units used for measurement.
        - `coordinatesystem` (CoordinateSystem): The coordinate system of the arc.

        """
        self.id = generateID()
        self.type = __class__.__name__
        self.curves = []
        self.points = []
        self.segmentcurves = None
        self.width = None
        self.height = None
        # Methods ()
        # self.close
        # pointonperimeter
        # Properties
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

    def serialize(self) -> 'dict':
        """Serializes the PolyCurve object.

        #### Returns:
        `dict`: Serialized data of the PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        curves_serialized = [curve.serialize() if hasattr(
            curve, 'serialize') else str(curve) for curve in self.curves]
        points_serialized = [point.serialize() if hasattr(
            point, 'serialize') else str(point) for point in self.points]

        return {
            'type': self.type,
            'curves': curves_serialized,
            'points': points_serialized,
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
        """Deserializes the PolyCurve object.

        #### Parameters:
        - `data` (dict): Serialized data of the PolyCurve object.

        #### Returns:
        `PolyCurve`: Deserialized PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        polycurve = PolyCurve()
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

        # Deserialize curves and points
        if 'curves' in data:
            for curve_data in data['curves']:
                # Assuming a deserialize method exists for curve objects
                curve = Line.deserialize(curve_data)
                polycurve.curves.append(curve)

        if 'points' in data:
            for point_data in data['points']:
                # Assuming a deserialize method exists for point objects
                point = Point.deserialize(point_data)
                polycurve.points.append(point)

        return polycurve

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

    def get_width(self) -> 'float':
        """Calculates the width of the PolyCurve.

        #### Returns:
        `float`: The width of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        left_top = Point(x=min_x, y=max_y, z=self.z)
        left_bottom = Point(x=min_x, y=min_y, z=self.z)
        right_top = Point(x=max_x, y=max_y, z=self.z)
        right_bottom = Point(x=max_x, y=min_y, z=self.z)
        self.width = abs(Point.distance(left_top, right_top))
        self.height = abs(Point.distance(left_top, left_bottom))
        return self.width

    def centroid(self) -> 'Point':
        """Calculates the centroid of the PolyCurve.

        #### Returns:
        `Point`: The centroid point of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        if self.isClosed:
            num_points = len(self.points)
            if num_points < 3:
                return "Polygon has less than 3 points!"

            A = 0.0
            for i in range(num_points):
                x0, y0 = self.points[i].x, self.points[i].y
                x1, y1 = self.points[(
                    i + 1) % num_points].x, self.points[(i + 1) % num_points].y
                A += x0 * y1 - x1 * y0
            A *= 0.5

            Cx, Cy = 0.0, 0.0
            for i in range(num_points):
                x0, y0 = self.points[i].x, self.points[i].y
                x1, y1 = self.points[(
                    i + 1) % num_points].x, self.points[(i + 1) % num_points].y
                factor = (x0 * y1 - x1 * y0)
                Cx += (x0 + x1) * factor
                Cy += (y0 + y1) * factor

            Cx /= (6.0 * A)
            Cy /= (6.0 * A)

            return Point(x=round(Cx, project.decimals), y=round(Cy, project.decimals), z=self.points[0].z)
        else:
            return None

    def area(self) -> 'float':  # shoelace formula
        """Calculates the area enclosed by the PolyCurve using the shoelace formula.

        #### Returns:
        `float`: The area enclosed by the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        if self.isClosed:
            if len(self.points) < 3:
                return "Polygon has less than 3 points!"

            num_points = len(self.points)
            S1, S2 = 0, 0

            for i in range(num_points):
                x, y = self.points[i].x, self.points[i].y
                if i == num_points - 1:
                    x_next, y_next = self.points[0].x, self.points[0].y
                else:
                    x_next, y_next = self.points[i + 1].x, self.points[i + 1].y

                S1 += x * y_next
                S2 += y * x_next

            area = 0.5 * abs(S1 - S2)
            return area
        else:
            print("Polycurve is not closed, no area!")
            return None

    def length(self) -> 'float':
        """Calculates the total length of the PolyCurve.

        #### Returns:
        `float`: The total length of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        lst = []
        for line in self.curves:
            lst.append(line.length)

        return sum(i.length for i in self.curves)

    def close(self) -> 'bool':
        """Closes the PolyCurve by connecting the last point to the first point.

        #### Returns:
        `bool`: True if the PolyCurve is successfully closed, False otherwise.

        #### Example usage:
        ```python

        ```        
        """
        if self.curves[0] == self.curves[-1]:
            return self
        else:
            self.curves.append(self.curves[0])
            plycrv = PolyCurve()
            for curve in self.curves:
                plycrv.curves.append(curve)
        return plycrv

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
        for crv in curvelst:
            if crv.length == 0:
                curvelst.remove(crv)
                # print("Error: Curve length cannot be zero.")
                # sys.exit()

        projectClosed = project.closed
        plycrv = PolyCurve()
        for index, curve in enumerate(curvelst):
            if index == 0:
                plycrv.curves.append(curve)
                plycrv.points.append(curve.start)
                plycrv.points.append(curve.end)
            else:
                plycrv.curves.append(curve)
                plycrv.points.append(curve.end)
        if projectClosed:
            if plycrv.points[0].value == plycrv.points[-1].value:
                plycrv.isClosed = True
            else:
                # plycrv.points.append(curvelst[0].start)
                plycrv.curves.append(curve)
                plycrv.isClosed = True
        elif projectClosed == False:
            if plycrv.points[0].value == plycrv.points[-1].value:
                plycrv.isClosed = True
            else:
                plycrv.isClosed = False
        if plycrv.points[-2].value == plycrv.points[0].value:
            plycrv.curves = plycrv.curves.pop(-1)

        return plycrv

    @classmethod
    def by_points(self, points: 'list[Point]') -> 'PolyCurve':
        """Creates a PolyCurve from a list of points.

        #### Parameters:
        - `points` (list[Point]): The list of points defining the PolyCurve.

        #### Returns:
        `PolyCurve`: The created PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        seen = set()
        unique_points = []

        for point in points:
            if point in seen:
                points.remove(point)
                print("Error: Polycurve cannot have multiple identical points.")
                sys.exit()

            seen.add(point)
            unique_points.append(point)

        plycrv = PolyCurve()
        for index, point in enumerate(points):
            plycrv.points.append(point)
            try:
                nextpoint = points[index+1]
                plycrv.curves.append(Line(start=point, end=nextpoint))
            except:
                firstpoint = points[0]
                plycrv.curves.append(Line(start=point, end=firstpoint))

        if project.closed:
            if plycrv.points[0].value == plycrv.points[-1].value:
                plycrv.isClosed = True
            else:
                plycrv.isClosed = True
                plycrv.points.append(points[0])

        elif project.closed == False:
            if plycrv.points[0].value == plycrv.points[-1].value:
                plycrv.isClosed = True
            else:
                plycrv.isClosed = False
                plycrv.points.append(points[0])

        return plycrv

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

    @staticmethod
    def by_polycurve_2D(PolyCurve2D) -> 'PolyCurve':
        """Creates a 3D PolyCurve from a 2D PolyCurve.

        #### Parameters:
        - `PolyCurve2D`: The 2D PolyCurve object.

        #### Returns:
        `PolyCurve`: The created 3D PolyCurve object.

        #### Example usage:
        ```python

        ```        
        """
        plycrv = PolyCurve()
        curves = []
        for i in PolyCurve2D.curves:
            if i.__class__.__name__ == "Arc2D":
                curves.append(Arc(Point(i.start.x, i.start.y, 0), Point(
                    i.mid.x, i.mid.y, 0), Point(i.end.x, i.end.y, 0)))
            elif i.__class__.__name__ == "Line2D":
                curves.append(Line(Point(i.start.x, i.start.y, 0),
                              Point(i.end.x, i.end.y, 0)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        plycrv.points = pnts
        plycrv.curves = curves
        return plycrv

    # make sure that the lines start/stop already on the edge of the polycurve
    def split(self, line: 'Line', returnlines=None) -> 'list[PolyCurve]':
        """Splits the PolyCurve by a line and returns the split parts.

        #### Parameters:
        - `line` (Line): The line to split the PolyCurve.
        - `returnlines` (bool, optional): Whether to return the split PolyCurves as objects or add them to the project. Defaults to None.

        #### Returns:
        `list[PolyCurve]`: If `returnlines` is True, returns a list of split PolyCurves. Otherwise, None.

        #### Example usage:
        ```python

        ```        
        """
        from abstract.intersect2d import Intersect2d, is_point_on_line_segment

        allLines = self.curves.copy()

        insect = Intersect2d().get_intersect_line_polycurve(
            self, line, split=True, stretch=False)
        for pt in insect["IntersectGridPoints"]:
            for index, line in enumerate(allLines):
                if is_point_on_line_segment(pt, line) == True:
                    cuttedLines = line.split([pt])
                    allLines = replace_at_index(allLines, index, cuttedLines)

        if len(insect["IntersectGridPoints"]) == 2:
            part1 = []
            part2 = []

            for j in allLines:
                # part1
                if j.start == insect["IntersectGridPoints"][1]:
                    part1LineEnd = j.end
                    part1.append(j.start)
                if j.end == insect["IntersectGridPoints"][0]:
                    part1LineStart = j.start
                    part1.append(j.end)
                # part2
                if j.start == insect["IntersectGridPoints"][0]:
                    part2LineEnd = j.end
                    part2.append(j.start)
                if j.end == insect["IntersectGridPoints"][1]:
                    part2LineStart = j.start
                    part2.append(j.end)

            s2 = self.points.index(part1LineStart)
            s1 = self.points.index(part1LineEnd)
            completelist = list(range(len(self.points)))
            partlist1 = flatten(completelist[s2:s1+1])
            partlist2 = flatten([completelist[s1+1:]] + [completelist[:s2]])

            SplittedPolyCurves = []
            # part1
            if part1LineStart != None and part1LineEnd != None:
                for i, index in enumerate(partlist1):
                    pts = self.points[index]
                    part1.insert(i+1, pts)
                if returnlines:
                    SplittedPolyCurves.append(PolyCurve.by_points(part1))
                else:
                    project.objects.append(PolyCurve.by_points(part1))

            # part2 -> BUGG?
            if part2LineStart != None and part2LineEnd != None:
                for index in partlist2:
                    pts = self.points[index]
                    part2.insert(index, pts)
                if returnlines:
                    SplittedPolyCurves.append(PolyCurve.by_points(part2))
                else:
                    project.objects.append(PolyCurve.by_points(part2))

            if returnlines:  # return lines while using multi_split
                return SplittedPolyCurves

        else:
            print(
                f"Must need 2 points to split PolyCurve into PolyCurves, got now {len(insect['IntersectGridPoints'])} points.")

    def multi_split(self, lines: 'Line') -> 'list[PolyCurve]':  # SLOW, MUST INCREASE SPEAD
        """Splits the PolyCurve by multiple lines.
        This method splits the PolyCurve by multiple lines and adds the resulting PolyCurves to the project.

        #### Parameters:
        - `lines` (List[Line]): The list of lines to split the PolyCurve.

        #### Returns:
        `List[PolyCurve]`: The list of split PolyCurves.

        #### Example usage:
        ```python

        ```        
        """
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

    def translate(self, vector_3d: 'Vector3') -> 'PolyCurve':
        """Translates the PolyCurve by a 3D vector.

        #### Parameters:
        - `vector_3d` (Vector3): The 3D vector by which to translate the PolyCurve.

        #### Returns:
        `PolyCurve`: The translated PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        crvs = []
        vector_1 = vector_3d
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.translate(i.start, vector_1), Point.translate(
                    i.middle, vector_1), Point.translate(i.end, vector_1)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.translate(i.start, vector_1),
                            Point.translate(i.end, vector_1)))
            else:
                print("Curvetype not found")
        pc = PolyCurve()
        pc.curves = crvs
        return pc

    @staticmethod
    def copy_translate(pc: 'PolyCurve', vector_3d: 'Vector3') -> 'PolyCurve':
        """Creates a copy of a PolyCurve and translates it by a 3D vector.

        #### Parameters:
        - `pc` (PolyCurve): The PolyCurve to copy and translate.
        - `vector_3d` (Vector3): The 3D vector by which to translate the PolyCurve.

        #### Returns:
        `PolyCurve`: The translated copy of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        crvs = []
        vector_1 = vector_3d
        for i in pc.curves:
            # if i.__class__.__name__ == "Arc":
            #    crvs.append(Arc(Point.translate(i.start, vector_1), Point.translate(i.middle, vector_1), Point.translate(i.end, vector_1)))
            if i.__class__.__name__ == "Line":
                crvs.append(Line(Point.translate(i.start, vector_1),
                            Point.translate(i.end, vector_1)))
            else:
                print("Curvetype not found")

        PCnew = PolyCurve.by_joined_curves(crvs)
        return PCnew

    def rotate(self, angle: 'float', dz: 'float') -> 'PolyCurve':
        """Rotates the PolyCurve by a given angle around the Z-axis and displaces it in the Z-direction.

        #### Parameters:
        - `angle` (float): The angle of rotation in degrees.
        - `dz` (float): The displacement in the Z-direction.

        #### Returns:
        `PolyCurve`: The rotated and displaced PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        # angle in degrees
        # dz = displacement in z-direction
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.rotate_XY(i.start, angle, dz), Point.rotate_XY(
                    i.middle, angle, dz), Point.rotate_XY(i.end, angle, dz)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.rotate_XY(i.start, angle, dz),
                            Point.rotate_XY(i.end, angle, dz)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.by_joined_curves(crvs)
        return crv

    def to_polycurve_2D(self):
        """Converts the PolyCurve to a PolyCurve2D.

        #### Returns:
        `PolyCurve2D`: The converted PolyCurve2D.

        #### Example usage:
        ```python

        ```        
        """
        # by points,
        from geometry.geometry2d import PolyCurve2D
        from geometry.geometry2d import Point2D
        from geometry.geometry2d import Line2D
        from geometry.geometry2d import Arc2D

        point_1 = PolyCurve2D()
        count = 0
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
        point_1.points = pnts
        point_1.curves = curves
        return point_1

    @staticmethod
    def transform_from_origin(polycurve: 'PolyCurve', startpoint: 'Point', directionvector: 'Vector3') -> 'PolyCurve':
        """Transforms a PolyCurve from a given origin point and direction vector.

        #### Parameters:
        - `polycurve` (PolyCurve): The PolyCurve to transform.
        - `startpoint` (Point): The origin point for the transformation.
        - `directionvector` (Vector3): The direction vector for the transformation.

        #### Returns:
        `PolyCurve`: The transformed PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        crvs = []
        if polycurve.type == "PolyCurve2D":
            for i in polycurve.curves:
                if i.__class__.__name__ == "Arc":
                    crvs.append(Arc(transform_point(i.start, CSGlobal, startpoint, directionvector),
                                    transform_point(
                                        i.mid, CSGlobal, startpoint, directionvector),
                                    transform_point(
                                        i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line":
                    crvs.append(Line(start=transform_point(i.start, CSGlobal, startpoint, directionvector),
                                     end=transform_point(
                                         i.end, CSGlobal, startpoint, directionvector)
                                     ))
                elif i.__class__.__name__ == "Arc2D":
                    # print(Point.point_2D_to_3D(i.start),CSGlobal, startpoint, directionvector)
                    crvs.append(Arc(transform_point(Point.point_2D_to_3D(i.start), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point_2D_to_3D(
                                        i.mid), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point_2D_to_3D(
                                        i.end), CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line2D":
                    crvs.append(Line(start=transform_point(Point.point_2D_to_3D(i.start), CSGlobal, startpoint, directionvector),
                                     end=transform_point(Point.point_2D_to_3D(
                                         i.end), CSGlobal, startpoint, directionvector)
                                     ))
                else:
                    print(i.__class__.__name__ + "Curvetype not found")
        elif polycurve.type == "PolyCurve":
            for i in polycurve.curves:
                if i.__class__.__name__ == "Arc":
                    crvs.append(Arc(transform_point(i.start, CSGlobal, startpoint, directionvector),
                                    transform_point(
                                        i.mid, CSGlobal, startpoint, directionvector),
                                    transform_point(
                                        i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line":
                    crvs.append(Line(start=transform_point(i.start, CSGlobal, startpoint, directionvector),
                                     end=transform_point(
                                         i.end, CSGlobal, startpoint, directionvector)
                                     ))
                elif i.__class__.__name__ == "Arc2D":
                    # print(Point.point_2D_to_3D(i.start),CSGlobal, startpoint, directionvector)
                    crvs.append(Arc(transform_point(Point.point_2D_to_3D(i.start), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point_2D_to_3D(
                                        i.mid), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point_2D_to_3D(
                                        i.end), CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line2D":
                    crvs.append(Line(start=transform_point(Point.point_2D_to_3D(i.start), CSGlobal, startpoint, directionvector),
                                     end=transform_point(Point.point_2D_to_3D(
                                         i.end), CSGlobal, startpoint, directionvector)
                                     ))
                else:
                    print(i.__class__.__name__ + "Curvetype not found")

        pc = PolyCurve()
        pc.curves = crvs
        return pc

    def __str__(self) -> 'str':
        """Returns a string representation of the PolyCurve.

        #### Returns:
        `str`: The string representation of the PolyCurve.

        #### Example usage:
        ```python

        ```        
        """
        length = len(self.points)
        return f"{__class__.__name__}, ({length} points)"

# 2D PolyCurve to 3D Polygon


def Rect(vector: 'Vector3', width: 'float', height: 'float') -> 'PolyCurve':
    """Creates a rectangle in the XY-plane with a translation of vector.

    #### Parameters:
    - `vector` (Vector3): The translation vector.
    - `width` (float): The width of the rectangle.
    - `height` (float): The height of the rectangle.

    #### Returns:
    `PolyCurve`: The rectangle PolyCurve.

    #### Example usage:
    ```python

    ```    
    """
    point_1 = Point(0, 0, 0).translate(Point(0, 0, 0), vector)
    point_2 = Point(0, 0, 0).translate(Point(width, 0, 0), vector)
    point_3 = Point(0, 0, 0).translate(Point(width, height, 0), vector)
    point_4 = Point(0, 0, 0).translate(Point(0, height, 0), vector)
    crv = PolyCurve.by_points([point_1, point_2, point_3, point_4, point_1])
    return crv


def Rect_XY(vector: 'Vector3', width: 'float', height: 'float') -> 'PolyCurve':
    """Creates a rectangle in the XY-plane.

    #### Parameters:
    - `vector` (Vector3): The base vector of the rectangle.
    - `width` (float): The width of the rectangle.
    - `height` (float): The height of the rectangle.

    #### Returns:
    `PolyCurve`: The rectangle PolyCurve.

    #### Example usage:
    ```python

    ```        
    """
    point_1 = Point(0, 0, 0).translate(Point(0, 0, 0), vector)
    point_2 = Point(0, 0, 0).translate(Point(width, 0, 0), vector)
    point_3 = Point(0, 0, 0).translate(Point(width, 0, height), vector)
    point_4 = Point(0, 0, 0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.by_points([point_1, point_2, point_3, point_4])
    return crv


def Rect_YZ(vector: 'Vector3', width: 'float', height: 'float') -> 'PolyCurve':
    """Creates a rectangle in the YZ-plane.

    #### Parameters:
    - `vector` (Vector3): The base vector of the rectangle.
    - `width` (float): The width of the rectangle.
    - `height` (float): The height of the rectangle.

    #### Returns:
    `PolyCurve`: The rectangle PolyCurve.

    #### Example usage:
    ```python

    ```        
    """
    point_1 = Point(0, 0, 0).translate(Point(0, 0, 0), vector)
    point_2 = Point(0, 0, 0).translate(Point(0, width, 0), vector)
    point_3 = Point(0, 0, 0).translate(Point(0, width, height), vector)
    point_4 = Point(0, 0, 0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.by_points([point_1, point_2, point_3, point_4, point_1])
    return crv


class Polygon:
    def __init__(self) -> 'Polygon':
        """Represents a polygon composed of lines.

        - `lines` (list[Line]): List of lines composing the polygon.
        """
        self.id = generateID()
        self.type = __class__.__name__
        self.curves = []
        self.points = []
        self.lines = []
        self.isClosed = True

    @classmethod
    def by_points(self, points: 'list[Point]') -> 'PolyCurve':
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
            if point.type == "Point2D":
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


    @classmethod
    def by_joined_curves(cls, curves: 'list[Line]') -> 'Polygon':
        if not curves:
            print("Error: At least one curve is required to form a Polygon.")
            sys.exit()

        for i in range(len(curves) - 1):
            if curves[i].end != curves[i+1].start:
                print("Error: Curves must be contiguous to form a Polygon.")
                sys.exit()

        if Point.to_matrix(curves[0].start) != Point.to_matrix(curves[-1].end):
            curves.append(Line(curves[-1].end, curves[0].start))

        polygon = cls()
        polygon.curves = curves

        for crv in polygon.curves:
            if Point.to_matrix(crv.start) not in polygon.points:
                polygon.points.append(crv.start)
            elif Point.to_matrix(crv.end) not in polygon.points:
                polygon.points.append(crv.end)

        return polygon


    def area(self) -> 'float':  # shoelace formula
        """Calculates the area enclosed by the Polygon using the shoelace formula.

        #### Returns:
        `float`: The area enclosed by the Polygon.

        #### Example usage:
        ```python

        ```        
        """
        if len(self.points) < 3:
            return "Polygon has less than 3 points!"

        num_points = len(self.points)
        S1, S2 = 0, 0

        for i in range(num_points):
            x, y = self.points[i].x, self.points[i].y
            if i == num_points - 1:
                x_next, y_next = self.points[0].x, self.points[0].y
            else:
                x_next, y_next = self.points[i + 1].x, self.points[i + 1].y

            S1 += x * y_next
            S2 += y * x_next

        area = 0.5 * abs(S1 - S2)
        return area

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


    def __str__(self) -> str:
        return f"{self.type}"


class Arc:
    def __init__(self, startPoint: 'Point', midPoint: 'Point', endPoint: 'Point') -> 'Arc':
        """Initializes an Arc object with start, mid, and end points.
        This constructor calculates and assigns the arc's origin, plane, radius, start angle, end angle, angle in radians, area, length, units, and coordinate system based on the input points.

        - `startPoint` (Point): The starting point of the arc.
        - `midPoint` (Point): The mid point of the arc which defines its curvature.
        - `endPoint` (Point): The ending point of the arc.
        """
        self.id = generateID()
        self.type = __class__.__name__
        self.start = startPoint
        self.mid = midPoint
        self.end = endPoint
        self.origin = self.origin_arc()
        vector_1 = Vector3(x=1, y=0, z=0)
        vector_2 = Vector3(x=0, y=1, z=0)
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
        self.coordinatesystem = self.coordinatesystem_arc()

    def distance(self, point_1: 'Point', point_2: 'Point') -> float:
        """Calculates the Euclidean distance between two points in 3D space.

        #### Parameters:
        - `point_1` (Point): The first point.
        - `point_2` (Point): The second point.

        #### Returns:
        `float`: The Euclidean distance between `point_1` and `point_2`.

        #### Example usage:
        ```python
        point1 = Point(1, 2, 3)
        point2 = Point(4, 5, 6)
        distance = arc.distance(point1, point2)
        # distance will be the Euclidean distance between point1 and point2
        ```
        """
        return math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2 + (point_2.z - point_1.z) ** 2)

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
        vx = Vector3.by_two_points(self.origin, self.start)  # Local X-axe
        vector_2 = Vector3.by_two_points(self.end, self.origin)
        vz = Vector3.cross_product(vx, vector_2)  # Local Z-axe
        vy = Vector3.cross_product(vx, vz)  # Local Y-axe
        self.coordinatesystem = CoordinateSystem(self.origin, Vector3.normalize(vx), Vector3.normalize(vy),
                                                 Vector3.normalize(vz))
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
        A = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
        
        if abs(A) < 1e-6:
            return float('inf')
        else:
            R = (a * b * c) / (4 * A)
            return R

    def origin_arc(self) -> 'Point':
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
        Vstartend = Vector3.by_two_points(self.start, self.end)
        halfVstartend = Vector3.scale(Vstartend, 0.5)
        b = 0.5 * Vector3.length(Vstartend)
        x = math.sqrt(Arc.radius_arc(self) * Arc.radius_arc(self) - b * b)
        mid = Point.translate(self.start, halfVstartend)
        vector_2 = Vector3.by_two_points(self.mid, mid)
        vector_3 = Vector3.normalize(vector_2)
        tocenter = Vector3.scale(vector_3, x)
        center = Point.translate(mid, tocenter)
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
        vector_1 = Vector3.by_two_points(self.origin, self.end)
        vector_2 = Vector3.by_two_points(self.origin, self.start)
        vector_3 = Vector3.by_two_points(self.origin, self.mid)
        vector_4 = Vector3.sum(vector_1, vector_2)
        try:
            v4b = Vector3.new_length(vector_4, self.radius)
            if Vector3.value(vector_3) == Vector3.value(v4b):
                angle = Vector3.angle_radian_between(vector_1, vector_2)
            else:
                angle = 2*math.pi-Vector3.angle_radian_between(vector_1, vector_2)
            return angle
        except:
            angle = 2*math.pi-Vector3.angle_radian_between(vector_1, vector_2)
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
    def points_at_parameter(arc: 'Arc', count: 'int') -> 'list':
        """Generates a list of points along the arc at specified intervals.
        This method divides the arc into segments based on the `count` parameter and calculates points at these intervals along the arc.

        #### Parameters:
        - `arc` (Arc): The arc object.
        - `count` (int): The number of points to generate along the arc.

        #### Returns:
        `list`: A list of points (`Point` objects) along the arc.

        #### Example usage:
        ```python
        arc = Arc(startPoint, midPoint, endPoint)
        points = Arc.points_at_parameter(arc, 5)
        # points will be a list of 5 points along the arc
        ```
        """
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angle_radian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point(arc.radius * math.cos(alpha),
                        arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        cs_new = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transform_point_2(i, cs_new))
        return pnts2

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


def transform_arc(arc_old, cs_new: 'CoordinateSystem') -> 'Arc':
    """Transforms an Arc object to a new coordinate system.

    This function takes an existing Arc object and a new CoordinateSystem object. It transforms the start, mid, and end points of the Arc to the new coordinate system, creating a new Arc object in the process.

    #### Parameters:
    - `arc_old` (Arc): The original Arc object to be transformed.
    - `cs_new` (CoordinateSystem): The new coordinate system to transform the Arc into.

    #### Returns:
    `Arc`: A new Arc object with its points transformed to the new coordinate system.

    #### Example usage:
    ```python
    arc_old = Arc(startPoint, midPoint, endPoint)
    cs_new = CoordinateSystem(...)  # Defined elsewhere
    arc_new = transform_arc(arc_old, cs_new)
    # arc_new is the transformed Arc object
    ```
    """
    start = transform_point_2(arc_old.start, cs_new)
    mid = transform_point_2(arc_old.mid, cs_new)
    end = transform_point_2(arc_old.end, cs_new)
    arc_new = Arc(startPoint=start, midPoint=mid, endPoint=end)

    return arc_new


class Circle:
    """Represents a circle with a specific radius, plane, and length.
    """
    def __init__(self, radius: 'float', plane: 'Plane', length: 'float') -> 'Circle':
        """The Circle class defines a circle by its radius, the plane it lies in, and its calculated length (circumference).

        - `radius` (float): The radius of the circle.
        - `plane` (Plane): The plane in which the circle lies.
        - `length` (float): The length (circumference) of the circle. Automatically calculated during initialization.
        """
        self.type = __class__.__name__
        self.radius = radius
        self.plane = plane
        self.length = length
        self.id = generateID()
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
        self.type = __class__.__name__
        self.firstRadius = firstRadius
        self.secondRadius = secondRadius
        self.plane = plane
        self.id = generateID()
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
