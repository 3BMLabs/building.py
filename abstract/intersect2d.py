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

import sys, os, math
from pathlib import Path
from typing import Any, List
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point
from geometry.curve import Line
from packages.helper import *

class Intersect2d:
    def __init__(self):
        pass

    def perp(self, a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    
    #two lines intersect
    def getIntersectPoint(self, line1, line2):
        # Check that the input lines are valid
        if line1.start == line1.end or line2.start == line2.end:
            return None  # Invalid input lines

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
            return None  # Lines are parallel or coincident
        num = np.dot(dap, dp)
        t = num / denom
        nX, nY = np.array([p3X, p3Y]) + t * db
        return Point(nX, nY, 0)

    
    #polycurve to line intersect
    def getIntersectPointPolyCurve(self, polycurves: List[Point], lines, split=None) -> List[Point]:
        dict = {}
        intersectionsPoints = []
        splitedLines = []
        if type(lines) == list:
            for line in lines:
                tmpPts = []
                for i in range(len(polycurves.points) - 1):
                    genLine = Line(polycurves.points[i], polycurves.points[i+1])
                    inCheck = Intersect2d().getIntersectPoint(genLine, line)

                    minX = min(polycurves.points[i].x, polycurves.points[i+1].x)
                    maxX = max(polycurves.points[i].x, polycurves.points[i+1].x)
                    minY = min(polycurves.points[i].y, polycurves.points[i+1].y)
                    maxY = max(polycurves.points[i].y, polycurves.points[i+1].y)
                    if inCheck != None:
                        if minX <= inCheck.x <= maxX and minY <= inCheck.y <= maxY:
                            intersectionsPoints.append(inCheck)
                            tmpPts.append(inCheck)
                if split == True:
                    if len(tmpPts) > 0:
                        splitedLines.append(line.split(tmpPts))

        elif lines.__class__.__name__ == "Line":
            
            for i in range(len(polycurves.points) - 1):
                tmpPts = []
                genLine = Line(polycurves.points[i], polycurves.points[i+1])
                inCheck = Intersect2d().getIntersectPoint(genLine, lines)
                minX = min(polycurves.points[i].x, polycurves.points[i+1].x)
                maxX = max(polycurves.points[i].x, polycurves.points[i+1].x)
                minY = min(polycurves.points[i].y, polycurves.points[i+1].y)
                maxY = max(polycurves.points[i].y, polycurves.points[i+1].y)
                # if inCheck != None:
                    # if minX <= inCheck.x <= maxX and minY <= inCheck.y <= maxY:
                    #     intersectionsPoints.append(inCheck)
                    # tmpPts.append(inCheck)
                    #     print(inCheck)
                    # if split == True:
                        # print(inCheck)
                        # print(lines)
                        # print(tmpPts)
                        # if len(tmpPts) > 0:
                        #     splitedLines.append(lines.split(tmpPts))
            sys.exit()
        
        dict["IntersectPoints"] = intersectionsPoints
        dict["IntersectLines"] = splitedLines

        return dict
    
    # shorter
    # for line in lines if isinstance(lines, list) else [lines]:
    # for i in range(len(polycurves.points) - 1):
    #     genLine = Line(polycurves.points[i], polycurves.points[i+1])
    #     inCheck = Intersect2d().getIntersectPoint(genLine, line)

    #     x_vals = [polycurves.points[i].x, polycurves.points[i+1].x]
    #     y_vals = [polycurves.points[i].y, polycurves.points[i+1].y]
    #     if min(x_vals) <= inCheck.x <= max(x_vals) and min(y_vals) <= inCheck.y <= max(y_vals):
    #         intersectionsPoints.append(inCheck)


def is_point_in_polygon(point, polygon):
    x, y, z = point.x, point.y, point.z
    intersections = 0
    for curve in polygon.curves:
        p1, p2 = curve.start, curve.end
        if (y > min(p1.y, p2.y)) and (y <= max(p1.y, p2.y)) and (x <= max(p1.x, p2.x)):
            if p1.y != p2.y:
                x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                if (p1.x == p2.x) or (x <= x_inters):
                    intersections += 1
    # print(intersections % 2 != 0)
    return intersections % 2 != 0


def is_polygon_in_polygon(polygon1, polygon2):
    booleans2 = []
    pts2 = []
    for curve in polygon2.curves:
        pts2S, pts2E = curve.start, curve.end
        booleans2.append(is_point_in_polygon(pts2S, polygon1))
        booleans2.append(is_point_in_polygon(pts2E, polygon1))
    print(all_true(booleans2))
    return all_true(booleans2)
    #is_point_in_polygon(Point5, ply1) #True


def planelineIntersection():
    # Define a line by its direction vector and a point on it
    line_dir = [1, 2, 3] # direction vector of the line
    line_pt = [0, 0, 0] # a point on the line

    # Define a plane by its normal vector and a point on it
    plane_norm = [4, 5, 6] # normal vector of the plane
    plane_pt = [1, 1, 1] # a point on the plane

    # Compute the dot product of the line direction and the plane normal
    dot_prod = sum([a*b for a,b in zip(line_dir, plane_norm)])

    # Check if the dot product is zero, which means the line is parallel to the plane
    if dot_prod == 0:
        print("The line is parallel to the plane. No intersection point.")
    else:
        # Compute the parameter t that gives the intersection point
        t = sum([(a-b)*c for a,b,c in zip(plane_pt, line_pt, plane_norm)]) / dot_prod

        # Compute the intersection point by plugging t into the line equation
        inter_pt = [a + b*t for a,b in zip(line_pt, line_dir)]

        # Print the intersection point
        print("The intersection point is", inter_pt)