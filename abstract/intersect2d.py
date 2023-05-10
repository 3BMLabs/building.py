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


class Intersect2d:
    def __init__(self):
        pass

    def perp(self, a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    
    #two lines intersect
    def getIntersectPoint(self, line1: Line, line2: Line) -> Point:
        p1, p2 = line1.start, line1.end
        p1X, p1Y, P1Z = p1.x, p1.y, p1.z
        p2X, p2Y, P2Z = p2.x, p2.y, p2.z

        p3, p4 = line2.start, line2.end
        p3X, p3Y, P3Z = p3.x, p3.y, p3.z
        p4X, p4Y, P4Z = p4.x, p4.y, p4.z

        da = np.array([p2X, p2Y])-np.array([p1X, p1Y])
        db = np.array([p4X, p4Y])-np.array([p3X, p3Y])
        dp = np.array([p1X, p1Y])-np.array([p3X, p3Y])
        dap = self.perp(da)
        denom = np.dot(dap, db)
        num = np.dot(dap, dp)
        nX, nY = (num / denom.astype(float))*db + np.array([p3X, p3Y])
        return Point(nX, nY, 0)
    
    #polycurve to line intersect
    def getIntersectPointPolyCurve(self, polycurves: List[Point], lines, split=None) -> List[Point]:
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
                    if minX <= inCheck.x <= maxX and minY <= inCheck.y <= maxY:
                        intersectionsPoints.append(inCheck)
                        tmpPts.append(inCheck)
                if split == True:
                    if len(tmpPts) > 0:
                        splitedLines.append(line.split(tmpPts))

        elif lines.__class__.__name__ == "Line":
            for i in range(len(polycurves.points) - 1):
                genLine = Line(polycurves.points[i], polycurves.points[i+1])
                inCheck = Intersect2d().getIntersectPoint(genLine, lines)

                minX = min(polycurves.points[i].x, polycurves.points[i+1].x)
                maxX = max(polycurves.points[i].x, polycurves.points[i+1].x)
                minY = min(polycurves.points[i].y, polycurves.points[i+1].y)
                maxY = max(polycurves.points[i].y, polycurves.points[i+1].y)
                if minX <= inCheck.x <= maxX and minY <= inCheck.y <= maxY:
                    intersectionsPoints.append(inCheck)

        return intersectionsPoints, splitedLines
    
    # shorter
    # for line in lines if isinstance(lines, list) else [lines]:
    # for i in range(len(polycurves.points) - 1):
    #     genLine = Line(polycurves.points[i], polycurves.points[i+1])
    #     inCheck = Intersect2d().getIntersectPoint(genLine, line)

    #     x_vals = [polycurves.points[i].x, polycurves.points[i+1].x]
    #     y_vals = [polycurves.points[i].y, polycurves.points[i+1].y]
    #     if min(x_vals) <= inCheck.x <= max(x_vals) and min(y_vals) <= inCheck.y <= max(y_vals):
    #         intersectionsPoints.append(inCheck)
