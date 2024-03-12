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

__title__= "curve"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/curve.py"


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.plane import Plane
from helper import *
from abstract.vector import *
from geometry.point import Point
from project.fileformat import project
from abstract.coordinatesystem import CoordinateSystem, CSGlobal
from geometry.point import transform_point

# [!not included in BP singlefile - end]

class Line: #add Line.bylenght (start and endpoint)
    def __init__(self, start: Point, end: Point) -> None:
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
        self.vector: Vector3 = Vector3.byTwoPoints(start,end)
        self.vector_normalised = Vector3.normalize(self.vector)

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        start_serialized = self.start.serialize() if hasattr(self.start, 'serialize') else str(self.start)
        end_serialized = self.end.serialize() if hasattr(self.end, 'serialize') else str(self.end)

        # Serialize vector if it has a serialize method, otherwise convert to string representation
        vector_serialized = self.vector.serialize() if hasattr(self.vector, 'serialize') else str(self.vector)
        vector_normalized_serialized = self.vector_normalised.serialize() if hasattr(self.vector_normalised, 'serialize') else str(self.vector_normalised)

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
    def deserialize(data):
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
            instance.vector_normalised = Vector3.deserialize(data['vector_normalised'])
        else:
            instance.vector_normalised = data['vector_normalised']

        return instance

    @staticmethod
    def by_startpoint_direction_length(start:Point, direction:Vector3, length:float):
        norm = math.sqrt(direction.x ** 2 + direction.y ** 2 + direction.z ** 2)
        normalized_direction = Vector3(direction.x / norm, direction.y / norm, direction.z / norm)
        
        end_x = start.x + normalized_direction.x * length
        end_y = start.y + normalized_direction.y * length
        end_z = start.z + normalized_direction.z * length
        end_point = Point(end_x, end_y, end_z)
        
        return Line(start, end_point)

    def translate(self,direction:Vector3):
        self.start = Point.translate(self.start,direction)
        self.end = Point.translate(self.end,direction)
        return self

    @staticmethod
    def translate_2(line,direction:Vector3):
        line.start = Point.translate(line.start,direction)
        line.end = Point.translate(line.end,direction)
        return line

    @staticmethod
    def transform(line, CSNew: CoordinateSystem):
        ln = Line(start=line.start, end=line.end)
        ln.start = transformPoint2(ln.start,CSNew)
        ln.end = transformPoint2(ln.end,CSNew)
        return ln

    def offset(line, vector):
        start = Point(line.start.x + vector.x, line.start.y + vector.y, line.start.z + vector.z)
        end = Point(line.end.x + vector.x, line.end.y + vector.y, line.end.z + vector.z)
        return Line(start=start, end=end)

    # @classmethod
    def point_at_parameter(self, interval=None):
        if interval == None:
            interval = 0.0
        x1, y1, z1 = self.start.x, self.start.y, self.start.z
        x2, y2, z2 = self.end.x, self.end.y, self.end.z
        if float(interval) == 0.0:
            return self.start
        else:
            devBy = 1/interval
            return Point((x1 + x2) / devBy, (y1 + y2) / devBy, (z1 + z2) / devBy)

    def mid_point(self):
        vect = Vector3.scale(self.vector,0.5)
        mid = Point.translate(self.start,vect)
        return mid

    def split(self, points: Point):
        lines = []
        if isinstance(points, list):        
            points.extend([self.start, self.end])
            sorted_points = sorted(points, key=lambda p: p.distance(p,self.end))
            lines = create_lines(sorted_points)
            return lines
        elif isinstance(points, Point):
            point = points
            lines.append(Line(start=self.start, end=point))
            lines.append(Line(start=point, end=self.end))
            return lines


    def length(self):
        return math.sqrt(math.sqrt(self.dx * self.dx + self.dy * self.dy) * math.sqrt(self.dx * self.dx + self.dy * self.dy) + self.dz * self.dz)

    def __str__(self):
        return f"{__class__.__name__}(" + f"{self.start}, {self.end})"


def create_lines(points):
    lines = []
    for i in range(len(points)-1):
        line = Line(points[i], points[i+1])
        lines.append(line)
    return lines


