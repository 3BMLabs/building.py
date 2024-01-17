# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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
from geometry.curve import Line
from helper import *

# [!not included in BP singlefile - end]

class Intersect2d:
    def __init__(self):
        pass

    def perp(self, a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    
    def getLineIntersect(self, line1, line2):
        if line1.start == line1.end or line2.start == line2.end:
            return None

        p1, p2 = line1.start, line1.end
        p1X, p1Y, p1Z = p1.x, p1.y, p1.z
        p2X, p2Y, p2Z = p2.x, p2.y, p2.z

        p3, p4 = line2.start, line2.end
        p3X, p3Y, p3Z = p3.x, p3.y, p3.z
        p4X, p4Y, p4Z = p4.x, p4.y, p4.z

        da = np.array([p2X, p2Y]) - np.array([p1X, p1Y])
        db = np.array([p4X, p4Y]) - np.array([p3X, p3Y])
        dp = np.array([p1X, p1Y]) - np.array([p3X, p3Y])
        dap = self.perp(da)
        denom = np.dot(dap, db)
        if abs(denom) < 1e-6:
            return None
        num = np.dot(dap, dp)
        t = num / denom
        nX, nY = np.array([p3X, p3Y]) + t * db
        return Point(nX, nY, 0)


    def getMultiLineIntersect(self, lines=Line) -> [Point]:
        pts = []
        for i in range(len(lines)):
            line1 = lines[i]
            for j in range(i+1, len(lines)):
                line2 = lines[j]
                intersection = Intersect2d().getLineIntersect(line1, line2)
                if intersection not in pts and intersection != None and is_point_on_line_segment(intersection, line2) == True:
                    pts.append(intersection)
        return pts

    
    def getIntersectLinePolyCurve(self, polycurve, lines, split=None, stretch=None):
        dict = {}
        intersectionsPointsList = []
        splitedLinesList = []
        InnerGridLines = []
        OuterGridLines = []
        if isinstance(lines, Line):
            lines = [lines]
        for line in lines:
            IntersectGridPoints = []
            for i in range(len(polycurve.points) - 1):
                genLine = Line(polycurve.points[i], polycurve.points[i+1])
                checkIntersect = Intersect2d().getLineIntersect(genLine, line)
                # print(checkIntersect)
                if stretch == False or stretch == None:
                    if checkIntersect != None:
                        if is_point_on_line_segment(checkIntersect, line) == False:
                            checkIntersect = None
                        else:
                            minX = min(polycurve.points[i].x, polycurve.points[i+1].x)
                            maxX = max(polycurve.points[i].x, polycurve.points[i+1].x)
                            minY = min(polycurve.points[i].y, polycurve.points[i+1].y)
                            maxY = max(polycurve.points[i].y, polycurve.points[i+1].y)
                        if checkIntersect != None:
                            if minX <= checkIntersect.x <= maxX and minY <= checkIntersect.y <= maxY:
                                intersectionsPointsList.append(checkIntersect)
                                IntersectGridPoints.append(checkIntersect)

                elif stretch == True:
                    minX = min(polycurve.points[i].x, polycurve.points[i+1].x)
                    maxX = max(polycurve.points[i].x, polycurve.points[i+1].x)
                    minY = min(polycurve.points[i].y, polycurve.points[i+1].y)
                    maxY = max(polycurve.points[i].y, polycurve.points[i+1].y)
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
                if is_point_in_polycurve(centerLinePoint, polycurve) == True:
                    InnerGridLines.append(line)
                else:
                    OuterGridLines.append(line)

        # dict["IntersectPolyCurve"] = polycurve
        dict["IntersectGridPoints"] = intersectionsPointsList
        dict["SplittedLines"] = flatten(splitedLinesList)
        dict["InnerGridLines"] = InnerGridLines
        dict["OuterGridLines"] = OuterGridLines

        return dict
    

def is_point_on_line(point, line):
    distance = abs((line.end.y - line.start.y) * point.x
                   - (line.end.x - line.start.x) * point.y
                   + line.end.x * line.start.y
                   - line.end.y * line.start.x) \
               / line.length
    return distance < 1e-9


def is_point_on_line_segment(point, line): #check!!! mogelijk dubbeling
    x_min = min(line.start.x, line.end.x)
    x_max = max(line.start.x, line.end.x)
    y_min = min(line.start.y, line.end.y)
    y_max = max(line.start.y, line.end.y)

    if x_min <= point.x <= x_max and y_min <= point.y <= y_max:
        distance = abs((line.end.y - line.start.y) * point.x
                       - (line.end.x - line.start.x) * point.y
                       + line.end.x * line.start.y
                       - line.end.y * line.start.x) \
                   / line.length
        return distance < 1e-9
    else:
        return False

def find_polycurve_intersections(polycurve1, polycurve2):
    intersections = []
    for i in range(len(polycurve1.points) - 1):
        line1 = Line(polycurve1.points[i], polycurve1.points[i+1])
        for j in range(len(polycurve2.points) - 1):
            line2 = Line(polycurve2.points[j], polycurve2.points[j+1])
            intersection = Intersect2d().getLineIntersect(line1, line2)
            if intersection and is_point_on_line_segment(intersection, line1) and is_point_on_line_segment(intersection, line2):
                intersections.append(intersection)
    return intersections

from geometry.curve import PolyCurve

def split_polycurve_at_intersections(PC, intersections):
    # Sorteer de intersectiepunten gebaseerd op hun afstand vanaf het startpunt
    intersections.sort(key=lambda pt: Point.distance(PC.points[0], pt))

    current_polycurve_points = [PC.points[0]]
    created_polycurves = []

    for i in range(1, len(PC.points)):
        segment_start = PC.points[i - 1]
        segment_end = PC.points[i]

        segment_intersections = [pt for pt in intersections if is_point_on_line_segment(pt, Line(segment_start, segment_end))]

        segment_intersections.sort(key=lambda pt: Point.distance(segment_start, pt))

        for intersect in segment_intersections:
            current_polycurve_points.append(intersect)
            created_polycurves.append(PolyCurve.byPoints(current_polycurve_points))
            current_polycurve_points = [intersect]
            intersections.remove(intersect)

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


# def is_point_in_polycurve(point, polycurve):
    # x, y, z = point.x, point.y, point.z
    # intersections = 0
    # for curve in polycurve.curves:
    #     p1, p2 = curve.start, curve.end
    #     if (y > min(p1.y, p2.y)) and (y <= max(p1.y, p2.y)) and (x <= max(p1.x, p2.x)):
    #         if p1.y != p2.y:
    #             x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
    #             if (p1.x == p2.x) or (x <= x_inters):
    #                 intersections += 1
    # print(intersections)
    # return intersections % 2 != 0


def is_point_in_polycurve(point, polycurve):
    lst = []
    invline = Line(point, Point(point.x+99999, point.y+99999, point.z))
    for curve in polycurve.curves:
        x = Intersect2d().getLineIntersect(curve, invline)
        lst.append(x)
    return lst


def is_polycurve_in_polycurve(mainpolycurve1, polycurve2):
    cp = polycurve2.centroid()
    pts = []
    if is_point_in_polycurve(cp, mainpolycurve1):
        return True
    return is_point_in_polycurve(cp, mainpolycurve1)


def planelineIntersection():
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


def splitCurvesInPolyCurveByPoints(polyCurve, points):
    from abstract.intersect2d import is_point_on_line_segment

    def splitCurveAtPoint(curve, point):
        if is_point_on_line_segment(point, curve):
            return curve.split([point])
        return [curve]

    split_curves = []
    for curve in polyCurve.curves:
        current_curves = [curve]
        for point in points:
            new_curves = []
            for c in current_curves:
                new_curves.extend(splitCurveAtPoint(c, point))
            current_curves = new_curves
        split_curves.extend(current_curves)

    return split_curves

def inLine(line, point):
    if line.start == point or line.end == point:
        return True
    return False


def splitPolyCurveByLine(polyCurve, line):
    from abstract.intersect2d import Intersect2d, is_point_on_line_segment
    dict = {}
    pcList = []
    nonsplitted = []
    intersect = Intersect2d().getIntersectLinePolyCurve(polyCurve, line, split=False, stretch=False)
    intersect_points = intersect["IntersectGridPoints"]
    if len(intersect_points) != 2:
        # print(f"Need exactly 2 intersection points to split, found {len(intersect_points)}")
        nonsplitted.append(PolyCurve)
        dict["inputPolycurve"] = [PolyCurve]
        dict["splittedPolycurve"] = pcList
        dict["nonsplittedPolycurve"] = nonsplitted
        dict["IntersectGridPoints"] = intersect_points

        return dict


    SegsandPoints = []

    for line in polyCurve.curves:
        for intersect_point in intersect_points:
            if is_point_on_line(intersect_point, line):
                SegsandPoints.append(intersect_point)
                SegsandPoints.append(intersect_point)

        SegsandPoints.append(line)

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