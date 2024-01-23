# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


"""This module provides tools for intersects
"""

__title__= "intersect"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/intersect.py"

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point
from geometry.curve import Line, PolyCurve
# from geometry.geometry2d import Vector2, Point2D, Line2D, PolyCurve2D
from helper import *

# [!not included in BP singlefile - end]

def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

#getLineIntersect
def get_line_intersect(Line_1=Line, Line_2=Line) -> Point:
    if Line_1.start == Line_1.end or Line_2.start == Line_2.end:
        return None

    p1, p2 = Line_1.start, Line_1.end
    p1X, p1Y, p1Z = p1.x, p1.y, p1.z
    p2X, p2Y, p2Z = p2.x, p2.y, p2.z

    p3, p4 = Line_2.start, Line_2.end
    p3X, p3Y, p3Z = p3.x, p3.y, p3.z
    p4X, p4Y, p4Z = p4.x, p4.y, p4.z

    da = np.array([p2X, p2Y]) - np.array([p1X, p1Y])
    db = np.array([p4X, p4Y]) - np.array([p3X, p3Y])
    dp = np.array([p1X, p1Y]) - np.array([p3X, p3Y])
    dap = perp(da)
    denom = np.dot(dap, db)
    if abs(denom) < 1e-6:
        return None
    num = np.dot(dap, dp)
    t = num / denom
    nX, nY = np.array([p3X, p3Y]) + t * db
    return Point(nX, nY, 0)


#getMultiLineIntersect
def get_multi_line_intersect(Lines=Line) -> list[Point]:
    pts = []
    for i in range(len(Lines)):
        line1 = Lines[i]
        for j in range(i+1, len(Lines)):
            line2 = Lines[j]
            intersection = get_line_intersect(line1, line2)
            if intersection not in pts and intersection != None and is_point_on_line_segment(intersection, line2) == True:
                pts.append(intersection)
    return pts


#getIntersectLinePolyCurve
def get_intersect_polycurve_lines(PolyCurve=PolyCurve, Lines=list[Line], split: bool = False, stretch: bool = False):
    dict = {}
    intersectionsPointsList = []
    splitedLinesList = []
    InnerGridLines = []
    OuterGridLines = []
    if Lines.type == "Line":
        Lines = [Lines]
    for line in Lines:
        IntersectGridPoints = []
        for i in range(len(PolyCurve.points) - 1):
            genLine = Line(PolyCurve.points[i], PolyCurve.points[i+1])
            checkIntersect = get_line_intersect(genLine, line)
            if stretch == False or stretch == None:
                if checkIntersect != None:
                    if is_point_on_line_segment(checkIntersect, line) == False:
                        checkIntersect = None
                    else:
                        minX = min(PolyCurve.points[i].x, PolyCurve.points[i+1].x)
                        maxX = max(PolyCurve.points[i].x, PolyCurve.points[i+1].x)
                        minY = min(PolyCurve.points[i].y, PolyCurve.points[i+1].y)
                        maxY = max(PolyCurve.points[i].y, PolyCurve.points[i+1].y)
                    if checkIntersect != None:
                        if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                            intersectionsPointsList.append(checkIntersect)
                            IntersectGridPoints.append(checkIntersect)

            elif stretch == True:
                minX = min(PolyCurve.points[i].x, PolyCurve.points[i+1].x)
                maxX = max(PolyCurve.points[i].x, PolyCurve.points[i+1].x)
                minY = min(PolyCurve.points[i].y, PolyCurve.points[i+1].y)
                maxY = max(PolyCurve.points[i].y, PolyCurve.points[i+1].y)
                if checkIntersect != None:
                    if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                        intersectionsPointsList.append(checkIntersect)
                        IntersectGridPoints.append(checkIntersect)

        if split == True:
            if len(IntersectGridPoints) > 0:
                splitedLinesList.append(line.split(IntersectGridPoints))


    for splittedLines in splitedLinesList:
        for line in splittedLines:
            centerLinePoint = line.pointAtParameter(0.5)
            if is_point_in_polycurve(centerLinePoint, PolyCurve) == True:
                InnerGridLines.append(line)
            else:
                OuterGridLines.append(line)

    dict["IntersectGridPoints"] = intersectionsPointsList
    dict["SplittedLines"] = flatten(splitedLinesList)
    dict["InnerGridLines"] = InnerGridLines
    dict["OuterGridLines"] = OuterGridLines

    return dict

