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

import numpy as np
import sys, os, math
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from abstract.vector import *
from geometry.point import Point
from geometry.curve import Line


class Intersect: #werkt nog niet!!
    def __init__(self):
        pass

    def getIntersect(self, line1:Line, line2:Line):
        a, b = line1.start, line1.end
        c, d = line2.start, line2.end

        d1 = Vector3.diff(b, a)
        d2 = Vector3.diff(d, c)
        print(d1, d2)

        n = Vector3.crossProduct(d1, d2)
        print(n)
        
        w = Vector3.crossProduct(d1, n)
        print(w)

        # t = Vector3.sum(d, d2)
        t = Vector3.crossProduct(d1, d2)
        w*(d, d2)

        dp1 = Vector3.dotProduct(Vector3.crossProduct(w, d1), n)
        sp1 = Vector3.square(n)

        t = Vector3(
            sp1.x / dp1,
            sp1.y / dp1,
            sp1.z / dp1
        )
        
        p = Vector3.sum(a, Vector3.crossProduct(d1, t))
        print(p)
        return Vector3.toPoint(p)


    def __str__(self) -> str:
        return "Intersection of two lines in 3D space."


