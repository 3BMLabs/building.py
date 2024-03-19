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
from abstract.vector import Vector3
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
        return Vector3(
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
    from abstract.vector import Vector3
    from geometry.point import Point
    PointLocal = Point(PointLocal1.x, PointLocal1.y, 0)
    # pn = Point.translate(CoordinateSystemNew.Origin, Vector3.scale(CoordinateSystemNew.Xaxis, PointLocal.x))
    # pn2 = Point2D.translate(pn, Vector3.scale(CoordinateSystemNew.Y_axis, PointLocal.y))
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


class Arc2D:
    def __init__(self, pntxy1, pntxy2, pntxy3) -> None:
        self.id = generateID()
        self.type = __class__.__name__
        self.start: Point2D = pntxy1
        self.mid: Point2D = pntxy2
        self.end: Point2D = pntxy3
        self.origin = self.origin_arc()
        self.angle_radian = self.angle_radian()
        self.radius = self.radius_arc()
        # self.radius = self.radius_arc()
        self.coordinatesystem = self.coordinatesystem_arc()
        # self.length

    def serialize(self):
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'start': self.start.serialize(),
            'mid': self.mid.serialize(),
            'end': self.end.serialize(),
            'origin': self.origin,
            'angle_radian': self.angle_radian,
            'coordinatesystem': self.coordinatesystem
        }

    @staticmethod
    def deserialize(data):
        start_point = Point2D.deserialize(data['start'])
        mid_point = Point2D.deserialize(data['mid'])
        end_point = Point2D.deserialize(data['end'])
        arc = Arc2D(start_point, mid_point, end_point)

        arc.origin = data.get('origin')
        arc.angle_radian = data.get('angle_radian')
        arc.coordinatesystem = data.get('coordinatesystem')

        return arc

    def __id__(self):
        return f"id:{self.id}"

    def points(self):
        # returns point on the curve
        return (self.start, self.mid, self.end)

    def coordinatesystem_arc(self):
        vx2d = Vector2.by_two_points(self.origin, self.start)  # Local X-axe
        vx = Vector3(vx2d.x, vx2d.y, 0)
        vy = Vector3(vx.y, vx.x * -1, 0)
        vz = Vector3(0, 0, 1)
        self.coordinatesystem = CoordinateSystem(self.origin, Vector3.normalize(
            vx), Vector3.normalize(vy), Vector3.normalize(vz))
        return self.coordinatesystem

    def angle_radian(self):
        v1 = Vector2.by_two_points(self.origin, self.end)
        v2 = Vector2.by_two_points(self.origin, self.start)
        angle = Vector2.angle_radian_between(v1, v2)
        return angle

    def origin_arc(self):
        # calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector2.by_two_points(self.start, self.end)
        halfVstartend = Vector2.scale(Vstartend, 0.5)
        # half distance between start and end
        b = 0.5 * Vector2.length(Vstartend)
        try:
            # distance from start-end line to origin
            x = math.sqrt(Arc2D.radius_arc(self) *
                          Arc2D.radius_arc(self) - b * b)
        except:
            x = 0
        mid = Point2D.translate(self.start, halfVstartend)
        v2 = Vector2.by_two_points(self.mid, mid)
        v3 = Vector2.normalize(v2)
        tocenter = Vector2.scale(v3, x)
        center = Point2D.translate(mid, tocenter)
        self.origin = center
        return center

    def radius_arc(self):
        a = Vector2.length(Vector2.by_two_points(self.start, self.mid))
        b = Vector2.length(Vector2.by_two_points(self.mid, self.end))
        c = Vector2.length(Vector2.by_two_points(self.end, self.start))
        s = (a + b + c) / 2
        A = math.sqrt(s * (s-a) * (s-b) * (s-c))
        R = (a * b * c) / (4 * A)
        return R

    @staticmethod
    def points_at_parameter(arc, count: int):
        # ToDo can be simplified. Now based on the 3D variant
        d_alpha = arc.angle_radian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point2D(arc.radius * math.cos(alpha),
                        arc.radius * math.sin(alpha)))
            alpha = alpha + d_alpha
        CSNew = arc.coordinatesystem
        pnts2 = []
        for i in pnts:
            pnts2.append(transform_point_2D(i, CSNew))
        return pnts2

    @staticmethod
    def segmented_arc(arc, count):
        pnts = Arc2D.points_at_parameter(arc, count)
        i = 0
        lines = []
        for j in range(len(pnts)-1):
            lines.append(Line2D(pnts[i], pnts[i+1]))
            i = i + 1
        return lines

    def __str__(self):
        return f"{__class__.__name__}({self.start},{self.mid},{self.end})"


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
    def copy_translate(pc, vector3d: Vector3):
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

    def to_polycurve_2D(self):
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
    def transform_from_origin(polycurve, startpoint: Point2D, directionvector: Vector3):
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