#is_point_on_line
def is_point_on_line(Point:Point, Line:Line) -> bool:
    distance = abs((Line.end.y - Line.start.y) * Point.x
                   - (Line.end.x - Line.start.x) * Point.y
                   + Line.end.x * Line.start.y
                   - Line.end.y * Line.start.x) \
               / Line.length
    return distance < 1e-9

#is_point_on_line_segment
def is_point_on_line_segment(Point:Point, Line:Line) -> bool: #check!!! mogelijk dubbeling
    x_min = min(Line.start.x, Line.end.x)
    x_max = max(Line.start.x, Line.end.x)
    y_min = min(Line.start.y, Line.end.y)
    y_max = max(Line.start.y, Line.end.y)

    if x_min <= Point.x <= x_max and y_min <= Point.y <= y_max:
        distance = abs((Line.end.y - Line.start.y) * Point.x
                       - (Line.end.x - Line.start.x) * Point.y
                       + Line.end.x * Line.start.y
                       - Line.end.y * Line.start.x) \
                   / Line.length
        return distance < 1e-9
    else:
        return False

#find_polycurve_intersections
def get_intersection_polycurves(PolyCurve_1:PolyCurve, PolyCurve_2:PolyCurve) -> list[Point]:
    points = []
    for i in range(len(PolyCurve_1.points) - 1):
        line1 = Line(PolyCurve_1.points[i], PolyCurve_1.points[i+1])
        for j in range(len(PolyCurve_2.points) - 1):
            line2 = Line(PolyCurve_2.points[j], PolyCurve_2.points[j+1])
            intersection = get_line_intersect(line1, line2)
            if intersection and is_point_on_line_segment(intersection, line1) and is_point_on_line_segment(intersection, line2):
                points.append(intersection)
    return points


#split_polycurve_at_intersections
def split_polycurve_at_intersections(PolyCurve:PolyCurve, Points:list[Point]) -> list[PolyCurve]:
    Points.sort(key=lambda pt: Point.distance(PolyCurve.points[0], pt))

    current_polycurve_points = [PolyCurve.points[0]]
    created_polycurves = []

    for i in range(1, len(PolyCurve.points)):
        segment_start = PolyCurve.points[i - 1]
        segment_end = PolyCurve.points[i]

        segment_intersections = [pt for pt in Points if is_point_on_line_segment(pt, Line(segment_start, segment_end))]

        segment_intersections.sort(key=lambda pt: Point.distance(segment_start, pt))

        for intersect in segment_intersections:
            current_polycurve_points.append(intersect)
            created_polycurves.append(PolyCurve.byPoints(current_polycurve_points))
            current_polycurve_points = [intersect]
            Points.remove(intersect)

        current_polycurve_points.append(segment_end)

    if len(current_polycurve_points) > 1:
        created_polycurves.append(PolyCurve.byPoints(current_polycurve_points))

    ptlist = []
    for index, pc in enumerate(created_polycurves):
        if index == 0:
            for pt in pc.points:
                ptlist.append(pt)
        elif index == 2:
            for pt in pc.points:
                ptlist.append(pt)
                ptlist.append(ptlist[1])

    pcurve = PolyCurve().byPoints(ptlist)

    try:
        return [created_polycurves[1], pcurve]
    except:
        return [created_polycurves[0]]

#is_point_in_polycurve
def is_point_in_polycurve(Point:Point, PolyCurve:PolyCurve) -> bool:
    x, y, z = Point.x, Point.y, Point.z
    intersections = 0
    for curve in PolyCurve.curves:
        p1, p2 = curve.start, curve.end
        if (y > min(p1.y, p2.y)) and (y <= max(p1.y, p2.y)) and (x <= max(p1.x, p2.x)):
            if p1.y != p2.y:
                x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if (p1.x == p2.x) or (x <= x_inters):
                    intersections += 1
    # print(intersections)
    return intersections % 2 != 0


