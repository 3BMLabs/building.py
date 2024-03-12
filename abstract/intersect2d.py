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

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.geometry2d import *
from helper import *

# [!not included in BP singlefile - end]

def perp(a):
    b = [None] * len(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def get_line_intersect(line_1, line_2):
    if line_1.start == line_1.end or line_2.start == line_2.end:
        return None

    p1, p2 = line_1.start, line_1.end
    p1X, p1Y = p1.x, p1.y
    p2X, p2Y = p2.x, p2.y

    p3, p4 = line_2.start, line_2.end
    p3X, p3Y = p3.x, p3.y
    p4X, p4Y = p4.x, p4.y

    da = [p2X - p1X, p2Y - p1Y]
    db = [p4X - p3X, p4Y - p3Y]
    dp = [p1X - p3X, p1Y - p3Y]
    dap = perp(da)
    denom = dap[0] * db[0] + dap[1] * db[1]
    if abs(denom) < 1e-6:
        return None
    num = dap[0] * dp[0] + dap[1] * dp[1]
    t = num / denom
    nX, nY = p3X + t * db[0], p3Y + t * db[1]

    return Point2D(nX, nY)


def get_multi_lines_intersect(lines: list[Line2D]) -> list[Point2D]:
    pts = []
    for i in range(len(lines)):
        line1 = lines[i]
        for j in range(i+1, len(lines)):
            line2 = lines[j]
            intersection = get_line_intersect(line1, line2)
            if intersection not in pts and intersection != None and is_point_on_line_segment(intersection, line2) == True:
                pts.append(intersection)
    return pts


def get_intersect_polycurve_lines(polycurve: PolyCurve2D, lines: list[Line2D], split: bool = False, stretch: bool = False):
    dict = {}
    intersectionsPointsList = []
    splitedLinesList = []
    InnerGridLines = []
    OuterGridLines = []
    if isinstance(lines, Line2D):
        lines = [lines]
    elif lines.type == "Line":
        print("Convert Line(s) to Line2D")
        sys.exit()
    else:
        print(f"Incorrect input: {lines}")
    for line in lines:
        IntersectGridPoints = []
        for i in range(len(polycurve.points2D) - 1):
            genLine = Line2D(polycurve.points2D[i], polycurve.points2D[i+1])
            checkIntersect = get_line_intersect(genLine, line)
            if stretch == False:
                if checkIntersect != None:
                    if is_point_on_line_segment(checkIntersect, line) == False:
                        checkIntersect = None
                    else:
                        minX = min(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                        maxX = max(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                        minY = min(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                        maxY = max(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                    if checkIntersect != None:
                        if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                            intersectionsPointsList.append(checkIntersect)
                            IntersectGridPoints.append(checkIntersect)

            elif stretch == True:
                minX = min(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                maxX = max(polycurve.points2D[i].x, polycurve.points2D[i+1].x)
                minY = min(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                maxY = max(polycurve.points2D[i].y, polycurve.points2D[i+1].y)
                if checkIntersect != None:
                    if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                        intersectionsPointsList.append(checkIntersect)
                        IntersectGridPoints.append(checkIntersect)

        if split == True:
            if len(IntersectGridPoints) > 0:
                splitedLinesList.append(line.split(IntersectGridPoints))

    for splittedLines in splitedLinesList:
        for line in splittedLines:
            centerLinePoint = line.point_at_parameter(0.5)
            if is_point_in_polycurve(centerLinePoint, polycurve) == True:
                InnerGridLines.append(line)
            else:
                OuterGridLines.append(line)

    dict["IntersectGridPoints"] = intersectionsPointsList
    dict["SplittedLines"] = flatten(splitedLinesList)
    dict["InnerGridLines"] = InnerGridLines
    dict["OuterGridLines"] = OuterGridLines

    return dict


def is_point_on_line_segment(point: Point2D, line: Line2D) -> bool:
    x_min = min(line.start.x, line.end.x)
    x_max = max(line.start.x, line.end.x)
    y_min = min(line.start.y, line.end.y)
    y_max = max(line.start.y, line.end.y)

    if x_min <= point.x <= x_max and y_min <= point.y <= y_max:
        try:
            distance = abs((line.end.y - line.start.y) * point.x
                        - (line.end.x - line.start.x) * point.y
                        + line.end.x * line.start.y
                        - line.end.y * line.start.x) \
                    / line.length
            return distance < 1e-9
        except:
            return False
    return False


def get_intersection_polycurve_polycurve(polycurve_1: PolyCurve2D, polycurve_2: PolyCurve2D) -> list[Point2D]:
    points = []
    for i in range(len(polycurve_1.points2D) - 1):
        line1 = Line2D(polycurve_1.points2D[i], polycurve_1.points2D[i+1])
        for j in range(len(polycurve_2.points2D) - 1):
            line2 = Line2D(polycurve_2.points2D[j], polycurve_2.points2D[j+1])
            intersection = get_line_intersect(line1, line2)
            if intersection and is_point_on_line_segment(intersection, line1) and is_point_on_line_segment(intersection, line2):
                points.append(intersection)
    return points


def split_polycurve_at_intersections(polycurve: PolyCurve2D, points: list[Point2D]) -> list[PolyCurve2D]:
    points.sort(key=lambda pt: Point2D.distance(polycurve.points2D[0], pt))

    current_polycurve_points = [polycurve.points2D[0]]
    created_polycurves = []

    for i in range(1, len(polycurve.points2D)):
        segment_start = polycurve.points2D[i - 1]
        segment_end = polycurve.points2D[i]

        segment_intersections = [pt for pt in points if is_point_on_line_segment(pt, Line2D(segment_start, segment_end))]

        segment_intersections.sort(key=lambda pt: Point2D.distance(segment_start, pt))

        for intersect in segment_intersections:
            current_polycurve_points.append(intersect)
            created_polycurves.append(polycurve.by_points(current_polycurve_points))
            current_polycurve_points = [intersect]
            points.remove(intersect)

        current_polycurve_points.append(segment_end)

    if len(current_polycurve_points) > 1:
        created_polycurves.append(polycurve.by_points(current_polycurve_points))

    ptlist = []
    for index, pc in enumerate(created_polycurves):
        if index == 0:
            for pt in pc.points2D:
                ptlist.append(pt)
        elif index == 2:
            for pt in pc.points2D:
                ptlist.append(pt)
                ptlist.append(ptlist[1])

    pcurve = polycurve().by_points(ptlist)

    try:
        return [created_polycurves[1], pcurve]
    except:
        return [created_polycurves[0]]


#extend to if on edge, then accept
def is_point_in_polycurve(point: Point2D, polycurve: PolyCurve2D) -> bool:
    x, y = point.x, point.y
    intersections = 0
    for curve in polycurve.curves:
        p1, p2 = curve.start, curve.end
        if (y > min(p1.y, p2.y)) and (y <= max(p1.y, p2.y)) and (x <= max(p1.x, p2.x)):
            if p1.y != p2.y:
                x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if (p1.x == p2.x) or (x <= x_inters):
                    intersections += 1
    return intersections % 2 != 0


def is_polycurve_in_polycurve(polycurve_1: PolyCurve2D, polycurve_2: PolyCurve2D) -> bool:
    colList = []
    for pt in polycurve_1.points2D:
        if is_point_in_polycurve(pt, polycurve_2):
            colList.append(True)
        else:
            colList.append(False)

    if all_true(colList):
        return True
    else:
        return False


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


def split_polycurve_by_points(polycurve: PolyCurve2D, points: list[Point2D]) -> list[PolyCurve2D]:
    from abstract.intersect2d import is_point_on_line_segment

    def splitCurveAtPoint(curve, point):
        if is_point_on_line_segment(point, curve):
            return curve.split([point])
        return [curve]

    split_curves = []
    for curve in polycurve.curves:
        current_curves = [curve]
        for point in points:
            new_curves = []
            for c in current_curves:
                new_curves.extend(splitCurveAtPoint(c, point))
            current_curves = new_curves
        split_curves.extend(current_curves)

    return split_curves


def is_on_line(line: Line2D, point: Point2D) -> bool:
    if line.start == Point2D or line.end == Point2D:
        return True
    return False


def split_polycurve_by_line(polycurve: PolyCurve2D, line: Line2D) -> dict[PolyCurve2D]:
    dict = {}
    pcList = []
    nonsplitted = []
    intersect = get_intersect_polycurve_lines(polycurve, line, split=False, stretch=False)
    intersect_points = intersect["IntersectGridPoints"]
    if len(intersect_points) != 2:
        nonsplitted.append(polycurve)
        dict["inputPolycurve"] = [polycurve]
        dict["splittedPolycurve"] = pcList
        dict["nonsplittedPolycurve"] = nonsplitted
        dict["IntersectGridPoints"] = intersect_points
        return dict

    SegsandPoints = []

    for Line in polycurve.curves:
        for intersect_point in intersect_points:
            if is_point_on_line_segment(intersect_point, Line):
                SegsandPoints.append(intersect_point)
                SegsandPoints.append(intersect_point)

        SegsandPoints.append(Line)

    elementen = []
    for item in SegsandPoints:
        elementen.append(item)

    split_lists = []
    current_list = []

    for element in elementen:
        current_list.append(element)

        if len(current_list) > 1 and current_list[-1].type == current_list[-2].type == 'Point2D':
            split_lists.append(current_list[:-1])
            current_list = [element]

    if current_list:
        split_lists.append(current_list)
    
    merged_list = split_lists[-1] + split_lists[0]

    lijsten = [merged_list, split_lists[1]]
    
    for lijst in lijsten:
        q = []
        for i in lijst:
            if i.type == "Line2D":
                q.append(i.end)
            elif i.type == "Point2D":
                q.append(i)
        pc = PolyCurve2D.by_points(q)
        pcList.append(pc)

    dict["inputPolycurve"] = [polycurve]
    dict["splittedPolycurve"] = pcList
    dict["nonsplittedPolycurve"] = nonsplitted
    dict["IntersectGridPoints"] = intersect_points

    return dict