class PolyCurve:
    def __init__(self):
        self.id = generateID()
        self.type = __class__.__name__        
        self.curves = []
        self.points = []
        self.segmentcurves = None
        self.width = None
        self.height = None
        #Methods ()
        # self.close
        #pointonperimeter
        #Properties
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
        curves_serialized = [curve.serialize() if hasattr(curve, 'serialize') else str(curve) for curve in self.curves]
        points_serialized = [point.serialize() if hasattr(point, 'serialize') else str(point) for point in self.points]

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

    def scale(self, scalefactor):
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                arcie = Arc(Point.product(scalefactor, i.start), Point.product(scalefactor, i.end))
                arcie.mid = Point.product(scalefactor,i.mid)
                crvs.append(arcie)
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.product(scalefactor, i.start), Point.product(scalefactor, i.end)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.by_joined_curves(crvs)
        return crv

    def get_width(self) -> float:
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


    def centroid(self) -> Point:
        if self.isClosed:
            num_points = len(self.points)
            if num_points < 3:
                return "Polygon has less than 3 points!"

            A = 0.0
            for i in range(num_points):
                x0, y0 = self.points[i].x, self.points[i].y
                x1, y1 = self.points[(i + 1) % num_points].x, self.points[(i + 1) % num_points].y
                A += x0 * y1 - x1 * y0
            A *= 0.5

            Cx, Cy = 0.0, 0.0
            for i in range(num_points):
                x0, y0 = self.points[i].x, self.points[i].y
                x1, y1 = self.points[(i + 1) % num_points].x, self.points[(i + 1) % num_points].y
                factor = (x0 * y1 - x1 * y0)
                Cx += (x0 + x1) * factor
                Cy += (y0 + y1) * factor

            Cx /= (6.0 * A)
            Cy /= (6.0 * A)

            return Point(x=round(Cx, project.decimals), y=round(Cy, project.decimals), z=self.points[0].z)
        else:
            return None

    def area(self) -> float:  # shoelace formula
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


    def length(self) -> float:
        lst = []
        for line in self.curves:
            lst.append(line.length)

        return sum(i.length for i in self.curves)


    def close(self) -> bool:
        if self.curves[0] == self.curves[-1]:
            return self
        else:
            self.curves.append(self.curves[0])
            plycrv = PolyCurve()
            for curve in self.curves:
                plycrv.curves.append(curve)
        return plycrv

    @classmethod
    def by_joined_curves(self, curvelst: list[Line]):
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
    def byPoints(self, points: list[Point]):
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
    def unclosed_by_points(self, points: list[Point]):
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
    def segment(self, count): #Create segmented polycurve. Arcs, elips will be translated to straight lines
        crvs = [] #add isClosed
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc.segmented_arc(i, count))
            elif i.__class__.__name__ == "Line":
                crvs.append(i)
        crv = flatten(crvs)
        pc = PolyCurve.by_joined_curves(crv)
        return pc

    @staticmethod
    def byPolyCurve2D(PolyCurve2D):
        # by points,
        plycrv = PolyCurve()
        curves = []
        for i in PolyCurve2D.curves:
            if i.__class__.__name__ == "Arc2D":
                curves.append(Arc(Point(i.start.x, i.start.y, 0), Point(i.mid.x, i.mid.y, 0), Point(i.end.x,i.end.y, 0)))
            elif i.__class__.__name__ == "Line2D":
                curves.append(Line(Point(i.start.x, i.start.y,0),Point(i.end.x, i.end.y,0)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        plycrv.points = pnts
        plycrv.curves = curves
        return plycrv


    def split(self, line: Line, returnlines=None): #make sure that the lines start/stop already on the edge of the polycurve
        from abstract.intersect2d import Intersect2d, is_point_on_line_segment

        allLines = self.curves.copy()

        # insect = Intersect2d().getIntersectLinePolyCurve(self, line, split=True, stretch=False)
        # for pt in insect["IntersectGridPoints"]:
        #     for index, line in enumerate(allLines):
        #         if is_point_on_line_segment(pt, line) == True:
        #             cuttedLines = line.split([pt])
        #             allLines = replace_at_index(allLines,index, cuttedLines)

        insect = Intersect2d().getIntersectLinePolyCurve(self, line, split=True, stretch=False)
        for pt in insect["IntersectGridPoints"]:
            for index, line in enumerate(allLines):
                if is_point_on_line_segment(pt, line) == True:
                    cuttedLines = line.split([pt])
                    allLines = replace_at_index(allLines,index, cuttedLines)

        if len(insect["IntersectGridPoints"]) == 2:
            part1 = []
            part2 = []

            for j in allLines:
                #part1
                if j.start == insect["IntersectGridPoints"][1]:
                    part1LineEnd = j.end
                    part1.append(j.start)
                if j.end == insect["IntersectGridPoints"][0]:
                    part1LineStart = j.start
                    part1.append(j.end)
                #part2
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
            #part1
            if part1LineStart != None and part1LineEnd != None:
                for i, index in enumerate(partlist1):
                    pts = self.points[index]
                    part1.insert(i+1, pts)
                if returnlines:
                    SplittedPolyCurves.append(PolyCurve.byPoints(part1))
                else:
                    project.objects.append(PolyCurve.byPoints(part1))

            #part2 -> BUGG?
            if part2LineStart != None and part2LineEnd != None:
                for index in partlist2:
                    pts = self.points[index]
                    part2.insert(index, pts)
                if returnlines:
                    SplittedPolyCurves.append(PolyCurve.byPoints(part2))
                else:
                    project.objects.append(PolyCurve.byPoints(part2))

            if returnlines: #return lines while using multi_split
                return SplittedPolyCurves

        else:
            print(f"Must need 2 points to split PolyCurve into PolyCurves, got now {len(insect['IntersectGridPoints'])} points.")


    def multi_split(self, lines:Line): #SOOOO SLOW, MUST INCREASE SPEAD
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


    def translate(self, vector3d:Vector3):
        crvs = []
        v1 = vector3d
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.translate(i.start, v1), Point.translate(i.middle, v1), Point.translate(i.end, v1)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.translate(i.start, v1), Point.translate(i.end, v1)))
            else:
                print("Curvetype not found")
        pc = PolyCurve()
        pc.curves = crvs
        return pc

    @staticmethod
    def copyTranslate(pc, vector3d:Vector3):
        crvs = []
        v1 = vector3d
        for i in pc.curves:
            #if i.__class__.__name__ == "Arc":
            #    crvs.append(Arc(Point.translate(i.start, v1), Point.translate(i.middle, v1), Point.translate(i.end, v1)))
            if i.__class__.__name__ == "Line":
                crvs.append(Line(Point.translate(i.start, v1), Point.translate(i.end, v1)))
            else:
                print("Curvetype not found")

        PCnew = PolyCurve.by_joined_curves(crvs)
        return PCnew

    def rotate(self, angle, dz):
        #angle in degrees
        #dz = displacement in z-direction
        crvs = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                crvs.append(Arc(Point.rotateXY(i.start, angle, dz), Point.rotateXY(i.middle, angle, dz), Point.rotateXY(i.end, angle, dz)))
            elif i.__class__.__name__ == "Line":
                crvs.append(Line(Point.rotateXY(i.start, angle, dz), Point.rotateXY(i.end, angle, dz)))
            else:
                print("Curvetype not found")
        crv = PolyCurve.by_joined_curves(crvs)
        return crv

    def to_polycurve_2D(self):
        # by points,
        from geometry.geometry2d import PolyCurve2D
        from geometry.geometry2d import Point2D
        from geometry.geometry2d import Line2D
        from geometry.geometry2d import Arc2D

        p1 = PolyCurve2D()
        count = 0
        curves = []
        for i in self.curves:
            if i.__class__.__name__ == "Arc":
                curves.append(Arc2D(Point2D(i.start.x, i.start.y), Point2D(i.middle.x, i.middle.y),
                                  Point2D(i.end.x, i.end.y)))
            elif i.__class__.__name__ == "Line":
                curves.append(Line2D(Point2D(i.start.x, i.start.y), Point2D(i.end.x, i.end.y)))
            else:
                print("Curvetype not found")
        pnts = []
        for i in curves:
            pnts.append(i.start)
        pnts.append(curves[0].start)
        p1.points = pnts
        p1.curves = curves
        return p1

    @staticmethod
    def transform_from_origin(polycurve, startpoint: Point, directionvector: Vector3):
        crvs = []
        if polycurve.type == "PolyCurve2D":
            for i in polycurve.curves:
                if i.__class__.__name__ == "Arc":
                    crvs.append(Arc(transform_point(i.start,CSGlobal,startpoint,directionvector),
                                    transform_point(i.mid, CSGlobal, startpoint, directionvector),
                                    transform_point(i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line":
                    crvs.append(Line(start = transform_point(i.start,CSGlobal,startpoint,directionvector),
                                    end = transform_point(i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Arc2D":
                    # print(Point.point2DTo3D(i.start),CSGlobal, startpoint, directionvector)
                    crvs.append(Arc(transform_point(Point.point2DTo3D(i.start),CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point2DTo3D(i.mid), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point2DTo3D(i.end), CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line2D":
                    crvs.append(Line(start = transform_point(Point.point2DTo3D(i.start),CSGlobal,startpoint,directionvector),
                                    end = transform_point(Point.point2DTo3D(i.end), CSGlobal, startpoint, directionvector)
                                    ))
                else:
                    print(i.__class__.__name__ + "Curvetype not found")
        elif polycurve.type == "PolyCurve":
            for i in polycurve.curves:
                if i.__class__.__name__ == "Arc":
                    crvs.append(Arc(transform_point(i.start,CSGlobal,startpoint,directionvector),
                                    transform_point(i.mid, CSGlobal, startpoint, directionvector),
                                    transform_point(i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line":
                    crvs.append(Line(start = transform_point(i.start,CSGlobal,startpoint,directionvector),
                                    end = transform_point(i.end, CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Arc2D":
                    # print(Point.point2DTo3D(i.start),CSGlobal, startpoint, directionvector)
                    crvs.append(Arc(transform_point(Point.point2DTo3D(i.start),CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point2DTo3D(i.mid), CSGlobal, startpoint, directionvector),
                                    transform_point(Point.point2DTo3D(i.end), CSGlobal, startpoint, directionvector)
                                    ))
                elif i.__class__.__name__ == "Line2D":
                    crvs.append(Line(start = transform_point(Point.point2DTo3D(i.start),CSGlobal,startpoint,directionvector),
                                    end = transform_point(Point.point2DTo3D(i.end), CSGlobal, startpoint, directionvector)
                                    ))
                else:
                    print(i.__class__.__name__ + "Curvetype not found")
  
        pc = PolyCurve()
        pc.curves = crvs
        return pc

    def __str__(self):
        l = len(self.points)
        return f"{__class__.__name__}, ({l} points)"
            
# 2D PolyCurve to 3D PolyGon

def Rect(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane with translation of vector
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(width, 0, 0), vector)
    p3 = Point(0,0,0).translate(Point(width, height, 0), vector)
    p4 = Point(0,0,0).translate(Point(0, height, 0), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4, p1])
    return crv

def RectXY(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(width, 0, 0), vector)
    p3 = Point(0,0,0).translate(Point(width, 0, height), vector)
    p4 = Point(0,0,0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4])
    return crv

def RectYZ(vector: Vector3, width: float, height: float):
    #Rectangle in XY-plane
    p1 = Point(0,0,0).translate(Point(0, 0, 0), vector)
    p2 = Point(0,0,0).translate(Point(0, width, 0), vector)
    p3 = Point(0,0,0).translate(Point(0, width, height), vector)
    p4 = Point(0,0,0).translate(Point(0, 0, height), vector)
    crv = PolyCurve.byPoints([p1, p2, p3, p4, p1])
    return crv



class PolyGon:
    def __init__(self, lines) -> None:
        self.type = __class__.__name__        
        self.Lines = lines#collect in list
        self.id = generateID()
        pass #Lines
    
    @staticmethod
    def polygon(flatCurves: Line) -> Point:
        points = []
        for i in flatCurves:
            points.append(i.start)
            try:
                points.append(i.middle)
            except:
                pass
        points.append(points[0])
        points3D = []
        for i in points:
            points3D.append(Point.point2DTo3D(i))
        return points3D

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Arc:
    def __init__(self, startPoint: Point, midPoint: Point, endPoint: Point):
        self.id = generateID()
        self.type = __class__.__name__        
        self.start = startPoint
        self.mid = midPoint
        self.end = endPoint
        self.origin = self.origin_arc()
        v1 = Vector3(x=1, y=0, z=0)
        v2 = Vector3(x=0, y=1, z=0)
        self.plane = Plane.byTwoVectorsOrigin(
            v1,
            v2,
            self.origin
        )
        self.radius = self.radiusarc()
        self.startAngle = 0
        self.endAngle = 0
        self.angleRadian = self.angleRadian()
        self.area = 0
        self.length = self.length()
        self.units = project.units
        self.coordinatesystem = self.coordinatesystemarc()

    def distance(self, p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2)

    def coordinatesystemarc(self):
        vx = Vector3.byTwoPoints(self.origin, self.start)  # Local X-axe
        v2 = Vector3.byTwoPoints(self.end, self.origin)
        vz = Vector3.crossProduct(vx, v2)  # Local Z-axe
        vy = Vector3.crossProduct(vx, vz)  # Local Y-axe
        self.coordinatesystem = CoordinateSystem(self.origin, Vector3.normalize(vx), Vector3.normalize(vy),
                                                 Vector3.normalize(vz))
        return self.coordinatesystem

    def radiusarc(self):
        a = self.distance(self.start, self.mid)
        b = self.distance(self.mid, self.end)
        c = self.distance(self.end, self.start)
        s = (a + b + c) / 2
        A = math.sqrt(s * (s - a) * (s - b) * (s - c))
        R = (a * b * c) / (4 * A)
        return R

    def origin_arc(self):
        # calculation of origin of arc #Todo can be simplified for sure
        Vstartend = Vector3.byTwoPoints(self.start, self.end)
        halfVstartend = Vector3.scale(Vstartend, 0.5)
        b = 0.5 * Vector3.length(Vstartend)  # half distance between start and end
        x = math.sqrt(Arc.radiusarc(self) * Arc.radiusarc(self) - b * b)  # distance from start-end line to origin
        mid = Point.translate(self.start, halfVstartend)
        v2 = Vector3.byTwoPoints(self.mid, mid)
        v3 = Vector3.normalize(v2)
        tocenter = Vector3.scale(v3, x)
        center = Point.translate(mid, tocenter)
        return center

    def angleRadian(self):
        v1 = Vector3.byTwoPoints(self.origin, self.end)
        v2 = Vector3.byTwoPoints(self.origin, self.start)
        v3 = Vector3.byTwoPoints(self.origin, self.mid)
        v4 = Vector3.sum(v1,v2)
        try:
            v4b = Vector3.new_length(v4,self.radius)
            if Vector3.value(v3) == Vector3.value(v4b):
                angle = Vector3.angleRadianBetween(v1, v2)
            else:
                angle = 2*math.pi-Vector3.angleRadianBetween(v1, v2)
            return angle
        except:
            angle = 2*math.pi-Vector3.angleRadianBetween(v1, v2)
            return angle

    def length(self):
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

    @staticmethod
    def points_at_parameter(arc, count: int):
        # Create points at parameter on an arc based on an interval
        d_alpha = arc.angleRadian / (count - 1)
        alpha = 0
        pnts = []
        for i in range(count):
            pnts.append(Point(arc.radius * math.cos(alpha), arc.radius * math.sin(alpha), 0))
            alpha = alpha + d_alpha
        CSNew = arc.coordinatesystem
        pnts2 = []  # transformed points
        for i in pnts:
            pnts2.append(transformPoint2(i, CSNew))
        return pnts2

    @staticmethod
    def segmented_arc(arc, count):
        pnts = Arc.points_at_parameter(arc, count)
        i = 0
        lines = []
        for j in range(len(pnts) - 1):
            lines.append(Line(pnts[i], pnts[i + 1]))
            i = i + 1
        return lines

    def __str__(self) -> str:
        return f"{__class__.__name__}()"

def transform_arc(Arcold,CSNew: CoordinateSystem):
    start = transformPoint2(Arcold.start,CSNew)
    mid = transformPoint2(Arcold.mid,CSNew)
    end = transformPoint2(Arcold.end,CSNew)
    Arcnew = Arc(startPoint=start,midPoint=mid,endPoint=end)

    return Arcnew

class Circle: #auto calculate length!
    def __init__(self, radius, plane, length) -> None:
        self.type = __class__.__name__        
        self.radius = radius
        self.plane = plane
        self.length = length
        self.id = generateID()
        pass #Curve

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"


class Ellipse:
    def __init__(self, firstRadius, secondRadius, plane) -> None:
        self.type = __class__.__name__        
        self.firstRadius = firstRadius
        self.secondRadius = secondRadius
        self.plane = plane
        self.id = generateID()
        pass #Curve
    pass

    def __id__(self):
        return f"id:{self.id}"

    def __str__(self) -> str:
        return f"{__class__.__name__}({self})"