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

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point, Point2D
from geometry.curve import Line

class Intersect:
    def __init__(self):
        pass

    def getIntersect(self, line1:Line, line2:Line):
        self.p1, self.q1 = line1.start, line1.end
        self.p2, self.q2 = line2.start, line2.end
        o1 = self.orientation(self.p1, self.q1, self.p2)
        o2 = self.orientation(self.p1, self.q1, self.q2)
        o3 = self.orientation(self.p2, self.q2, self.p1)
        o4 = self.orientation(self.p2, self.q2, self.q1)

        print(o1, o2, o3, o4)
        # if type(line1.start).__name__ == "Point":
        if (o1 != o2) and (o3 != o4):
            x1, y1, z1 = self.p1.x, self.p1.y, self.p1.z
            x2, y2, z2 = self.q1.x, self.q1.y, self.q1.z
            x3, y3, z3 = self.p2.x, self.p2.y, self.p2.z
            x4, y4, z4 = self.q2.x, self.q2.y, self.q2.z
            px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
            py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
            pz = ((x1*y2-y1*x2)*(z3-z4)-(x1-x2)*(z3*y4-z4*y3))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))

            intersection_point = Point(x=px, y=py, z=pz)
            # check if the intersection point lies on both lines
            if self.onSegment(self.p1, self.q1, intersection_point) and self.onSegment(self.p2, self.q2, intersection_point):
                return intersection_point

        # return None if there is no intersection
        return None

    def onSegment(self, p, q, r):
        return q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y) and q.z <= max(p.z, r.z) and q.z >= min(p.z, r.z)

    def orientation(self, p, q, r):
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            return 1 # Clockwise orientation
        elif (val < 0):
            return 2 # Counterclockwise orientation
        else:
            return 0 # Collinear orientation