#is_polycurve_in_polycurve
def is_polycurve_in_polycurve(PolyCurve_1:PolyCurve, PolyCurve_2:PolyCurve) -> bool:
    for pt in PolyCurve_2.points:
        if is_point_in_polycurve(pt, PolyCurve_1):
            return True
    return False


#planelineIntersection
def plane_line_intersection():
    line_dir = [1, 2, 3]
    line_pt = [0, 0, 0]

    plane_norm = [4, 5, 6]
    plane_pt = [1, 1, 1]

    dot_prod = sum([a*b for a,b in zip(line_dir, plane_norm)])

    if dot_prod == 0:
        print("The line is parallel to the plane. No intersection point.")
    else:
        t = sum([(a-b)*c for a,b,c in zip(plane_pt, line_pt, plane_norm)]) / dot_prod

        inter_pt = [a + b*t for a,b in zip(line_pt, line_dir)]

        print("The intersection point is", inter_pt)


#splitCurvesInPolyCurveByPoints
def split_polycurve_by_points(PolyCurve:PolyCurve, Points:list[Point]) -> list[PolyCurve]:
    from abstract.intersect2d import is_point_on_line_segment

    def splitCurveAtPoint(curve, point):
        if is_point_on_line_segment(point, curve):
            return curve.split([point])
        return [curve]

    split_curves = []
    for curve in PolyCurve.curves:
        current_curves = [curve]
        for point in Points:
            new_curves = []
            for c in current_curves:
                new_curves.extend(splitCurveAtPoint(c, point))
            current_curves = new_curves
        split_curves.extend(current_curves)

    return split_curves


#inLine
def is_on_line(Line:Line, Point:Point) -> bool:
    if Line.start == Point or Line.end == Point:
        return True
    return False


#splitPolyCurveByLine
def split_polycurve_by_line(PolyCurve:PolyCurve, Line:Line) -> dict[PolyCurve]:
    dict = {}
    pcList = []
    nonsplitted = []
    intersect = get_intersect_polycurve_lines(PolyCurve, Line, split=False, stretch=False)
    intersect_points = intersect["IntersectGridPoints"]
    if len(intersect_points) != 2:
        nonsplitted.append(PolyCurve)
        dict["inputPolycurve"] = [PolyCurve]
        dict["splittedPolycurve"] = pcList
        dict["nonsplittedPolycurve"] = nonsplitted
        dict["IntersectGridPoints"] = intersect_points
        return dict

    SegsandPoints = []

    for Line in PolyCurve.curves:
        for intersect_point in intersect_points:
            if is_point_on_line(intersect_point, Line):
                SegsandPoints.append(intersect_point)
                SegsandPoints.append(intersect_point)

        SegsandPoints.append(Line)

    elementen = []
    for item in SegsandPoints:
        elementen.append(item)

    gesplitste_lijsten = []
    huidige_lijst = []

    for element in elementen:
        huidige_lijst.append(element)

        if len(huidige_lijst) > 1 and huidige_lijst[-1].type == huidige_lijst[-2].type == 'Point':
            gesplitste_lijsten.append(huidige_lijst[:-1])
            huidige_lijst = [element]

    if huidige_lijst:
        gesplitste_lijsten.append(huidige_lijst)

    samengevoegde_lijst = gesplitste_lijsten[-1] + gesplitste_lijsten[0]

    lijsten = [samengevoegde_lijst, gesplitste_lijsten[1]]
    
    for lijst in lijsten:
        q = []
        for i in lijst:
            if i.type == "Line":
                q.append(i.end)
            elif i.type == "Point":
                q.append(i)
        pc = PolyCurve.byPoints(q)
        pcList.append(pc)

    dict["inputPolycurve"] = [PolyCurve]
    dict["splittedPolycurve"] = pcList
    dict["nonsplittedPolycurve"] = nonsplitted
    dict["IntersectGridPoints"] = intersect_points

    return dict